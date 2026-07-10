"""One-time: build professors.yaml from the C4DT labs listing.

Scrapes the paginated WordPress archive, has the LLM extract a professor/lab
list, resolves each to an OpenAlex author, and writes registry entries with
reviewed=false for a human to check before going live. Existing entries (by
slug) are preserved verbatim — re-running never clobbers reviewed data.
"""

from __future__ import annotations

import re
import sys
import unicodedata

from .models import Professor, RegistryEntry
from .registry import load_registry, save_registry
from .sources import firecrawl_scrape, openalex_find_author

_EXTRACT_INSTRUCTIONS = """\
You are given the markdown of the C4DT "laboratory" listing page(s). Extract
every EPFL laboratory and its lead professor. For each, return:
- name: the lead professor's full name (person, not the lab).
- lab: the laboratory's name.
- lab_url: the laboratory's own website URL if present in the text, otherwise
  the C4DT lab page URL.
Only include real labs with an identifiable lead professor. Do not invent data.
"""

_MAX_PAGES = 6


def _slugify(name: str) -> str:
    norm = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    norm = re.sub(r"[^a-zA-Z0-9]+", "-", norm).strip("-").lower()
    return norm


def _bare_openalex_id(author: dict | None) -> str | None:
    if not author or not author.get("id"):
        return None
    return author["id"].rstrip("/").split("/")[-1]


def _scrape_pages(start_url: str) -> str:
    base = start_url.rstrip("/")
    pages: list[str] = []
    for i in range(1, _MAX_PAGES + 1):
        page_url = base + "/" if i == 1 else f"{base}/page/{i}/"
        try:
            md = firecrawl_scrape(page_url)
        except Exception as e:  # noqa: BLE001 - 404 or last page: stop paginating
            print(f"  stop at page {i}: {e}", file=sys.stderr)
            break
        pages.append(md)
        print(f"  scraped page {i} ({len(md)} chars)", file=sys.stderr)
    return "\n\n---PAGE BREAK---\n\n".join(pages)


def _extract(markdown: str) -> list[RegistryEntry]:
    from pydantic_ai import Agent

    from .agent import build_model

    agent = Agent(
        build_model(),
        output_type=list[RegistryEntry],
        instructions=_EXTRACT_INSTRUCTIONS,
        defer_model_check=True,
    )
    return agent.run_sync(markdown).output


def run_bootstrap(start_url: str = "https://c4dt.epfl.ch/laboratory/") -> int:
    print(f"Scraping {start_url} ...", file=sys.stderr)
    markdown = _scrape_pages(start_url)
    if not markdown.strip():
        print("No content scraped.", file=sys.stderr)
        return 1

    entries = _extract(markdown)
    print(f"Extracted {len(entries)} labs.", file=sys.stderr)

    profs = load_registry()
    by_slug = {p.slug: p for p in profs}
    added = 0
    for e in entries:
        slug = _slugify(e.name)
        if not slug or slug in by_slug:
            continue
        author = openalex_find_author(e.name)
        prof = Professor(
            slug=slug,
            name=e.name,
            lab=e.lab,
            lab_url=e.lab_url,
            github_org=None,
            openalex_id=_bare_openalex_id(author),
            reviewed=False,
        )
        profs.append(prof)
        by_slug[slug] = prof
        added += 1
        aff = author.get("affiliation") if author else None
        print(f"  + {e.name} ({slug}) openalex={prof.openalex_id} [{aff}]", file=sys.stderr)

    save_registry(profs)
    print(
        f"\nAdded {added} new professors ({len(profs)} total).\n"
        "HUMAN REVIEW REQUIRED before go-live:\n"
        "  - verify each openalex_id (wrong id => confidently wrong summaries)\n"
        "  - fill in github_org where applicable\n"
        "  - flip reviewed: true once checked",
        file=sys.stderr,
    )
    return 0
