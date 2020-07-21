import pytest

import context
from garden import Garden


@pytest.fixture
def test_garden():
    return Garden(
        "Test Garden",
        "London",
        0.2,
        "13/11/2017",
        "Bob Brown",
        "Jen Brown",
        "McDougal The Cat",
    )


def test_three_owners_from_string():
    string_garden = Garden.from_string(
        "Bell-Cranleigh-0.1-24/04/2009-Mary Jones-Greg Jones-Toby"
    )
    assert (
        string_garden.ownership()
        == "The owners of Bell are Mary Jones, Greg Jones and Toby."
    )


def test_season(test_garden):
    seasons = ("Spring", "Summer", "Autumn", "Winter")
    assert test_garden.season() in seasons


if __name__ == "__main__":
    pytest.main()
