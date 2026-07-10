"""Command-line entry point: update / announce / bootstrap / regen-professors."""

from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from pathlib import Path

from .models import Professor, ProfileUpdate, profile_filename
from .registry import (
    get_by_slug,
    load_registry,
    pick_least_recently_updated,
    save_registry,
)
from .render import regen_professors_md, write_profile

RUN_DIR = Path(".run")
ANNOUNCEMENT = RUN_DIR / "announcement.json"
COMMIT_MSG = RUN_DIR / "commit-msg.txt"


def _today() -> str:
    return datetime.date.today().isoformat()


# --------------------------------------------------------------------------- #
# source fetch + prompt
# --------------------------------------------------------------------------- #
def _fetch_sources(prof: Professor) -> tuple[str, bool]:
    """Return (prompt-ready source text, any_source_ok)."""
    from . import sources

    blocks: list[str] = []
    ok = False

    if prof.urls:
        for url in prof.urls[:3]:  # cap Firecrawl usage on the prefetch
            try:
                md = sources.firecrawl_scrape(url)
                blocks.append(f"## Website ({url})\n\n{md[:15000]}")
                ok = True
            except Exception as e:  # noqa: BLE001
                blocks.append(f"## Website ({url})\n\n[unavailable: {e}]")
    else:
        blocks.append("## Website\n\n[no urls configured]")

    if prof.code_urls:
        for url in prof.code_urls[:3]:
            org = sources.github_org_from_url(url)
            try:
                if org:
                    repos = sources.github_org_repos(org)
                    blocks.append(
                        f"## Code — GitHub ({url})\n\n"
                        + json.dumps(repos, indent=2, default=str)
                    )
                else:
                    md = sources.firecrawl_scrape(url)
                    blocks.append(f"## Code ({url})\n\n{md[:10000]}")
                ok = True
            except Exception as e:  # noqa: BLE001
                blocks.append(f"## Code ({url})\n\n[unavailable: {e}]")
    else:
        blocks.append("## Code\n\n[no code_urls configured]")

    if prof.orcid or prof.openalex_id:
        anchor = f"ORCID {prof.orcid}" if prof.orcid else f"OpenAlex {prof.openalex_id}"
        try:
            works = sources.openalex_recent_works(
                openalex_id=prof.openalex_id, orcid=prof.orcid
            )
            blocks.append(
                f"## Recent publications ({anchor})\n\n"
                + json.dumps(works, indent=2, default=str)
            )
            ok = True
        except Exception as e:  # noqa: BLE001
            blocks.append(f"## Recent publications\n\n[unavailable: {e}]")
    else:
        blocks.append("## Recent publications\n\n[no orcid/openalex_id configured]")

    return "\n\n".join(blocks), ok


def _build_prompt(prof: Professor, sources_text: str, existing: str) -> str:
    existing_block = existing if existing.strip() else "[no existing profile — this is the first update]"
    urls = ", ".join(prof.urls) if prof.urls else "n/a"
    return (
        f"Professor: {prof.name}\n"
        f"Lab: {prof.lab}\n"
        f"URLs: {urls}\n\n"
        f"=== EXISTING PROFILE ===\n{existing_block}\n\n"
        f"=== FRESHLY FETCHED SOURCES ===\n{sources_text}\n"
    )


# --------------------------------------------------------------------------- #
# update
# --------------------------------------------------------------------------- #
def cmd_update(args: argparse.Namespace) -> int:
    profs = load_registry()
    if not profs:
        print("No professors in registry. Run bootstrap first.", file=sys.stderr)
        return 1

    prof = get_by_slug(profs, args.slug) if args.slug else pick_least_recently_updated(profs)
    if prof is None:
        print(f"Professor not found: {args.slug}", file=sys.stderr)
        return 1

    today = _today()
    print(f"Updating {prof.name} ({prof.slug}) for {today}", file=sys.stderr)

    path = Path("professors") / profile_filename(prof.slug)
    existing = path.read_text() if path.exists() else ""

    sources_text, any_source_ok = _fetch_sources(prof)

    failed = False
    if not any_source_ok:
        print("All sources unavailable.", file=sys.stderr)
        update = _fallback_update(prof, "- All sources were unavailable today; no changes.")
        failed = True
    else:
        try:
            from .agent import run_update

            update = run_update(
                _build_prompt(prof, sources_text, existing),
                firecrawl_api_key=os.environ.get("FIRECRAWL_API_KEY"),
            )
        except Exception as e:  # noqa: BLE001
            print(f"Agent run failed: {e}", file=sys.stderr)
            update = _fallback_update(prof, f"- Update failed (LLM error); sources fetched but not summarized.")
            failed = True

    # persist profile + registry-derived fields + professors index
    write_profile(prof, update, today)
    prof.one_sentence_summary = update.one_sentence_summary or prof.one_sentence_summary
    prof.readme_paragraph = update.readme_paragraph or prof.readme_paragraph
    prof.last_updated = today
    save_registry(profs)
    regen_professors_md(profs)

    # emit run artifacts for the workflow
    RUN_DIR.mkdir(exist_ok=True)
    announce = update.significant and not failed
    ANNOUNCEMENT.write_text(
        json.dumps(
            {
                "slug": prof.slug,
                "name": prof.name,
                "lab": prof.lab,
                "one_sentence_summary": update.one_sentence_summary,
                "matrix_summary": update.matrix_summary,
                "significant": bool(announce),
                "profile_path": f"professors/{profile_filename(prof.slug)}",
            },
            indent=2,
        )
    )
    suffix = " [sources unavailable]" if failed else ""
    COMMIT_MSG.write_text(f"Update {prof.name} ({prof.slug}) — {today}{suffix}\n")

    print(f"Wrote {path}; significant={announce}", file=sys.stderr)
    return 1 if failed else 0


