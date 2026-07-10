"""Deterministic fetchers for the three data sources. Each raises on failure;
callers wrap in try/except so one dead source doesn't wedge the run.
"""

from __future__ import annotations

import os

import httpx

FIRECRAWL_ENDPOINT = "https://api.firecrawl.dev/v2/scrape"
GITHUB_API = "https://api.github.com"
OPENALEX_API = "https://api.openalex.org"
MAILTO = "linus.gasser@epfl.ch"

_TIMEOUT = httpx.Timeout(60.0, connect=15.0)


def firecrawl_scrape(url: str, api_key: str | None = None) -> str:
    """Scrape a URL to markdown via Firecrawl v2. Returns the markdown body."""
    api_key = api_key or os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        raise RuntimeError("FIRECRAWL_API_KEY not set")
    resp = httpx.post(
        FIRECRAWL_ENDPOINT,
        headers={"Authorization": f"Bearer {api_key}"},
        json={"url": url, "formats": ["markdown"]},
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    data = resp.json().get("data", {})
    markdown = data.get("markdown")
    if not markdown:
        raise RuntimeError(f"Firecrawl returned no markdown for {url}")
    return markdown


def github_org_repos(org: str, token: str | None = None, per_page: int = 15) -> list[dict]:
    """Recently-pushed repos for a GitHub org (name, description, url,
    pushed_at, stars, language)."""
    token = token or os.environ.get("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    resp = httpx.get(
        f"{GITHUB_API}/orgs/{org}/repos",
        headers=headers,
        params={"sort": "pushed", "per_page": per_page},
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    return [
        {
            "name": r["name"],
            "description": r.get("description"),
            "url": r["html_url"],
            "pushed_at": r.get("pushed_at"),
            "stars": r.get("stargazers_count"),
            "language": r.get("language"),
        }
        for r in resp.json()
    ]


def openalex_recent_works(openalex_id: str, per_page: int = 25) -> list[dict]:
    """Recent works for an OpenAlex author id (title, date, venue, doi, url)."""
    resp = httpx.get(
        f"{OPENALEX_API}/works",
        params={
            "filter": f"authorships.author.id:{openalex_id}",
            "sort": "publication_date:desc",
            "per-page": per_page,
            "mailto": MAILTO,
        },
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    works = resp.json().get("results", [])
    out = []
    for w in works:
        loc = (w.get("primary_location") or {}).get("source") or {}
        out.append(
            {
                "title": w.get("title"),
                "publication_date": w.get("publication_date"),
                "venue": loc.get("display_name"),
                "doi": w.get("doi"),
                "url": w.get("id"),
                "cited_by_count": w.get("cited_by_count"),
            }
        )
    return out


def openalex_find_author(name: str) -> dict | None:
    """Top author hit for a name search, preferring EPFL affiliation."""
    resp = httpx.get(
        f"{OPENALEX_API}/authors",
        params={"search": name, "per-page": 10, "mailto": MAILTO},
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    results = resp.json().get("results", [])
    if not results:
        return None

    def is_epfl(a: dict) -> bool:
        inst = (a.get("last_known_institutions") or []) + (
            [a["last_known_institution"]] if a.get("last_known_institution") else []
        )
        return any("EPFL" in (i.get("display_name") or "").upper()
                   or "FÉDÉRALE DE LAUSANNE" in (i.get("display_name") or "").upper()
                   for i in inst)

    epfl_hits = [a for a in results if is_epfl(a)]
    chosen = epfl_hits[0] if epfl_hits else results[0]
    return {
        "id": chosen.get("id"),
        "display_name": chosen.get("display_name"),
        "works_count": chosen.get("works_count"),
        "affiliation": (
            (chosen.get("last_known_institutions") or [{}])[0].get("display_name")
            if chosen.get("last_known_institutions")
            else (chosen.get("last_known_institution") or {}).get("display_name")
        ),
    }
