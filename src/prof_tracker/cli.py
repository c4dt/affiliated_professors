"""Command-line entry point: update / announce / bootstrap / regen-professors."""

from __future__ import annotations

import argparse
import datetime
import json
import logging
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

logger = logging.getLogger(__name__)


class _LevelFormatter(logging.Formatter):
    """Plain message for INFO; level prefix for WARNING+; module tag for DEBUG."""

    def format(self, record: logging.LogRecord) -> str:
        if record.levelno == logging.DEBUG:
            return f"DEBUG {record.name}: {record.getMessage()}"
        if record.levelno == logging.INFO:
            return record.getMessage()
        return f"{record.levelname}: {record.getMessage()}"


def _setup_logging(verbose: bool) -> None:
    level_env = os.environ.get("LOG_LEVEL", "").upper()
    if verbose or level_env == "DEBUG":
        level = logging.DEBUG
    elif level_env in ("INFO", "WARNING", "ERROR"):
        level = getattr(logging, level_env)
    else:
        level = logging.INFO

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(_LevelFormatter())
    root = logging.getLogger("prof_tracker")
    root.addHandler(handler)
    root.setLevel(level)


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

    web_urls = prof.all_urls()
    if web_urls:
        for url in web_urls[:3]:  # cap Firecrawl usage on the prefetch
            logger.debug("Scraping web URL: %s", url)
            try:
                md = sources.firecrawl_scrape(url)
                logger.debug("  -> %d chars", len(md))
                blocks.append(f"## Website ({url})\n\n{md[:15000]}")
                ok = True
            except Exception as e:  # noqa: BLE001
                logger.warning("Web source unavailable %s: %s", url, e)
                blocks.append(f"## Website ({url})\n\n[unavailable: {e}]")
    else:
        logger.debug("No web URLs configured for %s", prof.slug)
        blocks.append("## Website\n\n[no urls configured]")

    if prof.code_urls:
        for url in prof.code_urls[:3]:
            org = sources.github_org_from_url(url)
            logger.debug("Fetching code source: %s (org=%s)", url, org)
            try:
                if org:
                    repos = sources.github_org_repos(org)
                    logger.debug("  -> %d repos", len(repos))
                    blocks.append(
                        f"## Code — GitHub ({url})\n\n"
                        + json.dumps(repos, indent=2, default=str)
                    )
                else:
                    md = sources.firecrawl_scrape(url)
                    logger.debug("  -> %d chars", len(md))
                    blocks.append(f"## Code ({url})\n\n{md[:10000]}")
                ok = True
            except Exception as e:  # noqa: BLE001
                logger.warning("Code source unavailable %s: %s", url, e)
                blocks.append(f"## Code ({url})\n\n[unavailable: {e}]")
    else:
        logger.debug("No code URLs configured for %s", prof.slug)
        blocks.append("## Code\n\n[no code_urls configured]")

    if prof.orcid or prof.openalex_id:
        anchor = f"ORCID {prof.orcid}" if prof.orcid else f"OpenAlex {prof.openalex_id}"
        logger.debug("Fetching publications: %s", anchor)
        try:
            works = sources.openalex_recent_works(
                openalex_id=prof.openalex_id, orcid=prof.orcid
            )
            logger.debug("  -> %d works", len(works))
            blocks.append(
                f"## Recent publications ({anchor})\n\n"
                + json.dumps(works, indent=2, default=str)
            )
            ok = True
        except Exception as e:  # noqa: BLE001
            logger.warning("Publications unavailable (%s): %s", anchor, e)
            blocks.append(f"## Recent publications\n\n[unavailable: {e}]")
    else:
        logger.debug("No ORCID/OpenAlex ID configured for %s", prof.slug)
        blocks.append("## Recent publications\n\n[no orcid/openalex_id configured]")

    return "\n\n".join(blocks), ok


