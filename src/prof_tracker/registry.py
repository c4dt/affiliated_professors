"""Load/save professors.yaml and pick the rotation target."""

from __future__ import annotations

from pathlib import Path

import yaml

from .models import Professor

DEFAULT_REGISTRY = Path("professors.yaml")


def load_registry(path: Path = DEFAULT_REGISTRY) -> list[Professor]:
    if not path.exists():
        return []
    raw = yaml.safe_load(path.read_text()) or []
    return [Professor.model_validate(_normalize(e)) for e in raw]


def _normalize(entry: dict) -> dict:
    """YAML may parse dates as datetime.date — coerce last_updated to ISO string."""
    entry = dict(entry)
    lu = entry.get("last_updated")
    if lu is not None and not isinstance(lu, str):
        entry["last_updated"] = lu.isoformat()
    return entry


def save_registry(profs: list[Professor], path: Path = DEFAULT_REGISTRY) -> None:
    data = [p.model_dump() for p in profs]
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100)
    )


def pick_least_recently_updated(profs: list[Professor]) -> Professor | None:
    """Never-updated professors (last_updated is None) come first; then the
    oldest last_updated. Ties broken by slug for determinism."""
    if not profs:
        return None
    return min(
        profs,
        key=lambda p: (p.last_updated is not None, p.last_updated or "", p.slug),
    )


def get_by_slug(profs: list[Professor], slug: str) -> Professor | None:
    return next((p for p in profs if p.slug == slug), None)
