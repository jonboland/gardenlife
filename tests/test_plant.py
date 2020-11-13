import pytest

import context
from organisms import Plant


@pytest.fixture
def sunflower():
    return Plant("flower", "sunflower", planted="01/05/2020")


def test_trend_decreasing(sunflower):
    sunflower.change_level("trend", "decrease")
    assert sunflower.trend == "decreasing"


def test_trend_already_rapidly_decreasing(sunflower, capsys):
    for x in range(3):
        sunflower.change_level("trend", "decrease")
    captured = capsys.readouterr()
    assert captured.out == "trend already set to rapidly decreasing\n"

def test_prevalence_high(sunflower):
    sunflower.change_level("prevalence", "increase")
    assert sunflower.prevalence == "high"


def test_impact_already_very_positive(sunflower, capsys):
    for x in range(3):
        sunflower.change_level("impact", "increase")
    captured = capsys.readouterr()
    assert captured.out == "impact already set to very positive\n"


def test_invalid_trend_level(sunflower):
    with pytest.raises(ValueError) as excinfo:
        sunflower.trend = "neutral"
    assert "neutral is not a valid trend level" in str(excinfo.value)


def test_invalid_direction(sunflower):
    with pytest.raises(ValueError) as excinfo:
        sunflower.change_level("impact", "blank")
    assert "blank is not a valid direction" in str(excinfo.value)


def test_date_appeared(sunflower):
    assert sunflower.planted == "01/05/2020"

def test_current(sunflower):
    assert sunflower.status.status == "current"

def test_archived(sunflower):
    sunflower.status.archive()
    assert sunflower.status.status == "archived"

def test_invalid_status(sunflower):
    with pytest.raises(ValueError) as excinfo:
        sunflower.status.status = "fishing"
    assert "fishing is not a valid status" in str(excinfo.value)


if __name__ == "__main__":
    pytest.main()
