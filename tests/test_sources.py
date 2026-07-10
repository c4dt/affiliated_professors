import pytest

from prof_tracker.models import Professor
from prof_tracker.sources import _norm, github_org_from_url, works_filter


def test_github_org_from_url():
    assert github_org_from_url("https://github.com/dedis") == "dedis"
    assert github_org_from_url("https://github.com/dedis/kyber") == "dedis"
    assert github_org_from_url("https://gitlab.com/foo") is None
    assert github_org_from_url("https://example.com/") is None


def test_works_filter_prefers_orcid():
    f = works_filter(openalex_id="A123", orcid="0000-0003-1579-5558")
    assert f == "authorships.author.orcid:https://orcid.org/0000-0003-1579-5558"


def test_works_filter_accepts_full_orcid_url():
    f = works_filter(orcid="https://orcid.org/0000-0003-1579-5558")
    assert f == "authorships.author.orcid:https://orcid.org/0000-0003-1579-5558"


def test_works_filter_falls_back_to_openalex_id():
    assert works_filter(openalex_id="A123") == "authorships.author.id:A123"


def test_works_filter_needs_one_anchor():
    with pytest.raises(ValueError):
        works_filter()


def test_norm_strips_accents_and_punctuation():
    assert _norm("Rüdiger Urbanke") == ["rudiger", "urbanke"]
    assert _norm("Jean-Pierre Hubaux") == ["jean", "pierre", "hubaux"]


def test_professor_has_orcid_field():
    p = Professor(slug="x", name="X", orcid="0000-0000-0000-0000")
    assert p.orcid == "0000-0000-0000-0000"
    assert Professor(slug="y", name="Y").orcid is None
