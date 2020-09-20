import datetime
import pytest

import context
from creature import Creature
from plant import Plant
from task import Task, MONTHLY


@pytest.fixture
def cut_hedges():
    task = Task(
        "cut hedges",
        "01/05/2020",
        "Cut all hedges in garden ready for Summer and Winter.",
        "Bob",
        8,
    )
    task.set_schedule(number=5, bymonth=(5, 10))
    return task


@pytest.fixture
def cut_hedges_too():
    return Task("cut hedges", "01/05/2020")


@pytest.fixture
def prune_tree():
    task = Task("prune tree", "01/07/2020", "Prune tree by front gate.", "Jill", 2)
    task.set_schedule(number=3)
    return task


def test_status_current(cut_hedges):
    assert cut_hedges.status.get() == "current"


def test_status_archived(cut_hedges):
    cut_hedges.status.archive()
    assert cut_hedges.status.get() == "archived"


def test_status_unarchived(cut_hedges):
    cut_hedges.status.archive()
    cut_hedges.status.unarchive()
    assert cut_hedges.status.get() == "current"


def test_equality_comparison_false(cut_hedges, prune_tree):
    assert (cut_hedges == prune_tree) == False


def test_equality_comparison_true(cut_hedges, cut_hedges_too):
    assert (cut_hedges == cut_hedges_too) == True


def test_set_schedule_without_start_date(prune_tree):
    prune_tree.set_schedule(number=2)
    assert prune_tree.schedule == [
        datetime.datetime(2020, 7, 1, 0, 0),
        datetime.datetime(2021, 7, 1, 0, 0),
    ]


def test_set_schedule_with_start_date(prune_tree):
    prune_tree.set_schedule("01/10/2020", MONTHLY, 4)
    assert prune_tree.schedule == [
        datetime.datetime(2020, 10, 1, 0, 0),
        datetime.datetime(2020, 11, 1, 0, 0),
        datetime.datetime(2020, 12, 1, 0, 0),
        datetime.datetime(2021, 1, 1, 0, 0),
    ]


def test_view_schedule(cut_hedges):
    assert cut_hedges.view_schedule() == [
        "01/05/2020",
        "01/10/2020",
        "01/05/2021",
        "01/10/2021",
        "01/05/2022",
    ]


def test_link_creature(cut_hedges):
    badger = Creature("mammal", "badger")
    cut_hedges.link_creature(badger)
    assert cut_hedges.creatures[0] == badger


def test_link_plant(prune_tree):
    sunflower = Plant("flower", "sunflower", planted="01/05/2020")
    prune_tree.link_plant(sunflower)
    assert prune_tree.plants[0] == sunflower


# Add Progress


def test_add_progress_completed_one_off(cut_hedges_too):
    cut_hedges_too.add_progress("completed", completed_date="03/05/2020")
    assert cut_hedges_too.progress == "completed"
    assert cut_hedges_too.completed_dates[-1] == datetime.datetime(2020, 5, 3, 0, 0)
    assert cut_hedges_too.status.get() == "archived"


def test_add_progress_completed_two_due_dates(prune_tree):
    prune_tree.set_schedule(number=2)  # Due dates: 01/07/2020, 01/07/2021
    prune_tree.add_progress("completed", completed_date="03/09/2020")
    assert prune_tree.progress == "completed"
    assert prune_tree.completed_dates[-1] == datetime.datetime(2020, 9, 3, 0, 0)
    assert prune_tree.status.get() == "current"


def test_add_progress_completed_two_due_dates_archived(prune_tree):
    prune_tree.set_schedule(number=2)  # Due dates: 01/07/2020, 01/07/2021
    prune_tree.add_progress("completed", completed_date="03/09/2021")
    assert prune_tree.progress == "completed"
    assert prune_tree.status.get() == "archived"


def test_add_progress_completed_several_due_dates(cut_hedges):
    cut_hedges.add_progress("completed", completed_date="03/05/2020")
    assert cut_hedges.progress == "completed"
    assert cut_hedges.status.get() == "current"


def test_add_progress_completed_early(cut_hedges):
    cut_hedges.add_progress("completed early", completed_date="03/04/2020")
    assert cut_hedges.progress == "completed early"
    assert cut_hedges.status.get() == "current"


