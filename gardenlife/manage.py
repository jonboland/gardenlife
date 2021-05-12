from calendar import Calendar
from datetime import datetime
from operator import attrgetter
import logging
import pickle
from tkinter.constants import SUNKEN, GROOVE
import traceback
import sys
import webbrowser

import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Column

from garden import Garden
from organisms import Creature, Plant
from task import Task


logging.basicConfig(
    filename="gardenlife.log", 
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(__name__)


ACCENT_COLOR = "#004225"


sg.theme(new_theme="LightGray1")
sg.theme_button_color(("white", ACCENT_COLOR))
sg.theme_input_background_color("light grey")
sg.theme_input_text_color("black")
sg.theme_slider_color(ACCENT_COLOR)


try:
    with open("gardens.pickle", "rb") as file:
        gardens = pickle.load(file)
# Create the gardens dict and default garden if they don't already exist
except FileNotFoundError:
    gardens = {}
    default_garden = Garden("", "", 0, datetime.today().strftime("%d/%m/%Y"), " ")
    gardens[""] = default_garden
# Load the most recently created/updated garden
garden = max(gardens.values(), key=attrgetter("timestamp"))


# -------------------------------------- Menu -------------------------------------- #


menu_definition = [["File", ["Save", "Exit"]], ["Help", ["About...", "Open web tutorial"]]]


# ------------------------------- Garden Summary Tab ------------------------------- #


REPORT_BUTTON_TEXT = ("VIEW ALL CREATURES", "VIEW ALL PLANTS", "VIEW EDIBLE PLANTS", "VIEW ALL TASKS")

outstanding_tasks = sum(
    task.get_current_progress() in {"Due", "Overdue", "Very overdue"} for task in garden.tasks.values()
)

summary_details = {
    "Garden name:": garden.name,
    "Location:": garden.location,
    "Size:": garden.garden_size(),
    "Owned by:": garden.ownership(),
    "Owned for:": garden.ownership_length(),
    "Total creatures:": len(garden.creatures),
    "Total plants:": len(garden.plants),
    "Total tasks:": len(garden.tasks),
    "Outstanding tasks:": outstanding_tasks,
    "Current season:": garden.season(),
}

summary = [
    [
        sg.Text(label, size=(15, 1), pad=(0, 10), justification="right"),
        sg.Text(value, size=(30, 1), relief=SUNKEN, key=f"-SUMMARY {label[:-1].upper()}-"),
    ]
    for label, value in summary_details.items()
]

report_buttons = [
    [sg.Button(name, size=(20, 2), pad=(0, 10), border_width=2)] for name in REPORT_BUTTON_TEXT
]

summary_tab = [
    [
        sg.Column(summary, pad=((30, 40), 40)),
        sg.Column(report_buttons, size=(200, 260), pad=((25, 40), 0)),
    ]
]


# ------------------------ Shared Tab Functions & Constants ------------------------ #


ITEM_BUTTON_TEXT = ("CREATE/UPDATE", "REMOVE")
FIELD_SIZE = (25, 1)


def item_label(label):
    return sg.Text(label, size=(13, 1), pad=(0, 10))


def organism_slider_label(label):
    return sg.Text(label, size=(12, 1), pad=((0, 8), (20, 0)))


def organism_slider(key=None, tooltip=None):
    return sg.Slider(
        range=(1, 5),
        key=key,
        orientation="horizontal",
        default_value=3,
        size=(19.7, 19),
        tooltip=tooltip,
    )


# -------------------------------- Manage Garden Tab ------------------------------- #


MG_FIELD_SIZE = (34, 1)


garden_details = {
    "Garden name:": garden.name,
    "Location:": garden.location,
    "Size:": garden.size,
    "Owner names:": " ".join(garden.owners),
}


def garden_label_format(label):
    return sg.Text(label, size=(15, 1), pad=(0, 10), justification="right")


select_garden = [
    garden_label_format("Select garden:"),
    sg.Combo(
        sorted(list(gardens)),
        default_value=garden.name,
        size=(34, 10),
        background_color="#F2F2F2",
        enable_events=True,
        readonly=True,
        key="-SELECT GARDEN-",
    ),
]

garden_blank = [sg.Text("", size=(0, 1))]  # Blank row to add space below selector

garden_details = [
    [
        garden_label_format(label),
        sg.Input(value, size=MG_FIELD_SIZE, key=f"-{label[:-1].upper()}-"),
    ]
    for label, value in garden_details.items()
]

owned_since = [
    garden_label_format("Owned since:"),
    sg.Input(garden.since, size=MG_FIELD_SIZE, tooltip="DD/MM/YYYY", key="-OWNED SINCE-"),
    sg.CalendarButton("PICK", format="%d/%m/%Y", pad=(0, 0)),
]

garden_buttons = [
    sg.Button(name, size=(18, 2), pad=((32.5, 0), 30), key=f"GARDEN {name}") for name in ITEM_BUTTON_TEXT
]

garden_elements = [select_garden, garden_blank] + garden_details + [owned_since, garden_buttons]

garden_tab = [[sg.Column(garden_elements, pad=((30, 40), 40))]]


# ------------------------------ Manage Creatures Tab ------------------------------ #


creature_name = [
    item_label("Creature name:"),
    sg.Combo(
        sorted([""] + list(garden.creatures)),
        size=(25, 10),
        key="-CREATURE NAME-",
        enable_events=True,
    ),
]

creature_type = [
    item_label("Creature type:"),
    sg.Combo(
        sorted([""] + list(set(c.creature_type for c in garden.creatures.values() if c.creature_type))),
        size=(25, 10),
        key="-CREATURE TYPE-",
    ),
]

creature_age = [item_label("Creature age:"), sg.Input(size=FIELD_SIZE, key="-CREATURE AGE-")]

creature_appeared = [
    sg.Text("Appeared date:", size=(13, 1), pad=(0, (6, 30))),
    sg.Input(size=FIELD_SIZE, pad=(5, (6, 30)), tooltip="DD/MM/YYYY", key="-CREATURE APPEARED DATE-"),
    sg.CalendarButton("PICK", format="%d/%m/%Y", pad=(0, (6, 30))),
]

creature_impact = [
    organism_slider_label("Impact level:"),
    organism_slider(
        key="-CREATURE IMPACT SLIDER-",
        tooltip="Impact levels — 1: very negative, 2: negative, "
        "3: neutral, 4: positive, 5: very positive",
    ),
]

creature_prevalence = [
    organism_slider_label("Prevalence level:"),
    organism_slider(
        key="-CREATURE PREVALENCE SLIDER-",
        tooltip="Prevalence levels — 1: very low, 2: low, " "3: medium, 4: high, 5: very high",
    ),
]

creature_trend = [
    organism_slider_label("Trend level:"),
    organism_slider(
        key="-CREATURE TREND SLIDER-",
        tooltip="Trend levels — 1: rapidly decreasing, 2: decreasing, "
        "3: stable, 4: increasing, 5: rapidly increasing",
    ),
]

creature_status = [
    sg.Text("Status:", size=(8, 1), pad=(0, 10)),
    sg.Combo(
        ["", "current", "archived"],
        size=FIELD_SIZE,
        readonly=True,
        background_color="#F2F2F2",
        key="-CREATURE STATUS-",
    ),
]

creature_notes_label = [sg.Text("Notes:", size=(8, 1), pad=(0, 10))]

creature_notes_field = [sg.Multiline(size=(35, 10), pad=(0, 10), key="-CREATURE NOTES-")]

creature_buttons = [
    sg.Button(name, size=(15, 2), pad=((0, 7), (32, 0)), key=f"CREATURE {name}")
    for name in ITEM_BUTTON_TEXT
]

creatures_left_column = [
    creature_name,
    creature_type,
    creature_age,
    creature_appeared,
    creature_impact,
    creature_prevalence,
    creature_trend,
]

creatures_right_column = [
    creature_status,
    creature_notes_label,
    creature_notes_field,
    creature_buttons,
]

creatures_tab = [
    [
        sg.Column(creatures_left_column, pad=((30, 40), 40), vertical_alignment="top"),
        sg.Column(creatures_right_column, pad=((0, 40), 40), vertical_alignment="top"),
    ]
]


# -------------------------------- Manage Plants Tab ------------------------------- #


plant_name = [
    item_label("Plant name:"),
    sg.Combo(
        sorted([""] + list(garden.plants)),
        size=(25, 10),
        key="-PLANT NAME-",
        enable_events=True,
    ),
]

plant_type = [
    item_label("Plant type:"),
    sg.Combo(
        sorted([""] + list(set(p.plant_type for p in garden.plants.values() if p.plant_type))),
        size=(25, 10),
        key="-PLANT TYPE-",
    ),
]

plant_age = [item_label("Plant age:"), sg.Input(size=FIELD_SIZE, key="-PLANT AGE-")]

plant_appeared = [
    sg.Text("Planted date:", size=(13, 1), pad=(0, (6, 30))),
    sg.Input(
        size=FIELD_SIZE,
        pad=(5, (6, 30)),
        tooltip="DD/MM/YYYY",
        key="-PLANT PLANTED DATE-",
    ),
    sg.CalendarButton("PICK", format="%d/%m/%Y", pad=(0, (6, 30)), key="-PLANT PICK-"),
]

plant_impact = [
    organism_slider_label("Impact level:"),
    organism_slider(
        key="-PLANT IMPACT SLIDER-",
        tooltip="Impact levels — 1: very negative, 2: negative, "
        "3: neutral, 4: positive, 5: very positive",
    ),
]

plant_prevalence = [
    organism_slider_label("Prevalence level:"),
    organism_slider(
        key="-PLANT PREVALENCE SLIDER-",
        tooltip="Prevalence levels — 1: very low, 2: low, " "3: medium, 4: high, 5: very high",
    ),
]

plant_trend = [
    organism_slider_label("Trend level:"),
    organism_slider(
        key="-PLANT TREND SLIDER-",
        tooltip="Trend levels — 1: rapidly decreasing, 2: decreasing, "
        "3: stable, 4: increasing, 5: rapidly increasing",
    ),
]

plant_status = [
    sg.Text("Status:", size=(8, 1), pad=(0, 10)),
    sg.Combo(
        ["", "current", "archived"],
        size=FIELD_SIZE,
        readonly=True,
        background_color="#F2F2F2",
        key="-PLANT STATUS-",
    ),
]

plant_edible = [
    sg.Text("Edible:", size=(8, 1), pad=(0, 10)), sg.Checkbox("", pad=(0, 0), key="-PLANT EDIBLE-")
]

plant_notes_label = [sg.Text("Notes:", size=(8, 1), pad=(0, 10))]

plant_notes_field = [sg.Multiline(size=(35, 10), pad=(0, 10), key="-PLANT NOTES-")]

plant_buttons = [
    sg.Button(name, size=(15, 2), pad=((0, 7), (32, 0)), key=f"PLANT {name}")
    for name in ITEM_BUTTON_TEXT
]

plants_left_column = [
    plant_name,
    plant_type,
    plant_age,
    plant_appeared,
    plant_impact,
    plant_prevalence,
    plant_trend,
]

plants_right_column = [
    plant_status,
    plant_edible,
    plant_notes_label,
    plant_notes_field,
    plant_buttons,
]

plants_tab = [
    [
        sg.Column(plants_left_column, pad=((30, 40), 40), vertical_alignment="top"),
        sg.Column(plants_right_column, pad=((0, 40), 40), vertical_alignment="top"),
    ]
]


# -------------------------------- Manage Tasks Tab -------------------------------- #


task_name = [
    item_label("Task name:"),
    sg.Combo(
        sorted([""] + list(garden.tasks)),
        size=FIELD_SIZE,
        key="-TASK NAME-",
        enable_events=True,
    ),
]

task_progress = [
    item_label("Progress:"),
    sg.Text("", size=(22, 1), relief=SUNKEN, key="-TASK PROGRESS-"),
]

task_next_due = [
    item_label("Next due:"),
    sg.Text("", size=(22, 1), relief=SUNKEN, key="-TASK NEXT DUE-"),
]

add_progress_button = [sg.Button("ADD PROGRESS", size=(21, 1), pad=((113.5, 0), (10, 4)))]

task_first_horizontal_line = [sg.Text("_" * 41, pad=(0, 0))]

task_assignee = [
    sg.Text("Assignee:", size=(13, 1), pad=(0, (16, 10))),
    sg.Input(size=FIELD_SIZE, key="-TASK ASSIGNEE-", pad=(4, (10, 0))),
]

task_length = [
    sg.Text("Length:", size=(13, 1), pad=(0, (10, 0))),
    sg.Input(size=FIELD_SIZE, key="-TASK LENGTH-", pad=(4, (10, 0))),
]

task_second_horizontal_line = [sg.Text("_" * 41, pad=(0, 0))]

task_link_labels = [
    sg.Text("Linked creatures:", size=(12, 1), pad=((0, 68), 10)),
    sg.Text("Linked plants:", size=(12, 1), pad=(0, 10)),
]

task_link_organisms = [
    sg.Listbox(
        values=(sorted(list(garden.creatures))),
        select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
        size=(17, 5),
        pad=((1, 26), 0),
        highlight_background_color=ACCENT_COLOR,
        key="-TASK LINKED CREATURES-",
    ),
    sg.Listbox(
        values=(sorted(list(garden.plants))),
        select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
        size=(17, 5),
        highlight_background_color=ACCENT_COLOR,
        key="-TASK LINKED PLANTS-",
    ),
]

task_status = [
    sg.Text("Status:", size=(8, 1), pad=((2, 0), 10)),
    sg.Combo(
        ["", "current", "archived"],
        size=FIELD_SIZE,
        readonly=True,
        background_color="#F2F2F2",
        key="-TASK STATUS-",
    ),
]

task_notes_label = [sg.Text("Description:", size=(10, 1), pad=(2, 10))]

task_description_field = [sg.Multiline(size=(37, 5), pad=(5, (10, 15)), key="-TASK NOTES-")]

task_start = [
    sg.Text("First due:", size=(8, 1), pad=(3, (13, 0))),
    sg.Input(size=(18, 1), pad=(5, (13, 0)), tooltip="DD/MM/YYYY", key="-TASK START-"),
    sg.CalendarButton("PICK", format="%d/%m/%Y", pad=((0, 7), (13, 0)), key="-TASK PICK START-"),
]

task_frequency = [
    sg.Text("Frequency:", size=(8, 1), pad=(3, (6, 0))),
    sg.Combo(
        ["", "daily", "weekly", "monthly", "yearly"],
        size=(18, 1),
        pad=(5, (6, 0)),
        readonly=True,
        background_color="#F2F2F2",
        key="-TASK FREQUENCY-",
    ),
]

task_count = [
    sg.Text("Count:", size=(8, 1), pad=(3, (8, 0))),
    sg.Input(
        size=(18, 1),
        pad=(5, (8, 0)),
        tooltip="Number of times task should be completed",
        key="-TASK COUNT-",
    ),
]

task_by_month = [
    sg.Text("By month:", size=(8, 1), pad=(3, (8, 0))),
    sg.Input(
        size=(18, 1),
        pad=(5, (8, 0)),
        tooltip="Digits between 1 and 12 separated by spaces\n"
        "For example: 1 3 5\n"
        "Specifies months when task should be completed",
        key="-TASK BY MONTH-",
    ),
]

task_interval = [
    sg.Text("Interval:", size=(8, 1), pad=(3, (8, 20))),
    sg.Input(
        size=(18, 1),
        tooltip="Digit representing interval between due dates\n"
        "For example: if frequency is monthly, 2 means every 2 months",
        pad=(5, (8, 20)),
        key="-TASK INTERVAL-",
    ),
]

schedule_contents = [
    task_start,
    task_frequency,
    task_count,
    task_by_month,
    task_interval,
]

task_schedule_frame = [
    sg.Frame("Schedule", schedule_contents, relief=GROOVE, border_width=2, size=(25, 5))
]

task_buttons = [
    sg.Button(name, size=(15, 2), pad=((4, 4), (22, 0)), key=f"TASK {name}") for name in ITEM_BUTTON_TEXT
]

plants_left_column = [
    task_name,
    task_progress,
    task_next_due,
    add_progress_button,
    task_first_horizontal_line,
    task_assignee,
    task_length,
    task_second_horizontal_line,
    task_link_labels,
    task_link_organisms,
]

plants_right_column = [
    task_status,
    task_notes_label,
    task_description_field,
    task_schedule_frame,
    task_buttons,
]

tasks_tab = [
    [
        sg.Column(plants_left_column, pad=((30, 40), 40), vertical_alignment="top"),
        sg.Column(plants_right_column, pad=((0, 40), 40), vertical_alignment="top"),
    ]
]


# ----------------------------------- Main Layout ---------------------------------- #


tab_details = {
    "Garden Summary": summary_tab,
    "Manage Garden": garden_tab,
    "Manage Creatures": creatures_tab,
    "Manage Plants": plants_tab,
    "Manage Tasks": tasks_tab,
}

all_tabs = [[sg.Tab(label, tab, pad=(10, 10)) for label, tab in tab_details.items()]]

layout = [[sg.Menu(menu_definition)], [sg.TabGroup(all_tabs, tab_background_color=ACCENT_COLOR)]]
# Create the window
window = sg.Window("gardenlife", layout, keep_on_top=True, enable_close_attempted_event=True)


# ----------------------- Summary Event Headings & Functions ----------------------- #


CREATURE_HEADS = ("Name", "Type", "Appeared", "Age", "Impact", "Prevalence", "Trend", "Status")
PLANT_HEADS = ("Name", "Type", "Planted", "Age", "Impact", "Prevalence", "Trend", "Status")
TASK_HEADS = ("Name", "Progress", "Next Due", "Assignee", "Length", "Creatures", "Plants", "Status")


def summary_head_format(title):
    return sg.Input(title, size=(11, 1), text_color="white", background_color=ACCENT_COLOR)


def summary_field_format(value):
    return sg.Input(value, size=(11, 1))


def organism_column_format(table):
    return sg.Column(table, size=(750, 500), scrollable=True)


def creature_fields(creature):
    values = (
        creature.creature_name,
        creature.creature_type,
        creature.appeared,
        creature.age,
        creature.get_level("impact"),
        creature.get_level("prevalence"),
        creature.get_level("trend"),
        creature.status.get(),
    )
    return [summary_field_format(value) for value in values]


def plant_fields(plant):
    values = (
        plant.plant_name,
        plant.plant_type,
        plant.planted,
        plant.age,
        plant.get_level("impact"),
        plant.get_level("prevalence"),
        plant.get_level("trend"),
        plant.status.get(),
    )
    return [summary_field_format(value) for value in values]


def task_fields(task):
    """Converts task values into task summary fields."""
    name_field = [sg.Input(task.task_name, size=(18, 1))]
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
    tasks.sort(key=attrgetter("assignee", "task_name"))
    tasks.sort(key=lambda task: task.get_next_due_date())
    tasks.sort(key=_progress_order, reverse=True)
    tasks.sort(key=lambda task: str(task.status), reverse=True)
    return tasks


def _progress_order(task):
    # Key for sorting tasks so those not yet due are placed before all others
    # Note that the overall order is reversed once this key has been applied to every task
    progress = task.get_current_progress()
    return "A" if progress == "Not yet due" else progress


# ---------------------------- Manage Event Functions ------------------------------ #


def update_garden_dropdown():
    garden_names = sorted(list(gardens))
    return window["-SELECT GARDEN-"].update(values=garden_names, size=(34, 10))


def clear_garden_values():
    for value in ("GARDEN NAME", "LOCATION", "SIZE", "OWNER NAMES", "OWNED SINCE"):
        window[f"-{value}-"].update("")


def clear_summary_values():
    for value in (
        "GARDEN NAME",
        "LOCATION",
        "SIZE",
        "OWNED BY",
        "OWNED FOR",
        "TOTAL CREATURES",
        "TOTAL PLANTS",
        "TOTAL TASKS",
        "OUTSTANDING TASKS",
    ):
        window[f"-SUMMARY {value}-"].update("")


def creature_instance():
    return garden.creatures.get(values["-CREATURE NAME-"])


def update_creature_dropdowns():
    creature_names = sorted([""] + list(garden.creatures))
    types = {c.creature_type for c in garden.creatures.values() if c.creature_type}
    creature_types = sorted([""] + list(types))
    return (
        window["-CREATURE NAME-"].update(values=creature_names, size=(25, 10)),
        window["-CREATURE TYPE-"].update(values=creature_types, size=(25, 10)),
    )


def clear_creature_values():
    for value in ("NAME", "TYPE", "AGE", "APPEARED DATE", "STATUS", "NOTES"):
        window[f"-CREATURE {value}-"].update("")
    for value in ("IMPACT", "PREVALENCE", "TREND"):
        window[f"-CREATURE {value} SLIDER-"].update(3)


def plant_instance():
    return garden.plants.get(values["-PLANT NAME-"])


def clear_plant_values():
    for value in ("NAME", "TYPE", "AGE", "PLANTED DATE", "EDIBLE", "STATUS", "NOTES"):
        window[f"-PLANT {value}-"].update("")
    for value in ("IMPACT", "PREVALENCE", "TREND"):
        window[f"-PLANT {value} SLIDER-"].update(3)


def update_plant_dropdowns():
    plant_names = sorted([""] + list(garden.plants))
    types = {p.plant_type for p in garden.plants.values() if p.plant_type}
    plant_types = sorted([""] + list(types))
    return (
        window["-PLANT NAME-"].update(values=plant_names, size=(25, 10)),
        window["-PLANT TYPE-"].update(values=plant_types, size=(25, 10)),
    )


def task_instance():
    return garden.tasks.get(values["-TASK NAME-"])


def clear_task_values():
    for value in (
        "NAME",
        "PROGRESS",
        "NEXT DUE",
        "ASSIGNEE",
        "LENGTH",
        "STATUS",
        "NOTES",
        "START",
        "FREQUENCY",
        "COUNT",
        "BY MONTH",
        "INTERVAL",
    ):
        window[f"-TASK {value}-"].update("")
        task = None


def update_task_dropdown():
    task_names = sorted([""] + list(garden.tasks))
    return window["-TASK NAME-"].update(values=task_names, size=(25, 10))


def clear_organism_links():
    window["-TASK LINKED CREATURES-"].update(sorted(list(garden.creatures)))
    window["-TASK LINKED PLANTS-"].update(sorted(list(garden.plants)))


def update_all_item_dropdowns():
    update_creature_dropdowns()
    update_plant_dropdowns()
    update_task_dropdown()


def clear_all_item_dropdowns():
    for value in ("CREATURE NAME", "CREATURE TYPE", "PLANT NAME", "PLANT TYPE", "TASK NAME"):
        window[f"-{value}-"].update(values="", size=(25, 10))


def clear_all_item_values_and_links():
    clear_creature_values()
    clear_plant_values()
    clear_task_values()
    clear_organism_links()


def clear_all_values_and_links():
    clear_garden_values()
    clear_summary_values()
    clear_all_item_values_and_links()


def view_plants_window(plant, attr):
        window.Disable()

        header_row = [[summary_head_format(title) for title in PLANT_HEADS]]

        plants = [
            plant_fields(plant)
            for plant in sorted_organisms(garden.plants.values(), sort_key="plant_name") if getattr(plant, attr)
        ]

        plant_table = header_row + plants

        plant_summary_column = [organism_column_format(plant_table)]

        plant_summary_layout = [plant_summary_column, [sg.Button("Close")]]

        plant_summary_window = sg.Window("Plant Summary", plant_summary_layout, keep_on_top=True)

        while True:
            plant_sum_event, plant_sum_values = plant_summary_window.read()
            print(plant_sum_event, plant_sum_values)

            if plant_sum_event in (sg.WIN_CLOSED, "Close"):
                plant_summary_window.close()
                window.Enable()
                break



# ------------------------------------ Popups -------------------------------------- #


MONTHS = [str(month) for month in range(1, 13)]


def fatal_error(error):
    sg.popup(
        "Sorry for the disruption.",
        "Unfortunately, gardenlife has stopped working because the following fatal error occured:",
        error, 
        traceback.format_exc(),
        title="Fatal Error", 
        keep_on_top=True, 
    )


def no_garden_popup(item):
    return sg.popup(
        f"It wasn't possible to add the {item} because a garden hasn't been selected. "
        "Please choose a garden on the Manage Garden tab and try again.",
        title="No Garden Error",
        keep_on_top=True,
    )


def remove_confirmation_popup(name, element):
    return sg.popup_ok_cancel(
        f"Are you sure you want to remove {name}?",
        f"This {element} will be permanently deleted.\n",
        "Click OK if you wish to proceed.\n",
        title="Remove Confirmation",
        keep_on_top=True,
    )


def invalid_name_popup(field):
    return sg.popup(
        f"The {field} field cannot be blank. Please add a name and try again.",
        title="Blank Name Error",
        keep_on_top=True,
    )


def invalid_date_popup(field, date):
    return sg.popup(
        f"The {field} field contains {date}, which is not a valid date. "
        "The format should be DD/MM/YYYY. Please correct and try again.",
        title="Date Format Error",
        keep_on_top=True,
    )


def invalid_digit_popup(field, digit):
    return sg.popup(
        f"The {field} field contains {digit}, which is not a valid digit. "
        "Please correct and try again.",
        title="Digit Error",
        keep_on_top=True,
    )


def invalid_bymonth_popup(bymonth):
    return sg.popup(
        f'The By month field contains "{bymonth}", which includes an invalid month or months. '
        "Months must be digits between 1 and 12, separated by a single space.",
        "Please correct and try again.",
        title="Month Format Error",
        keep_on_top=True,
    )


def no_due_dates_popup():
    return sg.popup(
        "Based on the current schedule, there are no due dates for this task. "
        "Please alter the schedule and try again.",
        title="No Due Dates Error",
        keep_on_top=True,
    )


# ---------------------------------- Event Loop ------------------------------------ #


# Keeps track of whether any changes have been made since the garden was saved
gardens_changed = False

# Display and interact with the window using an event loop
try:
    while True:
        event, values = window.read()
        print(event, values)

        ##################### Menu & Window Closure Events #####################

        # See if user wants to quit or attempted to close the window
        if event in ("Exit", sg.WINDOW_CLOSE_ATTEMPTED_EVENT):

            if gardens_changed:
                window.Disable()

                confirm_layout = [
                    [sg.Text("Would you like to save your changes?", pad=(0, 15))],
                    [
                        sg.Button("Save", size=(10, 1)),
                        sg.Button("Don't Save", size=(10, 1)),
                        sg.Button("Cancel", size=(10, 1)),
                    ],
                ]

                confirm_window = sg.Window(
                    "Confirm",
                    confirm_layout,
                    keep_on_top=True,
                    element_justification="center",
                )

                while True:
                    confirm_event, confirm_values = confirm_window.read()
                    print(confirm_event, confirm_values)

                    if confirm_event == "Save":
                        with open("gardens.pickle", "wb") as file:
                            pickle.dump(gardens, file)
                        sys.exit()
                    if confirm_event == "Don't Save":
                        sys.exit()
                    if confirm_event in ("Cancel", sg.WIN_CLOSED):
                        confirm_window.close()
                        window.Enable()
                        break
            else:
                break

        elif event == "Save":
            with open("gardens.pickle", "wb") as file:
                pickle.dump(gardens, file)
            gardens_changed = False

        elif event == "About...":
            sg.popup(
                "gardenlife v1.0\n\n" "A garden management application created by Jon Boland.\n",
                title="About...",
                button_color=ACCENT_COLOR,
                keep_on_top=True,
            )

        elif event == "Open web tutorial":
            webbrowser.open("https://github.com/jonboland/gardenlife/blob/master/README.rst")

        ######################## Creature Summary Events #######################

        elif event == "VIEW ALL CREATURES":
            window.Disable()

            header_row = [[summary_head_format(title) for title in CREATURE_HEADS]]

            creatures = [
                creature_fields(creature)
                for creature in sorted_organisms(garden.creatures.values(), sort_key="creature_name")
            ]

            creature_table = header_row + creatures

            creature_summary_column = [organism_column_format(creature_table)]

            creature_summary_layout = [creature_summary_column, [sg.Button("Close")]]

            creature_summary_window = sg.Window(
                "Creature Summary", creature_summary_layout, keep_on_top=True
            )

            while True:
                creature_sum_event, creature_sum_values = creature_summary_window.read()
                print(creature_sum_event, creature_sum_values)

                if creature_sum_event in (sg.WIN_CLOSED, "Close"):
                    creature_summary_window.close()
                    window.Enable()
                    break

        ########################## Plant Summary Events ########################

        elif event == "VIEW ALL PLANTS":
            view_plants_window("plant", "plant_name")

        elif event == "VIEW EDIBLE PLANTS":
            view_plants_window("plant", "edible")

        ########################## Task Summary Events #########################

        elif event == "VIEW ALL TASKS":

            window.Disable()

            name_head = [
                sg.Input(TASK_HEADS[0], size=(18, 1), text_color="white", background_color=ACCENT_COLOR)
            ]

            other_head = [summary_head_format(title) for title in TASK_HEADS[1:]]

            header_row = [name_head + other_head]

            tasks = [task_fields(task) for task in sorted_tasks(garden.tasks.values())]

            task_table = header_row + tasks

            task_summary_column = [sg.Column(task_table, size=(800, 500), scrollable=True)]

            task_summary_layout = [task_summary_column, [sg.Button("Close")]]

            task_summary_window = sg.Window("Task Summary", task_summary_layout, keep_on_top=True)

            while True:
                task_sum_event, task_sum_values = task_summary_window.read()
                print(task_sum_event, task_sum_values)

                if task_sum_event in (sg.WIN_CLOSED, "Close"):
                    task_summary_window.close()
                    window.Enable()
                    break

        ######################### Manage Garden Events #########################

        if event == "GARDEN CREATE/UPDATE":
            # Validate garden name and ownership info
            g_name = values["-GARDEN NAME-"].strip()
            g_owners = values["-OWNER NAMES-"].strip()
            g_since = values["-OWNED SINCE-"].strip()
            if not g_name:
                invalid_name_popup("garden name")
                continue
            if not g_owners:
                invalid_name_popup("owner names")
                continue
            try:
                valid_date = datetime.strptime(g_since, "%d/%m/%Y")
            except ValueError:
                invalid_date_popup(field="Owned since", date=g_since)
            # If there are no validation errors, create/update the garden
            else:
                cu_garden = Garden(g_name, values["-LOCATION-"], values["-SIZE-"], g_since, g_owners.split())
                # If garden already exists add all existing items to the updated version
                garden_instance = gardens.get(g_name)
                if garden_instance:
                    cu_garden.creatures = garden_instance.creatures
                    cu_garden.plants = garden_instance.plants
                    cu_garden.tasks = garden_instance.tasks
                # Add created/updated garden to gardens dictionary. Overwrite if already exists
                gardens[g_name] = cu_garden
                # Update dropdowns and clear field values and links
                update_garden_dropdown()
                clear_all_item_dropdowns()
                clear_all_values_and_links()
                gardens_changed = True

        elif event == "GARDEN REMOVE":
            g_confirmation = remove_confirmation_popup(garden.name, "garden")
            if g_confirmation == "OK":
                del gardens[values["-GARDEN NAME-"]]
                update_garden_dropdown()
                clear_all_item_dropdowns()
                clear_all_values_and_links()
                gardens_changed = True

        elif event == "-SELECT GARDEN-":  # A garden is selected from the dropdown
            # Load the selected garden
            garden = gardens[values["-SELECT GARDEN-"]]
            # If the default garden (blank row) is selected, clear fields
            if not values["-SELECT GARDEN-"]:
                clear_garden_values()
                clear_summary_values()
            # Otherwise, update the fields with the selected garden's values
            else:
                window["-GARDEN NAME-"].update(garden.name)
                window["-LOCATION-"].update(garden.location)
                window["-SIZE-"].update(garden.size)
                window["-OWNER NAMES-"].update(" ".join(garden.owners))
                window["-OWNED SINCE-"].update(garden.since)
                # And update the associated summary fields
                window["-SUMMARY GARDEN NAME-"].update(garden.name)
                window["-SUMMARY LOCATION-"].update(garden.location)
                window["-SUMMARY SIZE-"].update(garden.garden_size())
                window["-SUMMARY OWNED BY-"].update(garden.ownership())
                window["-SUMMARY OWNED FOR-"].update(garden.ownership_length())
                window["-SUMMARY TOTAL CREATURES-"].update(len(garden.creatures))
                window["-SUMMARY TOTAL PLANTS-"].update(len(garden.plants))
                window["-SUMMARY TOTAL TASKS-"].update(len(garden.tasks))
                window["-SUMMARY OUTSTANDING TASKS-"].update(outstanding_tasks)
            # Then update the item dropdowns and clear item field values and links
            update_all_item_dropdowns()
            clear_all_item_values_and_links()

        ####################### Manage Creatures Events ########################

        if event == "CREATURE CREATE/UPDATE":
            # Validate garden name, creature name and appeared date
            c_name = values["-CREATURE NAME-"].strip()
            c_appeared = values["-CREATURE APPEARED DATE-"].strip()
            # Check that a garden has been selected
            if not values["-SELECT GARDEN-"]:
                no_garden_popup("creature")
                continue
            if not c_name:
                invalid_name_popup("creature name")
                continue
            try:
                if c_appeared:
                    valid_date = datetime.strptime(c_appeared, "%d/%m/%Y")
            except ValueError:
                invalid_date_popup(field="Appeared date", date=c_appeared)

            else:
                creature = Creature(
                    creature_name=c_name,
                    creature_type=values["-CREATURE TYPE-"],
                    age=values["-CREATURE AGE-"],
                    appeared=c_appeared,
                    notes=values["-CREATURE NOTES-"],
                    impact=values["-CREATURE IMPACT SLIDER-"],
                    prevalence=values["-CREATURE PREVALENCE SLIDER-"],
                    trend=values["-CREATURE TREND SLIDER-"],
                )
                if values["-CREATURE STATUS-"] == "archived":
                    creature.status.archive()
                garden.add_item("creatures", creature)
                update_creature_dropdowns()
                clear_creature_values()
                window["-SUMMARY TOTAL CREATURES-"].update(len(garden.creatures))
                gardens_changed = True

        elif event == "CREATURE REMOVE":
            c_confirmation = remove_confirmation_popup(values["-CREATURE NAME-"], "creature")
            if c_confirmation == "OK":
                garden.remove_item("creatures", values["-CREATURE NAME-"])
                update_creature_dropdowns()
                clear_creature_values()
                window["-SUMMARY TOTAL CREATURES-"].update(len(garden.creatures))
                gardens_changed = True

        elif values["-CREATURE NAME-"] == "":
            clear_creature_values()

        # If a creature is selected populate the relevant fields with its values
        elif event == "-CREATURE NAME-":
            window["-CREATURE NAME-"].update(creature_instance().creature_name)
            window["-CREATURE TYPE-"].update(creature_instance().creature_type)
            window["-CREATURE AGE-"].update(creature_instance().age)
            window["-CREATURE APPEARED DATE-"].update(creature_instance().appeared)
            window["-CREATURE STATUS-"].update(creature_instance().status.get())
            window["-CREATURE NOTES-"].update(creature_instance().notes)
            window["-CREATURE IMPACT SLIDER-"].update(creature_instance().impact)
            window["-CREATURE PREVALENCE SLIDER-"].update(creature_instance().prevalence)
            window["-CREATURE TREND SLIDER-"].update(creature_instance().trend)

        ######################### Manage Plant Events ##########################

        if event == "PLANT CREATE/UPDATE":
            # Validate plant name and planted date
            p_name = values["-PLANT NAME-"].strip()
            p_planted = values["-PLANT PLANTED DATE-"].strip()
            # Check that a garden has been selected
            if not values["-SELECT GARDEN-"]:
                no_garden_popup("plant")
                continue
            if not p_name:
                invalid_name_popup("plant name")
                continue
            try:
                if p_planted:
                    valid_date = datetime.strptime(p_planted, "%d/%m/%Y")
            except ValueError:
                invalid_date_popup(field="Planted date", date=p_planted)

            else:
                plant = Plant(
                    plant_name=p_name,
                    plant_type=values["-PLANT TYPE-"],
                    age=values["-PLANT AGE-"],
                    planted=p_planted,
                    edible=values["-PLANT EDIBLE-"],
                    notes=values["-PLANT NOTES-"],
                    impact=values["-PLANT IMPACT SLIDER-"],
                    prevalence=values["-PLANT PREVALENCE SLIDER-"],
                    trend=values["-PLANT TREND SLIDER-"],
                )
                if values["-PLANT STATUS-"] == "archived":
                    plant.status.archive()
                garden.add_item("plants", plant)
                update_plant_dropdowns()
                clear_plant_values()
                window["-SUMMARY TOTAL PLANTS-"].update(len(garden.plants))
                gardens_changed = True

        elif event == "PLANT REMOVE":
            p_confirmation = remove_confirmation_popup(values["-PLANT NAME-"], "plant")
            if p_confirmation == "OK":
                garden.remove_item("plants", values["-PLANT NAME-"])
                update_plant_dropdowns()
                clear_plant_values()
                window["-SUMMARY TOTAL PLANTS-"].update(len(garden.plants))
                gardens_changed = True

        elif values["-PLANT NAME-"] == "":
            clear_plant_values()

        # If a plant is selected populate the relevant fields with its values
        elif event == "-PLANT NAME-":
            window["-PLANT NAME-"].update(plant_instance().plant_name)
            window["-PLANT TYPE-"].update(plant_instance().plant_type)
            window["-PLANT AGE-"].update(plant_instance().age)
            window["-PLANT PLANTED DATE-"].update(plant_instance().planted)
            window["-PLANT STATUS-"].update(plant_instance().status.get())
            window["-PLANT EDIBLE-"].update(plant_instance().edible)
            window["-PLANT NOTES-"].update(plant_instance().notes)
            window["-PLANT IMPACT SLIDER-"].update(plant_instance().impact)
            window["-PLANT PREVALENCE SLIDER-"].update(plant_instance().prevalence)
            window["-PLANT TREND SLIDER-"].update(plant_instance().trend)

        ########################## Manage Task Events ##########################

        if event == "TASK CREATE/UPDATE":
            # Check that a garden has been selected
            if not values["-SELECT GARDEN-"]:
                no_garden_popup("creature")
                continue
            # Strip and validate task name and set schedule values
            # NB: Frequency is not validated because it's a readonly dropdown
            t_name = values["-TASK NAME-"].strip()
            start_date = values["-TASK START-"].strip()
            count = values["-TASK COUNT-"].strip()
            bymonth = values["-TASK BY MONTH-"].strip()
            interval = values["-TASK INTERVAL-"].strip()
            if not t_name:
                invalid_name_popup("task name")
                continue
            try:
                if start_date:
                    valid_date = datetime.strptime(start_date, "%d/%m/%Y")
            except ValueError:
                invalid_date_popup(field="First due", date=start_date)
                continue
            if count and not count.isdigit():
                invalid_digit_popup(field="Count", digit=count)
            elif bymonth and any(month not in MONTHS for month in bymonth.split(" ")):
                invalid_bymonth_popup(bymonth)
            elif interval and not interval.isdigit():
                invalid_digit_popup(field="Interval", digit=interval)
            # If there are no validation errors, create/update the task
            else:
                task = Task(
                    task_name=t_name,
                    assignee=values["-TASK ASSIGNEE-"],
                    length=values["-TASK LENGTH-"],
                    linked_creatures=values["-TASK LINKED CREATURES-"],
                    linked_plants=values["-TASK LINKED PLANTS-"],
                    description=values["-TASK NOTES-"],
                )

                task.set_schedule(
                    start_date=start_date,
                    freq=values["-TASK FREQUENCY-"],
                    count=count,
                    bymonth=bymonth,
                    interval=interval,
                )
                # Handle rare situation where provided shedule doesn't produce any due dates
                if not task.schedule:
                    no_due_dates_popup()
                    continue

                if values["-TASK STATUS-"] == "archived":
                    task.status.archive()

                # If the task already exists add any pre-existing completed dates to it
                if task_instance():
                    task.completed_dates = task_instance().completed_dates
                # Add the task to the garden, overwriting the old version if it already exists
                garden.add_item("tasks", task)
                update_task_dropdown()
                # Clear the task fields and variable once the task has been added to the garden
                clear_task_values()
                clear_organism_links()
                # Update the task numbers shown on the summary tab
                window["-SUMMARY TOTAL TASKS-"].update(len(garden.tasks))
                window["-SUMMARY OUTSTANDING TASKS-"].update(
                    sum(
                        task.get_current_progress() in {"Due", "Overdue", "Very overdue"}
                        for task in garden.tasks.values()
                    )
                )
                gardens_changed = True

        elif event == "TASK REMOVE":
            t_confirmation = remove_confirmation_popup(values["-TASK NAME-"], "task")
            if t_confirmation == "OK":
                garden.remove_item("tasks", values["-TASK NAME-"])
                update_task_dropdown()
                clear_task_values()
                clear_organism_links()
                window["-SUMMARY TOTAL TASKS-"].update(len(garden.tasks))
                window["-SUMMARY OUTSTANDING TASKS-"].update(
                    sum(
                        task.get_current_progress() in {"Due", "Overdue", "Very overdue"}
                        for task in garden.tasks.values()
                    )
                )
                gardens_changed = True

        elif values["-TASK NAME-"] == "":
            clear_task_values()
            clear_organism_links()

        elif event == "ADD PROGRESS":
            if "task" in globals():
                window.Disable()

                progress_layout = [
                    [
                        sg.Column(
                            [
                                [sg.Checkbox(date, default=value, key=date)]
                                for date, value in task.get_all_progress().items()
                            ],
                            size=(200, 200),
                            scrollable=True,
                        ),
                    ],
                    [sg.Button("Add")],
                ]

                progress_window = sg.Window("Add Progress", progress_layout, keep_on_top=True)

                while True:
                    progress_event, progress_values = progress_window.read()
                    print(progress_event, progress_values)

                    if progress_event == "Add":
                        task.update_completed_dates(progress_values)

                    if progress_event in (sg.WIN_CLOSED, "Add"):
                        progress_window.close()
                        window.Enable()
                        break
            else:
                sg.popup("Task must be created before progress is added.", keep_on_top=True)

        # If a task is selected populate the relevant fields with its values
        elif event == "-TASK NAME-":
            window["-TASK PROGRESS-"].update(task_instance().get_current_progress())
            window["-TASK NEXT DUE-"].update(task_instance().get_next_due_date())
            window["-TASK ASSIGNEE-"].update(task_instance().assignee)
            window["-TASK LENGTH-"].update(task_instance().length)
            window["-TASK LINKED CREATURES-"].set_value(task_instance().linked_creatures)
            window["-TASK LINKED PLANTS-"].set_value(task_instance().linked_plants)
            window["-TASK STATUS-"].update(task_instance().status.get())
            window["-TASK NOTES-"].update(task_instance().description)
            window["-TASK START-"].update(task_instance().raw_schedule["start date"])
            window["-TASK FREQUENCY-"].update(task_instance().raw_schedule["freq"])
            window["-TASK COUNT-"].update(task_instance().raw_schedule["count"])
            window["-TASK BY MONTH-"].update(task_instance().raw_schedule["bymonth"])
            window["-TASK INTERVAL-"].update(task_instance().raw_schedule["interval"])
            # Assign instance to task variable so progress can be added
            task = task_instance()

except Exception as e:
    logger.exception("Fatal Error")
    fatal_error(e)

    ########################################################################

# Finish up by removing from the screen
window.close()
