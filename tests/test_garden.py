import pytest

import context
import garden
import organisms
import task


@pytest.fixture
def shade():
    return garden.Garden("Shade", "Hull", 1, "04/02/1987", "Dave Davidson")


@pytest.fixture
def badger():
    return organisms.Creature(
        "badger",
        "mammal",
        "03/07/2020",
        "Digs holes in various parts of the garden.",
        10,
        3,
        2,
        4,
    )


def test_one_owner(shade):
    assert shade.ownership() == "Dave Davidson"


def test_two_owners():
    light = garden.Garden(
        "Light", "London", 0.2, "13/11/2017", "Paul Daniels", "Ruby Wilson"
    )
    assert light.ownership() == "Paul Daniels and Ruby Wilson"


def test_three_owners_from_string():
    string_garden = garden.Garden.from_string(
        "Bell-Cranleigh-0.1-24/04/2009-Mary Jones-Greg Jones-Spot"
    )
    assert (
        string_garden.ownership()
        == "Mary Jones, Greg Jones and Spot"
    )


def test_ownership_lenght_less_than_two_years(shade):
    assert (
        shade.ownership_length("25/01/1989")
        == "721 days"
    )


def test_ownership_lenght_over_17_years(shade):
    assert (
        shade.ownership_length("22/03/2004")
        == "6,256 days (around 17 years)"
    )


def test_ownership_lenght_around_33_and_a_half_year(shade):
    assert (
        shade.ownership_length("22/07/2020")
        == "12,222 days (around 33.5 years)"
    )


def test_ownership_lenght_nearly_40_years(shade):
    assert (
        shade.ownership_length("01/01/2027")
        == "14,576 days (around 40 years)"
    )


def test_ownership_lenght_one_day(shade):
    assert (
        shade.ownership_length("05/02/1987")
        == "1 day"
    )


def test_ownership_lenght_zero_days():
    new_shade = garden.Garden(
        "New Shade", "Bath", 0.7, garden.strftime("%d/%m/%Y"), "Paul Daniels"
    )
    assert (
        new_shade.ownership_length()
        == "0 days"
    )


def test_season_current(shade):
    seasons = ("Spring", "Summer", "Autumn", "Winter")
    assert shade.season() in seasons


def test_season_specified(shade):
    seasons = ("Spring", "Summer", "Autumn", "Winter")
    assert shade.season("December") == "Winter"


def test_add_item_valueerror(shade, badger):
    with pytest.raises(ValueError) as excinfo:
        shade.add_item("animals", badger)
    assert str(excinfo.value) == "animals is not a valid category"


def test_add_item_creature(shade, badger):
    shade.add_item("creatures", badger)
    assert shade.creatures["badger"] == badger


def test_add_item_plant(shade):
    carrot = organisms.Plant("carrot", "vegetable", notes="In upper veg patch.")
    shade.add_item("plants", carrot)
    assert shade.plants["carrot"] == carrot


def test_add_item_task(shade):
    cut_hedges = task.Task("cut hedges", "01/05/2020")
    shade.add_item("tasks", cut_hedges)
    assert shade.tasks["cut hedges"] == cut_hedges

def test_str_representation(shade):
    assert str(shade) == "Garden in Hull called Shade, which is approximately 1 acre in size."


if __name__ == "__main__":
    pytest.main()
