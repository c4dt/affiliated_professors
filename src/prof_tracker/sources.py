"""Deterministic fetchers for the three data sources. Each raises on failure;
callers wrap in try/except so one dead source doesn't wedge the run.
"""

from __future__ import annotations

import os
import time
import unicodedata

import httpx

FIRECRAWL_ENDPOINT = "https://api.firecrawl.dev/v2/scrape"
GITHUB_API = "https://api.github.com"
OPENALEX_API = "https://api.openalex.org"
MAILTO = "linus.gasser@epfl.ch"

_TIMEOUT = httpx.Timeout(60.0, connect=15.0)


# OpenAlex puts you in the fast "polite pool" when it sees mailto + a
# User-Agent carrying a contact address.
_OPENALEX_UA = f"prof-tracker/0.1 (mailto:{MAILTO})"


def _openalex_get(path: str, params: dict, retries: int = 7) -> dict:
    """GET an OpenAlex endpoint with backoff on 429 (respects Retry-After)."""
    for attempt in range(retries):
        resp = httpx.get(
            f"{OPENALEX_API}/{path}",
            params=params,
            headers={"User-Agent": _OPENALEX_UA},
            timeout=_TIMEOUT,
        )
        if resp.status_code == 429 and attempt < retries - 1:
            wait = float(resp.headers.get("Retry-After", 2**attempt))
            time.sleep(min(wait, 30.0))
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError("unreachable")


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


def github_org_from_url(url: str) -> str | None:
    """Return the org/user slug for a github.com URL, else None."""
    from urllib.parse import urlparse

    parsed = urlparse(url)
    if "github.com" not in parsed.netloc:
        return None
    parts = [p for p in parsed.path.split("/") if p]
    return parts[0] if parts else None


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


def _orcid_url(orcid: str) -> str:
    return orcid if orcid.startswith("http") else f"https://orcid.org/{orcid}"


def works_filter(openalex_id: str | None = None, orcid: str | None = None) -> str:
    """Build the OpenAlex works filter, preferring ORCID.

    Filtering works by ORCID aggregates across OpenAlex's duplicate author
    records — more robust than the name-clustered author id, which is prone to
    collisions and sparse-duplicate records.
    """
    if orcid:
        return f"authorships.author.orcid:{_orcid_url(orcid)}"
    if openalex_id:
        return f"authorships.author.id:{openalex_id}"
    raise ValueError("need orcid or openalex_id")


def openalex_recent_works(
    openalex_id: str | None = None,
    orcid: str | None = None,
    per_page: int = 25,
) -> list[dict]:
    """Recent works for an author (title, date, venue, doi, url). Prefers ORCID."""
    payload = _openalex_get(
        "works",
        {
            "filter": works_filter(openalex_id, orcid),
            "sort": "publication_date:desc",
            "per-page": per_page,
            "mailto": MAILTO,
        },
    )
    works = payload.get("results", [])
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


def _norm(s: str) -> list[str]:
    ascii_ = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return [t for t in "".join(c if c.isalnum() else " " for c in ascii_).lower().split()]


def _bare_orcid(author: dict) -> str | None:
    o = author.get("orcid")
    return o.rstrip("/").split("/")[-1] if o else None


def _affiliation(author: dict) -> str | None:
    inst = author.get("last_known_institutions")
    if inst:
        return inst[0].get("display_name")
    return (author.get("last_known_institution") or {}).get("display_name")


def openalex_find_author(name: str) -> dict | None:
    """Best candidate author for a name.

    Only considers records whose display name shares the query's last name
    (avoids the EPFL-affiliated-but-wrong-person trap), then prefers records
    that carry an ORCID and have the most works (the primary author cluster,
    not a sparse duplicate).
    """
    payload = _openalex_get(
        "authors", {"search": name, "per-page": 10, "mailto": MAILTO}
    )
    results = payload.get("results", [])
    if not results:
        return None

    q = _norm(name)
    q_last = q[-1] if q else ""
    matched = [a for a in results if q_last in _norm(a.get("display_name") or "")]
    pool = matched or results

    def _is_epfl(a: dict) -> bool:
        aff = (_affiliation(a) or "").upper()
        return "LAUSANNE" in aff or "EPFL" in aff

    # among same-last-name records: prefer EPFL, then having an ORCID, then the
    # primary (most-published) cluster over sparse duplicates
    pool.sort(
        key=lambda a: (_is_epfl(a), a.get("orcid") is not None, a.get("works_count") or 0),
        reverse=True,
    )
    chosen = pool[0]
    return {
        "id": chosen.get("id"),
        "orcid": _bare_orcid(chosen),
        "display_name": chosen.get("display_name"),
        "works_count": chosen.get("works_count"),
        "affiliation": _affiliation(chosen),
    }
