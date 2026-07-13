"""Provider-agnostic pydantic-ai agent that turns prefetched source data into a
structured ProfileUpdate. Model is selected from env so the same code runs
against Anthropic, OpenAI, or any OpenAI-compatible endpoint.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass

logger = logging.getLogger(__name__)

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from .models import DiscussionExtraction, Professor, ProfileUpdate
from .sources import firecrawl_scrape

_PROVIDER_ENV = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "google-gla": "GEMINI_API_KEY",
    "groq": "GROQ_API_KEY",
    "mistral": "MISTRAL_API_KEY",
}

INSTRUCTIONS = """\
You maintain a research-tracking profile for one EPFL/C4DT affiliated professor.

You are given: the professor's current profile (if any), and freshly fetched
data from up to three sources (lab website, GitHub org, recent publications).
Some sources may be marked unavailable — just work with what you have.

Produce a ProfileUpdate:
- one_sentence_summary: a crisp sentence describing the professor's research focus.
- important_links: 3-6 curated title+url items (lab, key repos, standout papers).
- changelog_entry: markdown bullets describing ONLY genuinely new or notable
  developments since the existing profile (new papers, active repos, news). If
  nothing is materially new, say so in one short bullet. Do not restate old news.
- significant: true ONLY if there is a genuinely newsworthy development worth
  broadcasting to a team channel; routine activity is not significant.
- matrix_summary: 1-2 sentences summarizing what's new, for a chat announcement.

You may call scrape_url(url) up to 3 times total to follow one interesting link
(e.g. a news post or project page). Use it sparingly.
"""


@dataclass
class Deps:
    firecrawl_api_key: str | None = None
    scrape_budget: int = 3
    scrapes_done: int = 0


def build_model():
    """Return a pydantic-ai model from env.

    LLM_MODEL     provider-prefixed string ("anthropic:claude-sonnet-4-6") or a
                  bare model name when LLM_BASE_URL is set.
    LLM_BASE_URL  optional; any OpenAI-compatible server.
    LLM_API_KEY   mapped to the provider env var when no base URL is given.
    """
    model_str = os.environ.get("LLM_MODEL")
    if not model_str:
        raise RuntimeError("LLM_MODEL not set")
    base_url = os.environ.get("LLM_BASE_URL")
    api_key = os.environ.get("LLM_API_KEY")
    logger.debug("build_model: LLM_MODEL=%s base_url=%s api_key=%s", model_str, base_url, "set" if api_key else "not set")

    if base_url:
        model_name = model_str.split(":", 1)[-1]
        return OpenAIChatModel(
            model_name,
            provider=OpenAIProvider(base_url=base_url, api_key=api_key or "unused"),
        )

    # pydantic-ai string form; make sure the provider's expected env var is set.
    if api_key and ":" in model_str:
        provider = model_str.split(":", 1)[0]
        env_var = _PROVIDER_ENV.get(provider)
        if env_var and not os.environ.get(env_var):
            os.environ[env_var] = api_key
    return model_str


def make_agent() -> Agent[Deps, ProfileUpdate]:
    agent = Agent(
        build_model(),
        deps_type=Deps,
        output_type=ProfileUpdate,
        instructions=INSTRUCTIONS,
        defer_model_check=True,  # allow newer model names not yet in pydantic-ai's list
    )

    @agent.tool
    def scrape_url(ctx: RunContext[Deps], url: str) -> str:
        """Scrape a single web page to markdown. Hard-capped per run."""
        if ctx.deps.scrapes_done >= ctx.deps.scrape_budget:
            logger.debug("scrape_url: budget exhausted, refusing %s", url)
            return "Scrape budget exhausted (max 3 per run). Do not call scrape_url again."
        ctx.deps.scrapes_done += 1
        logger.debug("scrape_url: %s (%d/%d)", url, ctx.deps.scrapes_done, ctx.deps.scrape_budget)
        try:
            return firecrawl_scrape(url, ctx.deps.firecrawl_api_key)[:20000]
        except Exception as e:  # noqa: BLE001 - report to the model, don't crash
            logger.debug("scrape_url failed for %s: %s", url, e)
            return f"Scrape failed for {url}: {e}"

    return agent


def run_update(prompt: str, firecrawl_api_key: str | None = None) -> ProfileUpdate:
    logger.debug("run_update: prompt is %d chars", len(prompt))
    agent = make_agent()
    logger.debug("run_update: starting agent.run_sync")
    result = agent.run_sync(prompt, deps=Deps(firecrawl_api_key=firecrawl_api_key))
    logger.debug("run_update: done, usage=%s", getattr(result, "usage", None))
    return result.output


EXTRACT_INSTRUCTIONS = """\
You extract metadata from raw meeting notes about an EPFL professor.

You are given: raw notes (possibly with a preamble like "Discussed last Thursday
with Clement Pit-Claudel"), a list of professor names and slugs, and today's date.

Return:
- slug: the slug of the professor mentioned (match to the closest registry entry)
- date: the meeting date as YYYY-MM-DD (resolve relative references like
  "last Thursday" using today's date; default to today if no date mentioned)
"""


def run_extract(raw_text: str, professors: list[Professor], today: str) -> DiscussionExtraction:
    """Extract professor slug and meeting date from raw meeting notes."""
    roster = "\n".join(f"{p.slug}: {p.name}" for p in professors)
    agent: Agent[None, DiscussionExtraction] = Agent(
        build_model(),
        output_type=DiscussionExtraction,
        instructions=EXTRACT_INSTRUCTIONS,
        defer_model_check=True,
    )
    prompt = f"Today: {today}\n\nProfessors:\n{roster}\n\nNotes:\n{raw_text}"
    logger.debug("run_extract: prompt is %d chars", len(prompt))
    result = agent.run_sync(prompt)
    logger.debug("run_extract: slug=%s date=%s", result.output.slug, result.output.date)
    return result.output


NOTES_INSTRUCTIONS = """\
You maintain research-tracking profiles for EPFL/C4DT affiliated professors.

You are given: the professor's current profile (for style context) and raw
notes from a personal conversation with the professor about their recent work.

Produce clean, concise markdown that:
- Summarises what the professor described, matching the tone and style of
  their existing profile
- Is 2-5 short paragraphs or a mix of prose and bullets as appropriate
- Focuses on what is new and notable — what the professor highlighted themselves
- Preserves every URL from the notes as a markdown hyperlink, e.g.
  [Paper Title](https://...) — never drop or paraphrase away a link
- Does NOT include the section header (added automatically)
- Does NOT use first-person voice (write as reporting, not quoting)
- Does NOT include any personal information (names of people other than the
  professor, private contact details, sensitive organisational context, or
  anything the professor said off the record) — this profile is stored in a
  public repository

Output ONLY the formatted markdown, no preamble or trailing commentary.
"""


def run_notes(raw_text: str, existing_profile: str) -> str:
    """Format raw meeting notes into markdown for a Notes section."""
    agent: Agent[None, str] = Agent(
        build_model(),
        output_type=str,
        instructions=NOTES_INSTRUCTIONS,
        defer_model_check=True,
    )
    prompt = (
        f"=== EXISTING PROFILE ===\n{existing_profile}\n\n"
        f"=== MEETING NOTES ===\n{raw_text}\n"
    )
    logger.debug("run_notes: prompt is %d chars", len(prompt))
    result = agent.run_sync(prompt)
    return result.output
