"""Render professor markdown files and the README index.

Code owns the file structure; the model only supplies today's content. This
keeps the LLM from rewriting history and keeps diffs clean.
"""

from __future__ import annotations

import re
from pathlib import Path

from .models import Professor, ProfileUpdate, profile_filename

PROFESSORS_DIR = Path("professors")
README = Path("README.md")

_CHANGELOG_HEADER = "## Changelog"
_ENTRY_RE = re.compile(r"^### (\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)


def _split_changelog(existing: str) -> list[tuple[str, str]]:
    """Parse the changelog section of an existing profile into
    [(date, body), ...] in file order (newest first)."""
    idx = existing.find(_CHANGELOG_HEADER)
    if idx == -1:
        return []
    section = existing[idx + len(_CHANGELOG_HEADER):]
    matches = list(_ENTRY_RE.finditer(section))
    entries: list[tuple[str, str]] = []
    for i, m in enumerate(matches):
        date = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(section)
        entries.append((date, section[start:end].strip("\n")))
    return entries


def _render_changelog(entries: list[tuple[str, str]]) -> str:
    parts = [_CHANGELOG_HEADER, ""]
    for date, body in entries:
        parts.append(f"### {date}")
        parts.append("")
        if body.strip():
            parts.append(body.strip())
            parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def build_profile(
    prof: Professor, update: ProfileUpdate, today: str, existing: str = ""
) -> str:
    """Rebuild the header + summary + links from current data, then prepend
    today's changelog entry above the preserved old entries (idempotent per
    day: an existing entry for `today` is replaced)."""
    lines = [f"# {prof.name}", ""]
    if prof.lab:
        lab = f"[{prof.lab}]({prof.lab_url})" if prof.lab_url else prof.lab
        lines.append(f"**Lab:** {lab}")
    if prof.github_org:
        lines.append(f"**GitHub:** [{prof.github_org}](https://github.com/{prof.github_org})")
    if prof.openalex_id:
        lines.append(f"**OpenAlex:** [{prof.openalex_id}](https://openalex.org/{prof.openalex_id})")
    lines.append("")

    if update.one_sentence_summary:
        lines.append(update.one_sentence_summary)
        lines.append("")

    if update.important_links:
        lines.append("## Key research")
        lines.append("")
        for link in update.important_links:
            lines.append(f"- [{link.title}]({link.url})")
        lines.append("")

    entries = [(d, b) for (d, b) in _split_changelog(existing) if d != today]
    entries.insert(0, (today, update.changelog_entry.strip()))

    return "\n".join(lines).rstrip() + "\n\n" + _render_changelog(entries)


def write_profile(
    prof: Professor,
    update: ProfileUpdate,
    today: str,
    professors_dir: Path = PROFESSORS_DIR,
) -> Path:
    professors_dir.mkdir(parents=True, exist_ok=True)
    path = professors_dir / profile_filename(prof.slug)
    existing = path.read_text() if path.exists() else ""
    path.write_text(build_profile(prof, update, today, existing))
    return path


def build_readme(profs: list[Professor]) -> str:
    lines = [
        "# C4DT Affiliated Professors",
        "",
        "Research tracker for C4DT's affiliated professors. Each weekday an "
        "automated agent refreshes the least-recently-updated professor from "
        "their lab site, GitHub org, and publication feed.",
        "",
        "## Professors",
        "",
    ]
    for prof in sorted(profs, key=lambda p: p.name.lower()):
        fname = profile_filename(prof.slug)
        lines.append(f"### [{prof.name}](professors/{fname})")
        meta = prof.lab or ""
        updated = prof.last_updated or "—"
        lines.append(f"*{meta}* · last updated {updated}" if meta else f"last updated {updated}")
        lines.append("")
        body = prof.readme_paragraph or prof.one_sentence_summary
        if body:
            lines.append(body)
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def regen_readme(profs: list[Professor], path: Path = README) -> None:
    path.write_text(build_readme(profs))
