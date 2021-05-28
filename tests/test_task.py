from datetime import datetime
import pytest
import time

import context
from task import Task


@pytest.fixture
def cut_hedges():
    task = Task(
        name="cut hedges",
        description="Cut all hedges in garden ready for Summer and Winter.",
        assignee="Bob",
        length="8",
    )
    task.set_schedule(
        freq="monthly", start_date="01/05/2020", count="5", bymonth="5 10", interval=1
    )
    return task


@pytest.fixture
def cut_hedges_too():
    task = Task("cut hedges")
    task.set_schedule(
        freq="", start_date="01/05/2020", count="", bymonth="", interval=1
    )
    return task


@pytest.fixture
def prune_tree():
    task = Task("prune tree", "Prune tree by front gate.", "Jill", "2")
    return task


# Status


def test_status_current(cut_hedges):
    assert cut_hedges.status.get() == "Current"


def test_status_archived(cut_hedges):
    cut_hedges.status.archive()
    assert cut_hedges.status.get() == "Archived"


def test_status_unarchived(cut_hedges):
    cut_hedges.status.archive()
    cut_hedges.status.unarchive()
    assert cut_hedges.status.get() == "Current"


# Equality


def test_equality_comparison_false(cut_hedges, prune_tree):
    assert (cut_hedges == prune_tree) == False


def test_equality_comparison_true(cut_hedges, cut_hedges_too):
    assert (cut_hedges == cut_hedges_too) == True


# Set schedule


def test_set_schedule_without_start_date(prune_tree):
    prune_tree.set_schedule(start_date="", freq="", count="", bymonth="", interval="")
    assert prune_tree.schedule[0].strftime("%d/%m/%Y") == time.strftime("%d/%m/%Y")


def test_set_schedule_with_start_date(prune_tree):
    prune_tree.set_schedule(
        start_date="01/10/2020", freq="monthly", count="4", bymonth="", interval=""
    )
    assert prune_tree.schedule == [
        datetime(2020, 10, 1, 0, 0),
        datetime(2020, 11, 1, 0, 0),
        datetime(2020, 12, 1, 0, 0),
        datetime(2021, 1, 1, 0, 0),
    ]


# Add completed dates


def test_add_one_completed_date(cut_hedges):
    scheduled_dates = {
        "01/05/2020": True,
        "01/10/2020": False,
        "01/05/2021": False,
        "01/10/2021": False,
        "01/05/2022": False,
    }
    cut_hedges.update_completed_dates(scheduled_dates)
    assert cut_hedges.completed_dates == [datetime(2020, 5, 1, 0, 0)]


def test_add_two_completed_date(cut_hedges):
    scheduled_dates = {
        "01/05/2020": True,
        "01/10/2020": False,
        "01/05/2021": True,
        "01/10/2021": False,
        "01/05/2022": False,
    }
    cut_hedges.update_completed_dates(scheduled_dates)
    assert cut_hedges.completed_dates == [
        datetime(2020, 5, 1, 0, 0),
        datetime(2021, 5, 1, 0, 0),
    ]


def test_add_same_two_completed_date_twice(cut_hedges):
    scheduled_dates = {
        "01/05/2020": True,
        "01/10/2020": False,
        "01/05/2021": True,
        "01/10/2021": False,
        "01/05/2022": False,
    }
    cut_hedges.update_completed_dates(scheduled_dates)
    cut_hedges.update_completed_dates(scheduled_dates)
    assert cut_hedges.completed_dates == [
        datetime(2020, 5, 1, 0, 0),
        datetime(2021, 5, 1, 0, 0),
    ]


def test_remove_one_completed_date(cut_hedges):
    scheduled_dates = {
        "01/05/2020": True,
        "01/10/2020": False,
        "01/05/2021": False,
        "01/10/2021": False,
        "01/05/2022": False,
    }
    cut_hedges.update_completed_dates(scheduled_dates)
    assert cut_hedges.completed_dates == [datetime(2020, 5, 1, 0, 0)]
    scheduled_dates = {
        "01/05/2020": False,
        "01/10/2020": False,
        "01/05/2021": False,
        "01/10/2021": False,
        "01/05/2022": False,
    }
    cut_hedges.update_completed_dates(scheduled_dates)
    assert cut_hedges.completed_dates == []


def test_remove_two_completed_dates(cut_hedges):
    scheduled_dates = {
        "01/05/2020": True,
        "01/10/2020": False,
        "01/05/2021": True,
        "01/10/2021": False,
        "01/05/2022": True,
    }
    cut_hedges.update_completed_dates(scheduled_dates)
    assert cut_hedges.completed_dates == [
        datetime(2020, 5, 1, 0, 0),
        datetime(2021, 5, 1, 0, 0),
        datetime(2022, 5, 1, 0, 0),
    ]
    scheduled_dates = {
        "01/05/2020": True,
        "01/10/2020": False,
        "01/05/2021": False,
        "01/10/2021": False,
        "01/05/2022": False,
    }
    cut_hedges.update_completed_dates(scheduled_dates)
    assert cut_hedges.completed_dates == [datetime(2020, 5, 1, 0, 0)]


