from operator import attrgetter

import PySimpleGUI as sg
from accent import ACCENT_COLOR


CREATURE_HEADS = ("Name", "Type", "Appeared", "Impact", "Prevalence", "Trend", "Status")
PLANT_HEADS = ("Name", "Type", "Planted", "Impact", "Prevalence", "Trend", "Status")
TASK_HEADS = ("Name", "Progress", "Next Due", "Assignee", "Length", "Creatures", "Plants", "Status")


def summary_head_format(title):
    return sg.Input(title, size=(13, 1), text_color="white", background_color=ACCENT_COLOR)


def summary_field_format(value):
    return sg.Input(value, size=(13, 1))


def organism_column_format(table):
    return sg.Column(table, size=(750, 500), scrollable=True)


def creature_fields(creature):
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
    """Converts task values into task summary fields."""
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


def sorted_organisms(organisms, sort_key):
    """Sorts organism instances by archived status then by sort key."""
    organisms = sorted(organisms, key=attrgetter(sort_key))
    return sorted(organisms, key=lambda organism: str(organism.status), reverse=True)


def sorted_tasks(tasks):
    """Sorts tasks instances by status, progress, due date, assignee, and name."""
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