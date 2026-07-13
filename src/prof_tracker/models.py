"""Shared pydantic models — kept free of heavy imports so render/registry
can use them without pulling in pydantic-ai."""

from __future__ import annotations

from urllib.parse import urlparse

from pydantic import BaseModel, Field, model_validator


class Link(BaseModel):
    title: str
    url: str


class Professor(BaseModel):
    slug: str
    name: str
    lab: str = ""
    epfl_profile: str = ""  # canonical people.epfl.ch directory entry (identity anchor)
    lab_urls: list[str] = Field(default_factory=list)  # lab site(s), personal page(s)
    code_urls: list[str] = Field(default_factory=list)  # GitHub/GitLab orgs or users
    orcid: str | None = None  # authoritative identity anchor (human-verified)
    openalex_id: str | None = None  # optional fallback when no ORCID
    last_updated: str | None = None  # ISO date (YYYY-MM-DD), null until first run
    reviewed: bool = False
    # Note: agent-generated prose (summary, links, changelog) lives in the
    # professors/<SLUG>.md profile, not here — the registry is config only.

    @model_validator(mode="after")
    def _check_urls(self) -> Professor:
        """Every professor has exactly one people.epfl.ch profile and at least
        one lab/personal page. Enforced only for reviewed entries — bootstrap
        can't know the people.epfl.ch URL, so unreviewed entries may be
        incomplete until a human fills them in."""
        if not self.reviewed:
            return self
        host = urlparse(self.epfl_profile).netloc
        if host != "people.epfl.ch":
            raise ValueError(
                f"{self.slug}: reviewed entry needs a people.epfl.ch "
                f"epfl_profile (got {self.epfl_profile!r})"
            )
        if not self.lab_urls:
            raise ValueError(f"{self.slug}: reviewed entry needs at least one lab_url")
        return self

    def all_urls(self) -> list[str]:
        """EPFL profile first, then lab/personal pages — the order sources are
        fetched and links are rendered."""
        return ([self.epfl_profile] if self.epfl_profile else []) + self.lab_urls


class ProfileUpdate(BaseModel):
    """Structured output the agent must produce for one professor."""

    one_sentence_summary: str  # profile intro + index blurb + Matrix
    important_links: list[Link] = Field(default_factory=list)  # 3-6 items
    changelog_entry: str  # markdown bullets for today's dated entry
    significant: bool  # worth announcing on Matrix?
    matrix_summary: str  # 1-2 sentences


class DiscussionExtraction(BaseModel):
    """Structured output for extracting professor slug and date from raw meeting notes."""

    slug: str  # matched against the registry
    date: str  # YYYY-MM-DD resolved from text + today's date


class RegistryEntry(BaseModel):
    """One professor extracted during bootstrap from the C4DT labs listing."""

    slug: str
    name: str
    lab: str = ""
    lab_url: str = ""


def profile_filename(slug: str) -> str:
    """professors/<SLUG>.md — flat, uppercase filename."""
    return f"{slug.upper()}.md"
