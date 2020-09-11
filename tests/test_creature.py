import pytest

import context
from creature import Creature


@pytest.fixture
def badger():
    return Creature(
        "mammal",
        "badger",
        "03/07/2020",
        "Digs holes in various parts of the garden.",
        3,
        "positive",
        "low",
        "stable",
    )


def test_trend_increasing(badger):
    badger.change_level("trend", "increase")
    assert badger.trend == "increasing"


def test_trend_already_rapidly_increasing(badger, capsys):
    for x in range(3):
        badger.change_level("trend", "increase")
    captured = capsys.readouterr()
    assert captured.out == "trend already set to rapidly increasing\n"


def test_prevalence_very_low(badger):
    badger.change_level("prevalence", "decrease")
    assert badger.prevalence == "very low"


def test_impact_already_very_negative(badger, capsys):
    for x in range(4):
        badger.change_level("impact", "decrease")
    captured = capsys.readouterr()
    assert captured.out == "impact already set to very negative\n"


def test_invalid_impact_level(badger):
    with pytest.raises(ValueError) as excinfo:
        badger.impact = "high"
    assert "high is not a valid impact level" in str(excinfo.value)


def test_invalid_direction(badger):
    with pytest.raises(ValueError) as excinfo:
        badger.change_level("prevalence", "blank")
    assert "blank is not a valid direction" in str(excinfo.value)


def test_date_appeared(badger):
    assert badger.appeared == "03/07/2020"

def test_notes(badger):
    assert badger.notes == "Digs holes in various parts of the garden."

def test_unarchived(badger):
    badger.change_status()
    badger.change_status()
    assert badger.status == "current"


if __name__ == "__main__":
    pytest.main()