def _fallback_update(prof: Professor, changelog: str) -> ProfileUpdate:
    return ProfileUpdate(
        one_sentence_summary=prof.one_sentence_summary,
        important_links=[],
        changelog_entry=changelog,
        significant=False,
        matrix_summary="",
        readme_paragraph=prof.readme_paragraph,
    )


# --------------------------------------------------------------------------- #
# announce
# --------------------------------------------------------------------------- #
def _profile_url(profile_path: str) -> str:
    repo = os.environ.get("GITHUB_REPOSITORY")
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    branch = os.environ.get("GITHUB_REF_NAME", "main")
    base = os.environ.get("PROFILE_BASE_URL")
    if base:
        return f"{base.rstrip('/')}/{profile_path}"
    if repo:
        return f"{server}/{repo}/blob/{branch}/{profile_path}"
    return profile_path


def cmd_announce(args: argparse.Namespace) -> int:
    if not ANNOUNCEMENT.exists():
        print("No announcement.json — nothing to announce.", file=sys.stderr)
        return 0
    data = json.loads(ANNOUNCEMENT.read_text())

    minor_ok = os.environ.get("MATRIX_POST_MINOR", "").lower() == "true"
    if not data.get("significant") and not minor_ok:
        print("Update not significant; skipping Matrix post.", file=sys.stderr)
        return 0

    from . import matrix

    homeserver = os.environ["MATRIX_HOMESERVER_URL"].rstrip("/")
    token = matrix.resolve_token(homeserver)
    room = matrix.resolve_room(homeserver, token, os.environ["MATRIX_ROOM_ID"])

    url = _profile_url(data["profile_path"])
    name, lab = data["name"], data.get("lab", "")
    summary = data.get("one_sentence_summary", "")
    ms = data.get("matrix_summary", "")

    plain = f"{name} ({lab}) — {summary}\n{ms}\nFull profile: {url}"
    html = (
        f"<b>{name}</b> ({lab}) — {summary}<br/>{ms}<br/>"
        f'<a href="{url}">Full profile</a>'
    )
    event_id = matrix.send_html(homeserver, token, room, plain, html)
    print(f"Posted to Matrix: {event_id}", file=sys.stderr)
    return 0


# --------------------------------------------------------------------------- #
# regen-professors
# --------------------------------------------------------------------------- #
def cmd_regen_professors(args: argparse.Namespace) -> int:
    regen_professors_md(load_registry())
    print("Regenerated PROFESSORS.md", file=sys.stderr)
    return 0


# --------------------------------------------------------------------------- #
# bootstrap
# --------------------------------------------------------------------------- #
def cmd_bootstrap(args: argparse.Namespace) -> int:
    from .bootstrap import run_bootstrap

    return run_bootstrap(start_url=args.url)


def cmd_resolve_orcids(args: argparse.Namespace) -> int:
    from .bootstrap import resolve_orcids

    return resolve_orcids()


# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="prof-tracker")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_update = sub.add_parser("update", help="update one professor")
    p_update.add_argument("--slug", default=None)
    p_update.set_defaults(func=cmd_update)

    p_announce = sub.add_parser("announce", help="post the last update to Matrix")
    p_announce.set_defaults(func=cmd_announce)

    p_boot = sub.add_parser("bootstrap", help="build professors.yaml from C4DT labs")
    p_boot.add_argument("--url", default="https://c4dt.epfl.ch/laboratory/")
    p_boot.set_defaults(func=cmd_bootstrap)

    p_regen = sub.add_parser("regen-professors", help="regenerate PROFESSORS.md")
    p_regen.set_defaults(func=cmd_regen_professors)

    p_orcid = sub.add_parser(
        "resolve-orcids", help="fill candidate ORCIDs for human verification"
    )
    p_orcid.set_defaults(func=cmd_resolve_orcids)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