def test_add_progress_in_progress(cut_hedges):
    cut_hedges.add_progress("in progress", completed_date="04/06/2021")
    assert cut_hedges.progress == "in progress"
    assert cut_hedges.completed_dates == []
    assert cut_hedges.status.get() == "current"


def test_add_progress_completed_archived(cut_hedges):
    cut_hedges.add_progress(
        "completed", completed_date="04/06/2022"
    )  # Final date: 01/05/2022
    assert cut_hedges.progress == "completed"
    assert cut_hedges.completed_dates[-1] == datetime.datetime(2022, 6, 4, 0, 0)
    assert cut_hedges.status.get() == "archived"


def test_add_progress_completed_today(prune_tree):
    prune_tree.add_progress("completed")
    assert prune_tree.completed_dates[-1] == datetime.datetime.today()


# Refresh Progress


def test_refresh_progress_one_off_task_not_due(cut_hedges_too):
    cut_hedges_too.refresh_progress("01/04/2020")  # Due 01/05/2020
    assert not cut_hedges_too.progress
    assert cut_hedges_too.status.get() == "current"


def test_refresh_progress_one_off_task_due(cut_hedges_too):
    cut_hedges_too.refresh_progress("02/07/2020")  # Due 01/05/2020
    assert cut_hedges_too.progress == "outstanding"
    assert cut_hedges_too.status.get() == "current"


def test_refresh_progress_one_off_task_completed_before_due(cut_hedges_too):
    cut_hedges_too.add_progress(
        "completed early", completed_date="01/04/2020"
    )  # Due 01/05/2020
    cut_hedges_too.refresh_progress("01/06/2020")
    assert cut_hedges_too.progress == "completed early"
    assert cut_hedges_too.status.get() == "archived"


def test_refresh_progress_one_off_task_completed_on_due(cut_hedges_too):
    cut_hedges_too.add_progress(
        "completed", completed_date="01/05/2020"
    )  # Due 01/05/2020
    cut_hedges_too.refresh_progress("01/07/2020")
    assert cut_hedges_too.progress == "completed"
    assert cut_hedges_too.status.get() == "archived"


def test_refresh_progress_one_off_task_completed_after_due(cut_hedges_too):
    cut_hedges_too.add_progress(
        "completed", completed_date="04/06/2020"
    )  # Due 01/05/2020
    cut_hedges_too.refresh_progress("01/08/2020")
    assert cut_hedges_too.progress == "completed"
    assert cut_hedges_too.status.get() == "archived"


def test_refresh_progress_completed_once_due_again(prune_tree):
    prune_tree.set_schedule(
        "01/10/2020", MONTHLY, 4
    )  # Due: 01/10/2020, 01/11/2020, 01/12/2020, 01/01/2021
    prune_tree.add_progress("completed", "05/10/2020")
    prune_tree.refresh_progress("05/11/2020")
    assert prune_tree.progress == "outstanding"
    assert prune_tree.status.get() == "current"


def test_refresh_progress_completed_twice_before_second_due(prune_tree):
    prune_tree.set_schedule("01/10/2020", MONTHLY, 4)
    prune_tree.add_progress("completed", "05/10/2020")
    prune_tree.add_progress("completed early", "28/10/2020")
    prune_tree.refresh_progress("05/11/2020")
    assert prune_tree.progress == "completed early"


def test_refresh_progress_completed_second_time_on_second_due(prune_tree):
    prune_tree.set_schedule("01/10/2020", MONTHLY, 4)
    prune_tree.add_progress("completed", "05/10/2020")
    prune_tree.add_progress("completed", "01/11/2020")
    prune_tree.refresh_progress("05/11/2020")
    assert prune_tree.progress == "completed"


def test_refresh_progress_completed_second_time_after_second_due(prune_tree):
    prune_tree.set_schedule("01/10/2020", MONTHLY, 4)
    prune_tree.add_progress("completed", "05/10/2020")
    prune_tree.add_progress("completed", "04/11/2020")
    prune_tree.refresh_progress("05/11/2020")
    assert prune_tree.progress == "completed"


def test_refresh_progress_completed_twice_due_again(prune_tree):
    prune_tree.set_schedule("01/10/2020", MONTHLY, 4)
    prune_tree.add_progress("completed", "05/10/2020")
    prune_tree.add_progress("completed early", "29/10/2020")
    prune_tree.refresh_progress("10/12/2020")
    assert prune_tree.progress == "outstanding"
    assert prune_tree.status.get() == "current"


