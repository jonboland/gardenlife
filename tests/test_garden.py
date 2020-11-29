import pytest

import context
import garden


@pytest.fixture
def shade():
    return garden.Garden("Shade", "Hull", 1, "04/02/1987", "Dave Davidson")


def test_one_owner(shade):
    assert shade.ownership() == "The owner of Shade is Dave Davidson."


def test_two_owners():
    light = garden.Garden(
        "Light", "London", 0.2, "13/11/2017", "Paul Daniels", "Ruby Wilson"
    )
    assert light.ownership() == "The owners of Light are Paul Daniels and Ruby Wilson."


def test_three_owners_from_string():
    string_garden = garden.Garden.from_string(
        "Bell-Cranleigh-0.1-24/04/2009-Mary Jones-Greg Jones-Spot"
    )
    assert (
        string_garden.ownership()
        == "The owners of Bell are Mary Jones, Greg Jones and Spot."
    )


def test_ownership_lenght_less_than_two_years(shade):
    assert (
        shade.ownership_length("25/01/1989")
        == "Shade has been in the same hands for 721 days."
    )


def test_ownership_lenght_over_17_years(shade):
    assert (
        shade.ownership_length("22/03/2004")
        == "Shade has been in the same hands for 6,256 days.\nThat's around 17 years."
    )


def test_ownership_lenght_around_33_and_a_half_year(shade):
    assert (
        shade.ownership_length("22/07/2020")
        == "Shade has been in the same hands for 12,222 days.\nThat's around 33.5 years."
    )


def test_ownership_lenght_nearly_40_years(shade):
    assert (
        shade.ownership_length("01/01/2027")
        == "Shade has been in the same hands for 14,576 days.\nThat's around 40 years."
    )


def test_ownership_lenght_one_day(shade):
    assert (
        shade.ownership_length("05/02/1987")
        == "Shade has been in the same hands for 1 day."
    )


def test_ownership_lenght_zero_days():
    new_shade = garden.Garden(
        "New Shade", "Bath", 0.7, garden.strftime("%d/%m/%Y"), "Paul Daniels"
    )
    assert (
        new_shade.ownership_length()
        == "New Shade has been in the same hands for 0 days."
    )


def test_season_current(shade):
    seasons = ("Spring", "Summer", "Autumn", "Winter")
    assert shade.season() in seasons


def test_season_specified(shade):
    seasons = ("Spring", "Summer", "Autumn", "Winter")
    assert shade.season("December") == "Winter"


if __name__ == "__main__":
    pytest.main()
