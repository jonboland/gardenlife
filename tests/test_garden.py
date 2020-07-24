import pytest

import context
from garden import Garden


@pytest.fixture
def test_garden():
    return Garden("Shade", "Hull", 1, "04/02/1987", "Dave Davidson")


def test_one_owner(test_garden):
    assert test_garden.ownership() == "The owner of Shade is Dave Davidson."


def test_two_owners():
    garden_two = Garden(
        "Garden Two", "London", 0.2, "13/11/2017", "Paul Daniels", "Ruby Wilson"
    )
    assert (
        garden_two.ownership()
        == "The owners of Garden Two are Paul Daniels and Ruby Wilson."
    )


def test_three_owners_from_string():
    string_garden = Garden.from_string(
        "Bell-Cranleigh-0.1-24/04/2009-Mary Jones-Greg Jones-Spot"
    )
    assert (
        string_garden.ownership()
        == "The owners of Bell are Mary Jones, Greg Jones and Spot."
    )

def test_ownership_lenght_less_than_2_years(test_garden):
    assert (
        test_garden.ownership_length("1989-01-25")
        == "Shade has been in the same hands for 721 days."
    )


def test_ownership_lenght_over_17_years(test_garden):
    assert (
        test_garden.ownership_length("2004-03-22")
        == "Shade has been in the same hands for 6,256 days.\nThat's around 17 years."
    )


def test_ownership_lenght_around_33_and_a_half_year(test_garden):
    assert (
        test_garden.ownership_length("2020-07-22")
        == "Shade has been in the same hands for 12,222 days.\nThat's around 33.5 years."
    )


def test_ownership_lenght_nearly_40_years(test_garden):
    assert (
        test_garden.ownership_length("2027-01-01")
        == "Shade has been in the same hands for 14,576 days.\nThat's around 40 years."
    )


def test_season_current(test_garden):
    seasons = ("Spring", "Summer", "Autumn", "Winter")
    assert test_garden.season() in seasons


def test_season_specified(test_garden):
    seasons = ("Spring", "Summer", "Autumn", "Winter")
    assert test_garden.season("December") == "Winter"


if __name__ == "__main__":
    pytest.main()
