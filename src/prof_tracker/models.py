"""Shared pydantic models — kept free of heavy imports so render/registry
can use them without pulling in pydantic-ai."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Link(BaseModel):
    title: str
    url: str


class Professor(BaseModel):
    slug: str
    name: str
    lab: str = ""
    urls: list[str] = Field(default_factory=list)  # lab site, personal page, etc.
    code_urls: list[str] = Field(default_factory=list)  # GitHub/GitLab orgs or users
    orcid: str | None = None  # authoritative identity anchor (human-verified)
    openalex_id: str | None = None  # optional fallback when no ORCID
    last_updated: str | None = None  # ISO date (YYYY-MM-DD), null until first run
    reviewed: bool = False
    # Note: agent-generated prose (summary, links, changelog) lives in the
    # professors/<SLUG>.md profile, not here — the registry is config only.


class ProfileUpdate(BaseModel):
    """Structured output the agent must produce for one professor."""

    one_sentence_summary: str  # profile intro + index blurb + Matrix
    important_links: list[Link] = Field(default_factory=list)  # 3-6 items
    changelog_entry: str  # markdown bullets for today's dated entry
    significant: bool  # worth announcing on Matrix?
    matrix_summary: str  # 1-2 sentences


class RegistryEntry(BaseModel):
    """One professor extracted during bootstrap from the C4DT labs listing."""

    slug: str
    name: str
    lab: str = ""
    lab_url: str = ""


def profile_filename(slug: str) -> str:
    """professors/<SLUG>.md — flat, uppercase filename."""
    return f"{slug.upper()}.md"