def test_refresh_progress_completed_third_time_after_third_due(prune_tree):
    prune_tree.set_schedule("01/10/2020", MONTHLY, 4)
    prune_tree.add_progress("completed", "05/10/2020")
    prune_tree.add_progress("completed early", "29/10/2020")
    prune_tree.add_progress("completed", "02/12/2020")
    prune_tree.refresh_progress("10/12/2020")
    assert prune_tree.progress == "completed"


def test_refresh_progress_completed_once_due_again_in_progress(prune_tree):
    prune_tree.set_schedule(
        "01/10/2020", MONTHLY, 4
    )  # Due: 01/10/2020, 01/11/2020, 01/12/2020, 01/01/2021
    prune_tree.add_progress("completed", "05/10/2020")
    prune_tree.add_progress("in progress")
    prune_tree.refresh_progress("05/11/2020")
    assert prune_tree.progress == "in progress"


def test_refresh_progress_completed_once_third_due_reached_in_progress(prune_tree):
    prune_tree.set_schedule("01/10/2020", MONTHLY, 4)
    prune_tree.add_progress("completed", "05/10/2020")
    prune_tree.add_progress("in progress")
    prune_tree.refresh_progress("05/12/2020")
    assert prune_tree.progress == "outstanding"


def test_refresh_progress_completed_twice_third_due_reached_completed_early(prune_tree):
    prune_tree.set_schedule("01/10/2020", MONTHLY, 4)
    prune_tree.add_progress("completed", "05/10/2020")
    prune_tree.add_progress("completed early", "30/10/2020")
    prune_tree.refresh_progress("05/12/2020")
    assert prune_tree.progress == "outstanding"
    assert prune_tree.status.get() == "current"


def test_refresh_progress_completed_every_time(prune_tree):
    prune_tree.set_schedule("01/10/2020", MONTHLY, 4)
    prune_tree.add_progress("completed", "05/10/2020")
    prune_tree.add_progress("completed early", "30/10/2020")
    prune_tree.add_progress("completed", "06/12/2020")
    prune_tree.add_progress("completed", "03/01/2021")
    prune_tree.refresh_progress("08/01/2021")
    assert prune_tree.progress == "completed"
    assert prune_tree.status.get() == "archived"


def test_refresh_progress_completed_three_times_last_due_reached(prune_tree):
    prune_tree.set_schedule("01/10/2020", MONTHLY, 4)
    prune_tree.add_progress("completed", "05/10/2020")
    prune_tree.add_progress("completed early", "30/10/2020")
    prune_tree.add_progress("completed", "06/12/2020")
    prune_tree.refresh_progress("08/01/2021")
    assert prune_tree.progress == "outstanding"
    assert prune_tree.status.get() == "current"


def test_refresh_progress_completed_every_time_completed_early(prune_tree):
    prune_tree.set_schedule("01/10/2020", MONTHLY, 4)
    prune_tree.add_progress("completed", "05/10/2020")
    prune_tree.add_progress("completed early", "30/10/2020")
    prune_tree.add_progress("completed", "06/12/2020")
    prune_tree.add_progress("completed early", "31/12/2020")
    prune_tree.refresh_progress("08/01/2021")
    assert prune_tree.progress == "completed early"
    assert prune_tree.status.get() == "archived"


def test_refresh_progress_completed_twice_last_due_reached_in_progress(prune_tree):
    prune_tree.set_schedule(
        "01/10/2020", MONTHLY, 4
    )  # Due: 01/10/2020, 01/11/2020, 01/12/2020, 01/01/2021
    prune_tree.add_progress("completed", "05/10/2020")
    prune_tree.add_progress("completed early", "30/10/2020")
    prune_tree.add_progress("in progress")
    prune_tree.refresh_progress("08/01/2021")
    assert prune_tree.progress == "outstanding"


def test_refresh_progress_completed_three_times_last_due_reached_in_progress(prune_tree):
    prune_tree.set_schedule("01/10/2020", MONTHLY, 4)
    prune_tree.add_progress("completed", "05/10/2020")
    prune_tree.add_progress("completed early", "30/10/2020")
    prune_tree.add_progress("completed", "13/12/2020")
    prune_tree.add_progress("in progress")
    prune_tree.refresh_progress("08/01/2021")
    assert prune_tree.progress == "in progress"
    assert prune_tree.status.get() == "current"


if __name__ == "__main__":
    pytest.main()