def _build_prompt(prof: Professor, sources_text: str, existing: str) -> str:
    existing_block = existing if existing.strip() else "[no existing profile — this is the first update]"
    urls = ", ".join(prof.all_urls()) or "n/a"
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
        logger.error("No professors in registry. Run bootstrap first.")
        return 1

    prof = get_by_slug(profs, args.slug) if args.slug else pick_least_recently_updated(profs)
    if prof is None:
        logger.error("Professor not found: %s", args.slug)
        return 1

    today = _today()
    logger.info("Updating %s (%s) for %s", prof.name, prof.slug, today)

    path = Path("professors") / profile_filename(prof.slug)
    existing = path.read_text() if path.exists() else ""
    logger.debug("Existing profile: %d chars", len(existing))

    sources_text, any_source_ok = _fetch_sources(prof)

    failed = False
    if not any_source_ok:
        logger.warning("All sources unavailable — writing fallback entry")
        update = _fallback_update(prof, "- All sources were unavailable today; no changes.")
        failed = True
    else:
        try:
            from .agent import run_update

            logger.info("Running agent to produce profile update")
            update = run_update(
                _build_prompt(prof, sources_text, existing),
                firecrawl_api_key=os.environ.get("FIRECRAWL_API_KEY"),
            )
            logger.info(
                "Agent done: significant=%s, changelog=%d chars",
                update.significant,
                len(update.changelog_entry),
            )
        except Exception as e:  # noqa: BLE001
            logger.warning("Agent run failed: %s", e)
            update = _fallback_update(prof, "- Update failed (LLM error); sources fetched but not summarized.")
            failed = True

    # write the profile (prose lives there), bump rotation state, rebuild index
    write_profile(prof, update, today)
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

    logger.info("Wrote %s; significant=%s", path, announce)
    return 1 if failed else 0


def _fallback_update(prof: Professor, changelog: str) -> ProfileUpdate:
    # empty summary/links -> build_profile preserves whatever is in the existing
    # profile file, so a failed run only appends a changelog line
    return ProfileUpdate(
        one_sentence_summary="",
        important_links=[],
        changelog_entry=changelog,
        significant=False,
        matrix_summary="",
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
    if not repo:
        repo = _github_repo_from_git_remote()
    if repo:
        return f"{server}/{repo}/blob/{branch}/{profile_path}"
    return profile_path


def _github_repo_from_git_remote() -> str | None:
    """Derive 'owner/repo' from the git remote when not running in GitHub Actions."""
    import re
    import subprocess

    try:
        remote_url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return None
    m = re.match(
        r"(?:git@github\.com:|https://github\.com/)([^/]+/[^/]+?)(?:\.git)?$",
        remote_url,
    )
    return m.group(1) if m else None


def cmd_announce(args: argparse.Namespace) -> int:
    from . import matrix

    homeserver = os.environ["MATRIX_HOMESERVER_URL"].rstrip("/")
    token = matrix.resolve_token(homeserver)
    room = matrix.resolve_room(homeserver, token, os.environ["MATRIX_ROOM_ID"])

    if not ANNOUNCEMENT.exists():
        plain = "Professor tracker: no update was run today."
        html = plain
    else:
        data = json.loads(ANNOUNCEMENT.read_text())
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
    logger.info("Posted to Matrix: %s", event_id)
    return 0


# --------------------------------------------------------------------------- #
# reformat
# --------------------------------------------------------------------------- #
def cmd_reformat(args: argparse.Namespace) -> int:
    """Re-render all professor files in-place without an LLM call.

    Preserves all existing content (summary, key research, changelog) but
    applies the current render logic — including newest-first changelog sorting.
    """
    from .render import build_profile, PROFESSORS_DIR

    profs = load_registry()
    empty = ProfileUpdate(
        one_sentence_summary="",
        important_links=[],
        changelog_entry="",
        significant=False,
        matrix_summary="",
    )
    count = 0
    for prof in profs:
        path = PROFESSORS_DIR / profile_filename(prof.slug)
        if not path.exists():
            continue
        existing = path.read_text()
        path.write_text(build_profile(prof, empty, "0000-00-00", existing))
        count += 1
    logger.info("Reformatted %d professor files.", count)
    return 0


# --------------------------------------------------------------------------- #
# regen-professors
# --------------------------------------------------------------------------- #
def cmd_regen_professors(args: argparse.Namespace) -> int:
    regen_professors_md(load_registry())
    logger.info("Regenerated PROFESSORS.md")
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
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        default=False,
        help="Enable debug logging (overrides LOG_LEVEL env var)",
    )
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

    p_reformat = sub.add_parser("reformat", help="re-render all professor files in-place (no LLM)")
    p_reformat.set_defaults(func=cmd_reformat)

    p_orcid = sub.add_parser(
        "resolve-orcids", help="fill candidate ORCIDs for human verification"
    )
    p_orcid.set_defaults(func=cmd_resolve_orcids)

    args = parser.parse_args(argv)
    _setup_logging(args.verbose)
    from dotenv import load_dotenv
    load_dotenv()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
