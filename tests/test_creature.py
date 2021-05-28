import pytest

import context
import organisms


@pytest.fixture
def badger():
    return organisms.Creature(
        "badger",
        "mammal",
        appeared="03/07/2020",
        notes="Digs holes in various parts of the garden.",
        age=10,
        impact=3,
        prevalence=2,
        trend=4,
    )


def test_impact_neutral(badger):
    assert badger.get_level("impact") == "Neutral"


def test_prevalence_low(badger):
    badger.prevalence = 1
    assert badger.get_level("prevalence") == "Very Low"


def test_invalid_impact_level(badger):
    with pytest.raises(ValueError) as excinfo:
        badger.impact = "high"
    assert str(excinfo.value) == "high is not a valid impact level"


def test_date_appeared(badger):
    assert badger.appeared == "03/07/2020"


def test_notes(badger):
    assert badger.notes == "Digs holes in various parts of the garden."


def test_unarchived(badger):
    badger.status.archive()
    badger.status.unarchive()
    assert badger.status.status == "Current"


if __name__ == "__main__":
    pytest.main()
