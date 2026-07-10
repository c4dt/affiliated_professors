"""Provider-agnostic pydantic-ai agent that turns prefetched source data into a
structured ProfileUpdate. Model is selected from env so the same code runs
against Anthropic, OpenAI, or any OpenAI-compatible endpoint.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from .models import ProfileUpdate
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
- readme_paragraph: a concise paragraph (2-4 sentences) for the index page.

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
    )

    @agent.tool
    def scrape_url(ctx: RunContext[Deps], url: str) -> str:
        """Scrape a single web page to markdown. Hard-capped per run."""
        if ctx.deps.scrapes_done >= ctx.deps.scrape_budget:
            return "Scrape budget exhausted (max 3 per run). Do not call scrape_url again."
        ctx.deps.scrapes_done += 1
        try:
            return firecrawl_scrape(url, ctx.deps.firecrawl_api_key)[:20000]
        except Exception as e:  # noqa: BLE001 - report to the model, don't crash
            return f"Scrape failed for {url}: {e}"

    return agent


def run_update(prompt: str, firecrawl_api_key: str | None = None) -> ProfileUpdate:
    agent = make_agent()
    result = agent.run_sync(prompt, deps=Deps(firecrawl_api_key=firecrawl_api_key))
    return result.output
