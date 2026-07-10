from prof_tracker.models import Link, Professor, ProfileUpdate
from prof_tracker.render import (
    build_profile,
    build_readme,
    write_profile,
)


def _prof():
    return Professor(
        slug="bryan-ford",
        name="Bryan Ford",
        lab="DEDIS",
        lab_url="https://dedis.epfl.ch/",
        github_org="dedis",
        openalex_id="A5000000000",
        readme_paragraph="Works on decentralized systems.",
        last_updated="2026-07-10",
    )


def _update(entry="- did a thing"):
    return ProfileUpdate(
        one_sentence_summary="Builds decentralized systems.",
        important_links=[Link(title="DEDIS", url="https://dedis.epfl.ch/")],
        changelog_entry=entry,
        significant=True,
        matrix_summary="New paper.",
        readme_paragraph="Works on decentralized systems.",
    )


def test_profile_has_header_and_links():
    out = build_profile(_prof(), _update(), "2026-07-10")
    assert out.startswith("# Bryan Ford")
    assert "[DEDIS](https://dedis.epfl.ch/)" in out
    assert "https://github.com/dedis" in out
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


def test_readme_lists_professors_sorted():
    profs = [
        Professor(slug="zoe", name="Zoe Z", lab="LabZ", last_updated="2026-01-01"),
        Professor(slug="amy", name="Amy A", lab="LabA", readme_paragraph="Does A."),
    ]
    out = build_readme(profs)
    assert out.index("Amy A") < out.index("Zoe Z")
    assert "professors/AMY.md" in out
    assert "Does A." in out
    assert "last updated —" in out  # amy never updated
