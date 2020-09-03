import pytest

import context
from plant import Plant


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


def test_date_appeared(sunflower):
    assert sunflower.planted == "01/05/2020"


if __name__ == "__main__":
    pytest.main()
