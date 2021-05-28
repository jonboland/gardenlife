"""Summary functions for the gardenlife application."""

from operator import attrgetter

import PySimpleGUI as sg
from constants import ACCENT_COLOR


def summary_head_format(title):
    """Apply formatting to summary headings."""
    return sg.Input(title, size=(13, 1), text_color="white", background_color=ACCENT_COLOR)


def summary_field_format(value):
    """Apply formatting to a summary field."""
    return sg.Input(value, size=(13, 1))


def organism_column_format(table):
    """Apply formatting to creature and plant summary columns."""
    return sg.Column(table, size=(750, 500), scrollable=True)


def creature_fields(creature):
    """Return formatted summary fields for a creature."""
    values = (
        creature.name,
        creature.org_type,
        creature.appeared,
        creature.get_level("impact"),
        creature.get_level("prevalence"),
        creature.get_level("trend"),
        creature.status.get(),
    )
    return [summary_field_format(value) for value in values]


def plant_fields(plant):
    """Return formatted summary fields for a plant."""
    values = (
        plant.name,
        plant.org_type,
        plant.planted,
        plant.get_level("impact"),
        plant.get_level("prevalence"),
        plant.get_level("trend"),
        plant.status.get(),
    )
    return [summary_field_format(value) for value in values]


def task_fields(task):
    """Return formatted summary fields for a task."""
    name_field = [sg.Input(task.name, size=(18, 1))]
    other_values = (
        task.get_current_progress(),
        task.get_next_due_date(),
        task.assignee,
        task.length,
        ", ".join(task.linked_creatures),
        ", ".join(task.linked_plants),
        task.status.get(),
    )
    other_fields = [summary_field_format(value) for value in other_values]
    return name_field + other_fields


def sorted_organisms(organisms, sort_key="name"):
    """Sort organism instances by archived status then by sort key."""
    organisms = sorted(organisms, key=attrgetter(sort_key))
    return sorted(organisms, key=lambda organism: str(organism.status), reverse=True)


def sorted_tasks(tasks):
    """Sort tasks instances by status, progress, due date, assignee, and name."""
    tasks = list(tasks)
    tasks.sort(key=attrgetter("assignee", "name"))
    tasks.sort(key=lambda task: task.get_next_due_date())
    tasks.sort(key=_progress_order, reverse=True)
    tasks.sort(key=lambda task: str(task.status), reverse=True)
    return tasks


def _progress_order(task):
    # Key for sorting tasks so those not yet due are placed before all others
    # Note that the overall order is then reversed once this key has been applied to every task
    progress = task.get_current_progress()
    return "A" if progress == "Not yet due" else progress