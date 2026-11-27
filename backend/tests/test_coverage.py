from collections import Counter

from app.ingestion.coverage import load_roster, match_institution


def test_roster_complete() -> None:
    roster = load_roster()
    assert len(roster) == 87
    assert len({target.key for target in roster}) == 87
    assert Counter(target.category for target in roster) == {
        "IIT": 23,
        "NIT": 31,
        "IIIT": 25,
        "IISER": 7,
        "IISc": 1,
    }


def test_matching_rejects_wrong_campus_and_ambiguity() -> None:
    target = next(t for t in load_roster() if t.name == "IIT Delhi")
    candidate = {
        "id": "https://openalex.org/I123",
        "display_name": "Indian Institute of Technology Delhi",
        "type": "education",
        "country_code": "IN",
    }
    wrong = {**candidate, "display_name": "Indian Institute of Technology Bombay"}
    assert match_institution(target, [wrong]) is None
    assert match_institution(target, [{**candidate, "country_code": "US"}]) is None
    assert match_institution(target, [candidate]) == candidate
    assert match_institution(
        target, [candidate, {**candidate, "id": "https://openalex.org/I456"}]
    ) is None


def test_named_alias() -> None:
    target = next(t for t in load_roster() if t.name == "NIT Bhopal")
    candidate = {
        "id": "https://openalex.org/I123",
        "display_name": "Maulana Azad National Institute of Technology",
        "type": "education",
        "country_code": "IN",
    }
    assert match_institution(target, [candidate]) == candidate
