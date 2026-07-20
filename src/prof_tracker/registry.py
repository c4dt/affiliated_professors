"""Load/save professors.yaml and pick the rotation target."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse

import yaml

from .models import Professor

DEFAULT_REGISTRY = Path("professors.yaml")


def load_registry(path: Path = DEFAULT_REGISTRY) -> list[Professor]:
    if not path.exists():
        return []
    raw = yaml.safe_load(path.read_text()) or []
    return [Professor.model_validate(_normalize(e)) for e in raw]


def _normalize(entry: dict) -> dict:
    """Coerce dates to ISO strings and migrate legacy single-URL fields to lists."""
    entry = dict(entry)
    lu = entry.get("last_updated")
    if lu is not None and not isinstance(lu, str):
        entry["last_updated"] = lu.isoformat()

    # legacy: lab_url (str) -> lab_urls (list); github_org (slug) -> code_urls (list)
    if "lab_url" in entry and "lab_urls" not in entry:
        lab_url = entry.pop("lab_url")
        entry["lab_urls"] = [lab_url] if lab_url else []
    if "github_org" in entry and "code_urls" not in entry:
        org = entry.pop("github_org")
        entry["code_urls"] = [f"https://github.com/{org}"] if org else []

    # legacy: flat urls (list) -> epfl_profile (people.epfl.ch) + lab_urls (rest)
    if "urls" in entry and "epfl_profile" not in entry:
        urls = entry.pop("urls") or []
        epfl = next(
            (u for u in urls if urlparse(u).netloc == "people.epfl.ch"), ""
        )
        entry["epfl_profile"] = epfl
        entry.setdefault("lab_urls", [u for u in urls if u != epfl])
    return entry


def save_registry(profs: list[Professor], path: Path = DEFAULT_REGISTRY) -> None:
    # sort by name (same key as the PROFESSORS.md index) so the two stay in sync
    ordered = sorted(profs, key=lambda p: p.name.lower())
    data = [p.model_dump() for p in ordered]
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100)
    )
    _prettier_format(path)


def _prettier_format(path: Path) -> None:
    """Best-effort: canonicalize the file with Prettier (default settings) so
    generated writes match editors that format YAML with Prettier (e.g. Zed) and
    don't churn the diff. No-op if prettier isn't on PATH."""
    if shutil.which("prettier") is None:
        return
    try:
        subprocess.run(
            ["prettier", "--write", str(path)], check=True, capture_output=True
        )
    except Exception:  # noqa: BLE001 - formatting is cosmetic, never fail a run
        pass


def pick_least_recently_updated(profs: list[Professor]) -> Professor | None:
    """Never-updated professors (last_updated is None) come first; then the
    oldest last_updated. Ties broken by slug for determinism. Retired
    professors are excluded from the rotation entirely."""
    active = [p for p in profs if not p.retired]
    if not active:
        return None
    return min(
        active,
        key=lambda p: (p.last_updated is not None, p.last_updated or "", p.slug),
    )


def get_by_slug(profs: list[Professor], slug: str) -> Professor | None:
    return next((p for p in profs if p.slug == slug), None)
