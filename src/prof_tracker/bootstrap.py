"""One-time: build professors.yaml from the C4DT labs listing.

Scrapes the paginated WordPress archive, has the LLM extract a professor/lab
list, resolves each to an OpenAlex author, and writes registry entries with
reviewed=false for a human to check before going live. Existing entries (by
slug) are preserved verbatim — re-running never clobbers reviewed data.
"""

from __future__ import annotations

import logging
import re
import time
import unicodedata

from .models import Professor, RegistryEntry
from .registry import load_registry, save_registry
from .sources import firecrawl_scrape, openalex_find_author

logger = logging.getLogger(__name__)

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
            logger.debug("Stop paginating at page %d: %s", i, e)
            break
        pages.append(md)
        logger.info("Scraped page %d (%d chars)", i, len(md))
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


def resolve_orcids() -> int:
    """Fill candidate ORCIDs (and OpenAlex ids) via name search for human
    verification. For reviewed=false entries, candidates overwrite untrusted
    ids; for reviewed=true entries, only a missing ORCID is filled and the
    human-set openalex_id is left untouched. Prints a table to verify.
    """
    profs = load_registry()
    rows: list[tuple] = []
    seen_orcid: dict[str, str] = {}

    for p in profs:
        if p.reviewed and p.orcid:
            continue  # already anchored + trusted
        try:
            author = openalex_find_author(p.name)
        except Exception as e:  # noqa: BLE001 - throttle/network: keep existing, flag, go on
            logger.warning("ORCID lookup failed for %s: %s", p.name, e)
            rows.append((p.name, p.orcid, None, "LOOKUP-FAILED (kept existing)"))
            continue
        time.sleep(0.2)  # stay under OpenAlex's polite-pool rate limit
        orcid = author.get("orcid") if author else None
        oa_id = _bare_openalex_id(author)
        disp = author.get("display_name") if author else None
        works = author.get("works_count") if author else None
        aff = author.get("affiliation") if author else None

        if p.reviewed:
            p.orcid = p.orcid or orcid  # don't touch trusted openalex_id
        else:
            p.orcid = orcid
            p.openalex_id = oa_id

        # verification hints
        name_ok = _slugify(p.name).split("-")[-1] in _slugify(disp or "").split("-")
        dup = seen_orcid.get(orcid) if orcid else None
        if orcid:
            seen_orcid[orcid] = p.name
        flags = []
        if not orcid:
            flags.append("NO-ORCID")
        if not name_ok:
            flags.append(f"NAME?({disp})")
        if aff and "LAUSANNE" not in aff.upper():
            flags.append(f"AFF?({aff})")
        if dup:
            flags.append(f"DUP-with:{dup}")
        rows.append((p.name, orcid, works, " ".join(flags)))

    save_registry(profs)

    logger.info("\n=== ORCID candidates — VERIFY each (https://orcid.org/<id>) ===")
    for name, orcid, works, flags in rows:
        mark = "  " if not flags else "!!"
        logger.info("%s %s %s works=%-5s %s", mark, f"{name:<32}", f"{orcid or '-':<21}", works or "-", flags)
    flagged = sum(1 for r in rows if r[3])
    logger.info(
        "\n%d entries resolved, %d flagged for closer review.\n"
        "Verify each ORCID against the professor's real profile, correct any wrong\n"
        "ones by hand, fill epfl_profile + code_urls, then set reviewed: true.",
        len(rows),
        flagged,
    )
    return 0


def run_bootstrap(start_url: str = "https://c4dt.epfl.ch/laboratory/") -> int:
    logger.info("Scraping %s ...", start_url)
    markdown = _scrape_pages(start_url)
    if not markdown.strip():
        logger.warning("No content scraped.")
        return 1

    entries = _extract(markdown)
    logger.info("Extracted %d labs.", len(entries))

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
            epfl_profile="",  # filled in by hand during review
            lab_urls=[e.lab_url] if e.lab_url else [],
            code_urls=[],
            orcid=author.get("orcid") if author else None,
            openalex_id=_bare_openalex_id(author),
            reviewed=False,
        )
        profs.append(prof)
        by_slug[slug] = prof
        added += 1
        aff = author.get("affiliation") if author else None
        logger.info("  + %s (%s) openalex=%s [%s]", e.name, slug, prof.openalex_id, aff)

    save_registry(profs)
    logger.info(
        "\nAdded %d new professors (%d total).\n"
        "HUMAN REVIEW REQUIRED before go-live:\n"
        "  - verify each openalex_id (wrong id => confidently wrong summaries)\n"
        "  - add the people.epfl.ch profile as epfl_profile\n"
        "  - fill in code_urls (GitHub/GitLab) where applicable\n"
        "  - flip reviewed: true once checked",
        added,
        len(profs),
    )
    return 0
