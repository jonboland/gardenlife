import pytest

import context
import organisms


@pytest.fixture
def sunflower():
    return organisms.Plant(
        name="sunflower",
        org_type="flower",
        planted="03/05/2021",
        prevalence=2,
        trend=3,
    )


def test_impact_neutral(sunflower):
    assert sunflower.get_level("impact") == "Neutral"


def test_prevalence_low(sunflower):
    sunflower.prevalence = 1
    assert sunflower.get_level("prevalence") == "Very Low"


def test_invalid_trend_level(sunflower):
    with pytest.raises(ValueError) as excinfo:
        sunflower.trend = "very positive"
    assert str(excinfo.value) == "very positive is not a valid trend level"


def test_date_appeared(sunflower):
    assert sunflower.planted == "03/05/2021"


def test_plant_repr(sunflower):
    assert repr(sunflower) == "Plant(sunflower, flower)"


def test_plant_str(sunflower):
    assert str(sunflower) == "Plant name: sunflower. Plant type: flower."


def test_current(sunflower):
    assert sunflower.status.status == "Current"


def test_archived(sunflower):
    sunflower.status.archive()
    assert sunflower.status.status == "Archived"


def test_invalid_status(sunflower):
    with pytest.raises(ValueError) as excinfo:
        sunflower.status.status = "fishing"
    assert str(excinfo.value) == "fishing is not a valid status"


if __name__ == "__main__":
    pytest.main()