# Get all progress


def test_get_all_progress_no_completed_dates(cut_hedges):
    assert cut_hedges.get_all_progress() == {
        "01/05/2020": False,
        "01/10/2020": False,
        "01/05/2021": False,
        "01/10/2021": False,
        "01/05/2022": False,
    }


def test_get_all_progress_with_completed_dates(cut_hedges):
    scheduled_dates = {"01/05/2020": True, "01/10/2021": True}
    cut_hedges.update_completed_dates(scheduled_dates)
    assert cut_hedges.get_all_progress() == {
        "01/05/2020": True,
        "01/10/2020": False,
        "01/05/2021": False,
        "01/10/2021": True,
        "01/05/2022": False,
    }


# Get current progress


def test_current_progress_no_completed_dates_not_yet_due(cut_hedges):
    current_progress = cut_hedges.get_current_progress(current_date="30/04/2020")
    assert current_progress == "Not yet due"


def test_current_progress_no_completed_dates_due(cut_hedges):
    current_progress = cut_hedges.get_current_progress(current_date="01/05/2020")
    assert current_progress == "Due"


def test_current_progress_no_completed_dates_overdue(cut_hedges):
    current_progress = cut_hedges.get_current_progress(current_date="01/09/2020")
    assert current_progress == "Overdue"


def test_current_progress_no_completed_dates_very_overdue(cut_hedges):
    current_progress = cut_hedges.get_current_progress(current_date="01/11/2020")
    assert current_progress == "Very overdue"


def test_current_progress_with_completed_date_due(cut_hedges):
    scheduled_dates = {"01/05/2020": True, "01/10/2020": False}
    cut_hedges.update_completed_dates(scheduled_dates)
    current_progress = cut_hedges.get_current_progress(current_date="01/10/2020")
    assert current_progress == "Due"


def test_current_progress_with_completed_date_one_missed_date(cut_hedges):
    scheduled_dates = {"01/05/2020": True}
    cut_hedges.update_completed_dates(scheduled_dates)
    current_progress = cut_hedges.get_current_progress(current_date="01/11/2020")
    assert current_progress == "Overdue"


def test_current_progress_with_completed_dates_two_missed_dates(cut_hedges):
    scheduled_dates = {"01/05/2020": True, "01/10/2020": True}
    cut_hedges.update_completed_dates(scheduled_dates)
    current_progress = cut_hedges.get_current_progress(current_date="01/11/2021")
    assert current_progress == "Very overdue"


def test_current_progress_with_completed_dates_no_missed_dates(cut_hedges):
    scheduled_dates = {"01/05/2020": True, "01/10/2020": True}
    cut_hedges.update_completed_dates(scheduled_dates)
    current_progress = cut_hedges.get_current_progress(current_date="01/04/2021")
    assert current_progress == "Completed"


# Get next date date


def test_get_next_due_date_no_completed_dates(cut_hedges):
    next_due = cut_hedges.get_next_due_date()
    assert next_due == "01/05/2020"


def test_get_next_due_date_all_dates_completed(cut_hedges):
    scheduled_dates = {
        "01/05/2020": True,
        "01/10/2020": True,
        "01/05/2021": True,
        "01/10/2021": True,
        "01/05/2022": True,
    }
    cut_hedges.update_completed_dates(scheduled_dates)
    next_due = cut_hedges.get_next_due_date()
    assert next_due == "No further due dates"


def test_get_next_due_date_last_date_completed(cut_hedges):
    scheduled_dates = {
        "01/05/2020": False,
        "01/10/2020": True,
        "01/05/2021": False,
        "01/10/2021": False,
        "01/05/2022": True,
    }
    cut_hedges.update_completed_dates(scheduled_dates)
    next_due = cut_hedges.get_next_due_date()
    assert next_due == "No further due dates"


def test_get_next_due_date_first_date_completed(cut_hedges):
    scheduled_dates = {
        "01/05/2020": True,
        "01/10/2020": False,
        "01/05/2021": False,
        "01/10/2021": False,
        "01/05/2022": False,
    }
    cut_hedges.update_completed_dates(scheduled_dates)
    next_due = cut_hedges.get_next_due_date()
    assert next_due == "01/10/2020"


def test_get_next_due_date_penultimate_date_completed(cut_hedges):
    scheduled_dates = {
        "01/05/2020": False,
        "01/10/2020": False,
        "01/05/2021": False,
        "01/10/2021": True,
        "01/05/2022": False,
    }
    cut_hedges.update_completed_dates(scheduled_dates)
    next_due = cut_hedges.get_next_due_date()
    assert next_due == "01/05/2022"


if __name__ == "__main__":
    pytest.main()
