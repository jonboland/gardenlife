import pytest

import context
from creature import Creature


@pytest.fixture
def test_creature():
    return Creature("mammal", "badger", "03/07/2020", 3, "positive", "low", "stable")


def test_trend_increasing(test_creature):
    test_creature.change_level("trend", "increase")
    assert test_creature.trend == "increasing"


def test_trend_already_rapidly_increasing(test_creature, capsys):
    for x in range(3):
        test_creature.change_level("trend", "increase")
    captured = capsys.readouterr()
    assert captured.out == "trend already set to rapidly increasing\n"


def test_prevalence_very_low(test_creature):
    test_creature.change_level("prevalence", "decrease")
    assert test_creature.prevalence == "very low"


def test_impact_already_very_negative(test_creature, capsys):
    for x in range(4):
        test_creature.change_level("impact", "decrease")
    captured = capsys.readouterr()
    assert captured.out == "impact already set to very negative\n"


def test_invalid_impact_level(test_creature):
    with pytest.raises(ValueError) as excinfo:
        test_creature.impact = "high"
    assert "high is not a valid impact level" in str(excinfo.value)


def test_invalid_direction(test_creature):
    with pytest.raises(ValueError) as excinfo:
        test_creature.change_level("prevalence", "blank")
    assert "blank is not a valid direction" in str(excinfo.value)


def test_date_appeared(test_creature):
    assert test_creature.appeared == "03/07/2020"


if __name__ == "__main__":
    pytest.main()
