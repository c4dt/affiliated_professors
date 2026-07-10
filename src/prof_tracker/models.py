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
    lab_url: str = ""
    github_org: str | None = None
    orcid: str | None = None  # authoritative identity anchor (human-verified)
    openalex_id: str | None = None  # optional fallback when no ORCID
    one_sentence_summary: str = ""
    readme_paragraph: str = ""
    last_updated: str | None = None  # ISO date (YYYY-MM-DD), null until first run
    reviewed: bool = False


class ProfileUpdate(BaseModel):
    """Structured output the agent must produce for one professor."""

    one_sentence_summary: str
    important_links: list[Link] = Field(default_factory=list)  # 3-6 items
    changelog_entry: str  # markdown bullets for today's dated entry
    significant: bool  # worth announcing on Matrix?
    matrix_summary: str  # 1-2 sentences
    readme_paragraph: str


class RegistryEntry(BaseModel):
    """One professor extracted during bootstrap from the C4DT labs listing."""

    slug: str
    name: str
    lab: str = ""
    lab_url: str = ""


def profile_filename(slug: str) -> str:
    """professors/<SLUG>.md — flat, uppercase filename."""
    return f"{slug.upper()}.md"
