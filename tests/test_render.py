from prof_tracker.models import Link, Professor, ProfileUpdate
from prof_tracker.render import (
    build_professors_md,
    build_profile,
    write_profile,
)


def _prof():
    return Professor(
        slug="bryan-ford",
        name="Bryan Ford",
        lab="DEDIS",
        urls=["https://dedis.epfl.ch/", "https://bford.info/"],
        code_urls=["https://github.com/dedis"],
        orcid="0000-0002-0528-3033",
        openalex_id="A5000000000",
        last_updated="2026-07-10",
        reviewed=True,
    )


def _update(entry="- did a thing"):
    return ProfileUpdate(
        one_sentence_summary="Builds decentralized systems.",
        important_links=[Link(title="DEDIS", url="https://dedis.epfl.ch/")],
        changelog_entry=entry,
        significant=True,
        matrix_summary="New paper.",
    )


def test_profile_has_header_and_links():
    out = build_profile(_prof(), _update(), "2026-07-10")
    assert out.startswith("# Bryan Ford")
    assert "**Lab:** DEDIS" in out
    assert "[dedis.epfl.ch](https://dedis.epfl.ch/)" in out
    assert "[bford.info](https://bford.info/)" in out  # multiple urls
    assert "https://github.com/dedis" in out
    assert "[0000-0002-0528-3033](https://orcid.org/0000-0002-0528-3033)" in out
    assert "## Key research" in out
    assert "### 2026-07-10" in out


def test_changelog_prepends_and_preserves_history():
    existing = build_profile(_prof(), _update("- first entry"), "2026-06-01")
    updated = build_profile(_prof(), _update("- second entry"), "2026-07-10", existing)
    # newest on top
    assert updated.index("### 2026-07-10") < updated.index("### 2026-06-01")
    # old content preserved verbatim
    assert "- first entry" in updated
    assert "- second entry" in updated


def test_stray_empty_and_duplicate_headers_are_collapsed():
    # simulate a profile whose changelog got a stray empty today header + a dup
    existing = (
        "# Bryan Ford\n\n## Changelog\n\n"
        "### 2026-07-10\n\n"                       # stray empty
        "### 2026-07-10\n\n- real body\n\n"        # duplicate date, has body
        "### 2026-06-01\n\n- older\n"
    )
    out = build_profile(_prof(), _update("- new body"), "2026-07-10", existing)
    assert out.count("### 2026-07-10") == 1
    assert out.count("### 2026-06-01") == 1
    assert "- new body" in out and "- older" in out


def test_same_day_rerun_replaces_entry():
    existing = build_profile(_prof(), _update("- old body"), "2026-07-10")
    rerun = build_profile(_prof(), _update("- new body"), "2026-07-10", existing)
    assert rerun.count("### 2026-07-10") == 1
    assert "- new body" in rerun
    assert "- old body" not in rerun


def test_write_profile_uppercase_filename(tmp_path):
    path = write_profile(_prof(), _update(), "2026-07-10", tmp_path)
    assert path.name == "BRYAN-FORD.md"
    assert path.exists()


def test_readme_lists_professors_sorted(tmp_path):
    profs = [
        Professor(slug="zoe", name="Zoe Z", lab="LabZ", last_updated="2026-01-01"),
        Professor(slug="amy", name="Amy A", lab="LabA"),
    ]
    # the index reads each summary from the profile file, not the registry
    (tmp_path / "AMY.md").write_text("# Amy A\n\n**Lab:** LabA\n\nDoes A.\n\n## Changelog\n")
    out = build_professors_md(profs, tmp_path)
    assert out.index("Amy A") < out.index("Zoe Z")
    assert "professors/AMY.md" in out
    assert "Does A." in out                 # summary pulled from AMY.md
    assert "last updated —" in out          # amy never updated


def test_readme_shows_verification_links_even_when_unreviewed(tmp_path):
    profs = [
        Professor(
            slug="amy",
            name="Amy A",
            lab="LabA",
            urls=["https://laba.example/", "https://amy.example/"],
            code_urls=["https://github.com/amy"],
            orcid="0000-0000-0000-0001",
            openalex_id="A5001",
            reviewed=False,
        )
    ]
    out = build_professors_md(profs, tmp_path)  # no profile file yet
    assert "⬜ unreviewed" in out
    assert "[laba.example](https://laba.example/)" in out
    assert "[amy.example](https://amy.example/)" in out
    assert "[github.com/amy](https://github.com/amy)" in out
    assert "[ORCID 0000-0000-0000-0001](https://orcid.org/0000-0000-0000-0001)" in out
    assert "[OpenAlex A5001](https://openalex.org/A5001)" in out


def test_extract_summary_ignores_header_and_metadata():
    from prof_tracker.render import _extract_summary

    text = "# Amy A\n\n**Lab:** LabA\n**Web:** [x](https://x)\n\nDoes A things.\n\n## Key research\n\n- [a](https://b)\n"
    assert _extract_summary(text) == "Does A things."


def test_fallback_update_preserves_existing_summary_and_links():
    from prof_tracker.models import ProfileUpdate

    existing = build_profile(_prof(), _update("- first"), "2026-06-01")
    empty = ProfileUpdate(
        one_sentence_summary="",
        important_links=[],
        changelog_entry="- sources unavailable",
        significant=False,
        matrix_summary="",
    )
    out = build_profile(_prof(), empty, "2026-07-10", existing)
    assert "Builds decentralized systems." in out  # summary preserved
    assert "## Key research" in out                 # links preserved
    assert "[DEDIS](https://dedis.epfl.ch/)" in out
    assert "- sources unavailable" in out
