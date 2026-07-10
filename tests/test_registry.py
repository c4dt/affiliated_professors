from prof_tracker.models import Professor
from prof_tracker.registry import (
    load_registry,
    pick_least_recently_updated,
    save_registry,
)


def _profs():
    return [
        Professor(slug="a", name="A", last_updated="2026-06-01"),
        Professor(slug="b", name="B", last_updated=None),
        Professor(slug="c", name="C", last_updated="2026-05-15"),
    ]


def test_never_updated_comes_first():
    assert pick_least_recently_updated(_profs()).slug == "b"


def test_oldest_when_all_updated():
    profs = [
        Professor(slug="a", name="A", last_updated="2026-06-01"),
        Professor(slug="c", name="C", last_updated="2026-05-15"),
    ]
    assert pick_least_recently_updated(profs).slug == "c"


def test_tie_broken_by_slug():
    profs = [
        Professor(slug="z", name="Z", last_updated=None),
        Professor(slug="a", name="A", last_updated=None),
    ]
    assert pick_least_recently_updated(profs).slug == "a"


def test_empty_registry():
    assert pick_least_recently_updated([]) is None


def test_legacy_fields_migrate_to_lists(tmp_path):
    path = tmp_path / "professors.yaml"
    path.write_text(
        "- slug: bryan-ford\n"
        "  name: Bryan Ford\n"
        "  lab_url: https://dedis.epfl.ch/\n"
        "  github_org: dedis\n"
    )
    p = load_registry(path)[0]
    assert p.urls == ["https://dedis.epfl.ch/"]
    assert p.code_urls == ["https://github.com/dedis"]


def test_save_sorts_by_name(tmp_path):
    path = tmp_path / "professors.yaml"
    save_registry(
        [
            Professor(slug="zoe", name="Zoe Z"),
            Professor(slug="amy", name="amy a"),  # lowercase -> case-insensitive
            Professor(slug="bob", name="Bob B"),
        ],
        path,
    )
    assert [p.name for p in load_registry(path)] == ["amy a", "Bob B", "Zoe Z"]


def test_roundtrip_and_date_coercion(tmp_path):
    path = tmp_path / "professors.yaml"
    save_registry(_profs(), path)
    # simulate YAML that parsed a bare date into datetime.date
    text = path.read_text().replace("last_updated: '2026-06-01'", "last_updated: 2026-06-01")
    path.write_text(text)
    loaded = load_registry(path)
    a = next(p for p in loaded if p.slug == "a")
    assert a.last_updated == "2026-06-01"
    assert isinstance(a.last_updated, str)
