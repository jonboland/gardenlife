from calendar import Calendar
import pickle
from tkinter.constants import SUNKEN, GROOVE
import traceback
import sys

import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Column

from garden import Garden
from organisms import Creature, Plant
from task import Task


sg.theme(new_theme="LightGray1")
sg.theme_button_color(("white", "#004225"))
sg.theme_input_background_color("light grey")
sg.theme_input_text_color("black")
sg.theme_slider_color("#004225")


try:
    with open("garden.pickle", "rb") as file:
        garden = pickle.load(file)
except (OSError, IOError):
    garden = Garden("-", "-", 0, "01/01/2000", "-")


# -------------------------------------- Menu -------------------------------------- #


menu_definition = [["File", ["Save", "Exit"]], ["About..."]]


# ------------------------------- Garden Summary Tab ------------------------------- #


REPORT_BUTTON_TEXT = ("VIEW ALL CREATURES", "VIEW ALL PLANTS", "VIEW ALL TASKS")


summary_details = {
    "Current season:": garden.season(),
    "Garden name:": garden.name,
    "Location:": garden.location,
    "Size:": garden.garden_size(),
    "Owned by:": garden.ownership(),
    "Owned for:": garden.ownership_length(),
    "Total creatures:": len(garden.creatures),
    "Total plants:": len(garden.plants),
    "Total tasks:": len(garden.tasks),
    "Outstanding tasks:": 0,
}

# fmt: off
summary = [
    [
        sg.Text(label, size=(15, 1), pad=(0, 10), justification="right"),
        sg.Text(value, size=(30, 1), relief=SUNKEN, key=f"-SUMMARY {label[:-1].upper()}-"),
    ]
    for label, value in summary_details.items()
]
# fmt: on

report_buttons = [
    [sg.Button(name, size=(20, 2), pad=(0, 10), border_width=2)]
    for name in REPORT_BUTTON_TEXT
]


summary_tab = [
    [
        # sg.Text("", size=(1, 20)),  # Blank row to set column sizes
        sg.Column(summary, pad=((30, 40), 40)),
        sg.Column(report_buttons, size=(200, 190), pad=((25, 40), 0)),
    ]
]


# -------------------------------- Manage Garden Tab ------------------------------- #


GARDEN_BUTTON_TEXT = ("CREATE GARDEN", "UPDATE GARDEN")


garden_details = {
    "Garden name:": garden.name,
    "Location:": garden.location,
    "Size:": garden.size,
    "Owner names:": " ".join(garden.owners),
    "Owned since:": garden.since,
}


def garden_label_format(label):
    return sg.Text(label, size=(15, 1), pad=(0, 10), justification="right")


select_garden = [
    garden_label_format("Select garden:"),
    sg.Combo([], default_value=garden.name, size=(30, 10), key="-SELECT GARDEN-"),
]


garden_blank = [sg.Text("", size=(0, 1))]  # Blank row to add space below selector

garden_details = [
    [
        garden_label_format(label),
        sg.Input(value, size=(30, 1), key=f"-{label[:-1].upper()}-"),
    ]
    for label, value in garden_details.items()
]

garden_buttons = [
    sg.Button(name, size=(15, 2), pad=((43, 0), 30)) for name in GARDEN_BUTTON_TEXT
]

garden_elements = [select_garden, garden_blank] + garden_details + [garden_buttons]

garden_tab = [[sg.Column(garden_elements, pad=((30, 40), 40))]]


# ------------------------------ Manage Creatures Tab ------------------------------ #


CREATURE_BUTTON_TEXT = ("CREATE/UPDATE", "REMOVE")
CREATURE_FIELD_SIZE = (25, 1)


def creature_label(label):
    return sg.Text(label, size=(13, 1), pad=(0, 10))


def creature_slider_label(label):
    return sg.Text(label, size=(12, 1), pad=((0, 8), (20, 0)))


def creature_slider(key=None, tooltip=None):
    return sg.Slider(
        range=(1, 5),
        key=key,
        orientation="horizontal",
        default_value=3,
        size=(19.7, 19),
        tooltip=tooltip,
    )


creature_name = [
    creature_label("Creature name:"),
    sg.Combo(
        sorted([""] + list(garden.creatures)),
        size=(25, 10),
        key="-CREATURE NAME-",
        enable_events=True,
    ),
]
# fmt: off
creature_type = [
    creature_label("Creature type:"),
    sg.Combo(
        sorted([""] + [creature.creature_type for creature in garden.creatures.values()]),
        size=(25, 10),
        key="-CREATURE TYPE-",
    ),
]

creature_age = [
    creature_label("Creature age:"),
    sg.Input(size=CREATURE_FIELD_SIZE, key="-CREATURE AGE-"),
]

creature_appeared = [
    sg.Text("Appeared date:", size=(13, 1), pad=(0, (6, 30))),
    sg.Input(size=CREATURE_FIELD_SIZE, key="-CREATURE APPEARED DATE-", pad=(5, (6, 30))),
    sg.CalendarButton("PICK", format="%d/%m/%Y", pad=(0, (6, 30))),
]

creature_impact = [
    creature_slider_label("Impact level:"),
    creature_slider(
        key="-CREATURE IMPACT SLIDER-",
        tooltip="Impact levels — 1: very negative, 2: negative, "
                "3: neutral, 4: positive, 5: very positive",
    ),
]

creature_prevalence = [
    creature_slider_label("Prevalence level:"),
    creature_slider(
        key="-CREATURE PREVALENCE SLIDER-", 
        tooltip="Prevalence levels — 1: very low, 2: low, "
                "3: medium, 4: high, 5: very high",
    ),
]

creature_trend = [
    creature_slider_label("Trend level:"),
    creature_slider(
        key="-CREATURE TREND SLIDER-", 
        tooltip="Trend levels — 1: rapidly decreasing, 2: decreasing, "
                "3: stable, 4: increasing, 5: rapidly increasing",
    ),
]

creature_status = [
    sg.Text("Status:", size=(8, 1), pad=(0, 10)),
    sg.Combo(["current", "archived"], size=CREATURE_FIELD_SIZE, key="-CREATURE STATUS-"),
]

creature_notes_label = [sg.Text("Notes:", size=(8, 1), pad=(0, 10))]

creature_notes_field = [sg.Multiline(size=(35, 10), pad=(0, 10), key="-CREATURE NOTES-")]
# fmt: on
creature_buttons = [
    sg.Button(name, size=(15, 2), pad=((0, 7), (32, 0)), key=f"CREATURE {name}")
    for name in CREATURE_BUTTON_TEXT
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


PLANT_BUTTON_TEXT = ("CREATE/UPDATE", "REMOVE")
PLANT_FIELD_SIZE = (25, 1)


def plant_label(label):
    return sg.Text(label, size=(13, 1), pad=(0, 10))


def plant_slider_label(label):
    return sg.Text(label, size=(12, 1), pad=((0, 8), (20, 0)))


def plant_slider(key=None, tooltip=None):
    return sg.Slider(
        range=(1, 5),
        key=key,
        orientation="horizontal",
        default_value=3,
        size=(19.7, 19),
        tooltip=tooltip,
    )


plant_name = [
    plant_label("Plant name:"),
    sg.Combo(
        sorted([""] + list(garden.plants)),
        size=(25, 10),
        key="-PLANT NAME-",
        enable_events=True,
    ),
]

plant_type = [
    plant_label("Plant type:"),
    sg.Combo(
        sorted([""] + [plant.plant_type for plant in garden.plants.values()]),
        size=(25, 10),
        key="-PLANT TYPE-",
    ),
]

plant_age = [
    plant_label("Plant age:"),
    sg.Input(size=PLANT_FIELD_SIZE, key="-PLANT AGE-"),
]

plant_appeared = [
    sg.Text("Planted date:", size=(13, 1), pad=(0, (6, 30))),
    sg.Input(size=PLANT_FIELD_SIZE, key="-PLANT PLANTED DATE-", pad=(5, (6, 30))),
    sg.CalendarButton("PICK", format="%d/%m/%Y", pad=(0, (6, 30)), key="-PLANT PICK-"),
]

plant_impact = [
    plant_slider_label("Impact level:"),
    plant_slider(
        key="-PLANT IMPACT SLIDER-",
        tooltip="Impact levels — 1: very negative, 2: negative, "
        "3: neutral, 4: positive, 5: very positive",
    ),
]

plant_prevalence = [
    plant_slider_label("Prevalence level:"),
    plant_slider(
        key="-PLANT PREVALENCE SLIDER-",
        tooltip="Prevalence levels — 1: very low, 2: low, "
        "3: medium, 4: high, 5: very high",
    ),
]

plant_trend = [
    plant_slider_label("Trend level:"),
    plant_slider(
        key="-PLANT TREND SLIDER-",
        tooltip="Trend levels — 1: rapidly decreasing, 2: decreasing, "
        "3: stable, 4: increasing, 5: rapidly increasing",
    ),
]

plant_status = [
    sg.Text("Status:", size=(8, 1), pad=(0, 10)),
    sg.Combo(["current", "archived"], size=PLANT_FIELD_SIZE, key="-PLANT STATUS-"),
]

plant_notes_label = [sg.Text("Notes:", size=(8, 1), pad=(0, 10))]

plant_notes_field = [sg.Multiline(size=(35, 10), pad=(0, 10), key="-PLANT NOTES-")]

plant_buttons = [
    sg.Button(name, size=(15, 2), pad=((0, 7), (32, 0)), key=f"PLANT {name}")
    for name in PLANT_BUTTON_TEXT
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


TASK_BUTTON_TEXT = ("CREATE/UPDATE", "REMOVE")
TASK_FIELD_SIZE = (25, 1)


def task_label(label):
    return sg.Text(label, size=(13, 1), pad=(0, 10))


task_name = [
    task_label("Task name:"),
    sg.Combo(
        sorted([""] + list(garden.tasks)),
        size=TASK_FIELD_SIZE,
        key="-TASK NAME-",
        enable_events=True,
    ),
]

task_progress = [
    task_label("Progress:"),
    sg.Text("", size=(22, 1), relief=SUNKEN, key="-TASK PROGRESS-"),
]

task_next_due = [
    task_label("Next due:"),
    sg.Text("", size=(22, 1), relief=SUNKEN, key="-TASK NEXT DUE-"),
]

add_progress_button = [
    sg.Button("ADD PROGRESS", size=(21, 1), pad=((113.5, 0), (10, 4)))
]

task_first_horizontal_line = [sg.Text("_" * 41, pad=(0, 0))]

task_assignee = [
    sg.Text("Assignee:", size=(13, 1), pad=(0, (16, 10))),
    sg.Input(size=TASK_FIELD_SIZE, key="-TASK ASSIGNEE-", pad=(4, (10, 0))),
]

task_length = [
    sg.Text("Length:", size=(13, 1), pad=(0, (10, 0))),
    sg.Input(size=TASK_FIELD_SIZE, key="-TASK LENGTH-", pad=(4, (10, 0))),
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
        highlight_background_color="#004225",
        key="-TASK LINKED CREATURES-",
    ),
    sg.Listbox(
        values=(sorted(list(garden.plants))),
        select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
        size=(17, 5),
        highlight_background_color="#004225",
        key="-TASK LINKED PLANTS-",
    ),
]

task_status = [
    sg.Text("Status:", size=(8, 1), pad=((2, 0), 10)),
    sg.Combo(["current", "archived"], size=TASK_FIELD_SIZE, key="-TASK STATUS-"),
]

task_notes_label = [sg.Text("Description:", size=(10, 1), pad=(2, 10))]

task_description_field = [
    sg.Multiline(size=(37, 5), pad=(5, (10, 15)), key="-TASK NOTES-")
]

task_start = [
    sg.Text("First due:", size=(8, 1), pad=(3, (13, 0))),
    sg.Input(size=(18, 1), key="-TASK START-", pad=(5, (13, 0))),
    sg.CalendarButton(
        "PICK", format="%d/%m/%Y", pad=((0, 7), (13, 0)), key="-TASK PICK START-"
    ),
]

task_frequency = [
    sg.Text("Frequency:", size=(8, 1), pad=(3, (6, 0))),
    sg.Combo(
        ["daily", "weekly", "monthly", "yearly"],
        size=(18, 1),
        pad=(5, (6, 0)),
        key="-TASK FREQUENCY-",
    ),
]

task_count = [
    sg.Text("Count:", size=(8, 1), pad=(3, (8, 0))),
    sg.Input(size=(18, 1), key="-TASK COUNT-", pad=(5, (8, 0))),
]

task_by_month = [
    sg.Text("By month:", size=(8, 1), pad=(3, (8, 0))),
    sg.Input(size=(18, 1), key="-TASK BY MONTH-", pad=(5, (8, 0))),
]

task_interval = [
    sg.Text("Interval:", size=(8, 1), pad=(3, (8, 20))),
    sg.Input(size=(18, 1), key="-TASK INTERVAL-", pad=(5, (8, 20))),
]

schedule_contents = [
    task_start,
    task_frequency,
    task_count,
    task_by_month,
    task_interval,
]

task_schedule_frame = [
    sg.Frame(
        "Schedule",
        schedule_contents,
        relief=GROOVE,  # SUNKEN, RAISED, RIDGE, GROOVE
        border_width=2,
        size=(25, 5),
    )
]

task_buttons = [
    sg.Button(name, size=(15, 2), pad=((4, 4), (22, 0)), key=f"TASK {name}")
    for name in TASK_BUTTON_TEXT
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

# fmt: off
layout = [[sg.Menu(menu_definition)], [sg.TabGroup(all_tabs, tab_background_color="#004225")]]
# fmt: on
# Create the window
window = sg.Window(
    "gardenlife", layout, keep_on_top=True, enable_close_attempted_event=True
)


# ----------------------------------- Event Loop ----------------------------------- #


# Keeps track of whether any changes have been made since the garden was saved
garden_changed = False

# Display and interact with the window using an event loop
while True:
    event, values = window.read()
    print(event, values)

    ########################### Menu & Window Closure Events ###########################

    # See if user wants to quit or attempted to close the window
    if event in ("Exit", sg.WINDOW_CLOSE_ATTEMPTED_EVENT):

        if garden_changed:
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
                "Confirm", confirm_layout, keep_on_top=True, element_justification="center"
            )

            while True:
                confirm_event, confirm_values = confirm_window.read()
                print(confirm_event, confirm_values)

                if confirm_event == "Save":
                    with open("garden.pickle", "wb") as file:
                        pickle.dump(garden, file)
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
        with open("garden.pickle", "wb") as file:
            pickle.dump(garden, file)
        garden_changed = False

    ######################### Garden Summary Events ########################

    # Add report events here

    ######################### Manage Garden Events #########################

    elif event == "UPDATE GARDEN":
        # Update the garden instance
        garden.name = values["-GARDEN NAME-"]
        garden.location = values["-LOCATION-"]
        garden.size = values["-SIZE-"]
        garden.owners = values["-OWNER NAMES-"].split()
        garden.since = values["-OWNED SINCE-"]
        # Then update the associated summary fields
        window["-SUMMARY GARDEN NAME-"].update(garden.name)
        window["-SUMMARY LOCATION-"].update(garden.location)
        window["-SUMMARY SIZE-"].update(garden.garden_size())
        window["-SUMMARY OWNED BY-"].update(garden.ownership())
        window["-SUMMARY OWNED FOR-"].update(garden.ownership_length())
        garden_changed = True

    ####################### Manage Creatures Events ########################

    def clear_creature_values():
        for value in ("NAME", "TYPE", "AGE", "APPEARED DATE", "STATUS", "NOTES"):
            window[f"-CREATURE {value}-"].update("")
        for value in ("IMPACT", "PREVALENCE", "TREND"):
            window[f"-CREATURE {value} SLIDER-"].update(3)

    def creature_instance():
        return garden.creatures[values["-CREATURE NAME-"]]

    def update_creature_dropdowns():
        creature_names = sorted([""] + list(garden.creatures))
        creature_types = sorted(
            [""] + [creature.creature_type for creature in garden.creatures.values()]
        )
        return (
            window["-CREATURE NAME-"].update(values=creature_names, size=(25, 10)),
            window["-CREATURE TYPE-"].update(values=creature_types, size=(25, 10)),
        )


    if event == "CREATURE CREATE/UPDATE":
        creature = Creature(
            creature_name=values["-CREATURE NAME-"],
            creature_type=values["-CREATURE TYPE-"],
            age=values["-CREATURE AGE-"],
            appeared=values["-CREATURE APPEARED DATE-"],
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
        garden_changed = True

    elif event == "CREATURE REMOVE":
        garden.remove_item("creatures", values["-CREATURE NAME-"])
        update_creature_dropdowns()
        clear_creature_values()
        window["-SUMMARY TOTAL CREATURES-"].update(len(garden.creatures))
        garden_changed = True

    elif values["-CREATURE NAME-"] == "":
        clear_creature_values()

    # If a creature is selected populate the relevant fields with its values
    elif values["-CREATURE NAME-"]:  # Something is highlighted in the dropdown
        window["-CREATURE TYPE-"].update(creature_instance().creature_type)
        window["-CREATURE AGE-"].update(creature_instance().age)
        window["-CREATURE APPEARED DATE-"].update(creature_instance().appeared)
        window["-CREATURE STATUS-"].update(creature_instance().status.get())
        window["-CREATURE NOTES-"].update(creature_instance().notes)
        window["-CREATURE IMPACT SLIDER-"].update(creature_instance().impact)
        window["-CREATURE PREVALENCE SLIDER-"].update(
            creature_instance().prevalence
        )
        window["-CREATURE TREND SLIDER-"].update(creature_instance().trend)

    ######################### Manage Plant Events ##########################

    def clear_plant_values():
        for value in ("NAME", "TYPE", "AGE", "PLANTED DATE", "STATUS", "NOTES"):
            window[f"-PLANT {value}-"].update("")
        for value in ("IMPACT", "PREVALENCE", "TREND"):
            window[f"-PLANT {value} SLIDER-"].update(3)

    def plant_instance():
        return garden.plants[values["-PLANT NAME-"]]

    def update_plant_dropdowns():
        plant_names = sorted([""] + list(garden.plants))
        plant_types = sorted(
            [""] + [plant.plant_type for plant in garden.plants.values()]
        )
        return (
            window["-PLANT NAME-"].update(values=plant_names, size=(25, 10)),
            window["-PLANT TYPE-"].update(values=plant_types, size=(25, 10)),
        )


    if event == "PLANT CREATE/UPDATE":
        plant = Plant(
            plant_name=values["-PLANT NAME-"],
            plant_type=values["-PLANT TYPE-"],
            age=values["-PLANT AGE-"],
            planted=values["-PLANT PLANTED DATE-"],
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
        garden_changed = True

    elif event == "PLANT REMOVE":
        garden.remove_item("plants", values["-PLANT NAME-"])
        update_plant_dropdowns()
        clear_plant_values()
        window["-SUMMARY TOTAL PLANTS-"].update(len(garden.plants))
        garden_changed = True

    elif values["-PLANT NAME-"] == "":
        clear_plant_values()

    # If a plant is selected populate the relevant fields with its values
    elif values["-PLANT NAME-"]:  # Something is highlighted in the dropdown
        window["-PLANT TYPE-"].update(plant_instance().plant_type)
        window["-PLANT AGE-"].update(plant_instance().age)
        window["-PLANT PLANTED DATE-"].update(plant_instance().planted)
        window["-PLANT STATUS-"].update(plant_instance().status.get())
        window["-PLANT NOTES-"].update(plant_instance().notes)
        window["-PLANT IMPACT SLIDER-"].update(plant_instance().impact)
        window["-PLANT PREVALENCE SLIDER-"].update(plant_instance().prevalence)
        window["-PLANT TREND SLIDER-"].update(plant_instance().trend)

    ########################## Manage Task Events ##########################
    
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

    def task_instance():
        return garden.tasks.get(values["-TASK NAME-"])

    def update_task_dropdown():
        task_names = sorted([""] + list(garden.tasks))
        return window["-TASK NAME-"].update(values=task_names, size=(25, 10))

    def clear_organism_links():
        window["-TASK LINKED CREATURES-"].update(sorted(list(garden.creatures)))
        window["-TASK LINKED PLANTS-"].update(sorted(list(garden.plants)))

    if event == "TASK CREATE/UPDATE":
        task = Task(
            task_name=values["-TASK NAME-"],
            assignee=values["-TASK ASSIGNEE-"],
            length=values["-TASK LENGTH-"],
            linked_creatures=values["-TASK LINKED CREATURES-"],
            linked_plants=values["-TASK LINKED PLANTS-"],
            description=values["-TASK NOTES-"],
        )

        if values["-TASK STATUS-"] == "archived":
            task.status.archive()

        task.set_schedule(
            start_date=values["-TASK START-"],
            freq=values["-TASK FREQUENCY-"],
            count=values["-TASK COUNT-"],
            bymonth=values["-TASK BY MONTH-"],
            interval=values["-TASK INTERVAL-"],
        )
        # If the task already exists add any pre-existing completed dates to it
        if task_instance():
            task.completed_dates = task_instance().completed_dates
        # Add the task to the garden, overwriting the old version if it already exists
        garden.add_item("tasks", task)
        # Clear the task variable once the task has been added to the garden
        update_task_dropdown()
        clear_task_values()
        clear_organism_links()
        # Update the total tasks number shown on the summary tab
        window["-SUMMARY TOTAL TASKS-"].update(len(garden.tasks))
        garden_changed = True

    elif event == "TASK REMOVE":
        garden.remove_item("tasks", values["-TASK NAME-"])
        update_task_dropdown()
        clear_task_values()
        clear_organism_links()
        window["-SUMMARY TOTAL TASKS-"].update(len(garden.tasks))
        garden_changed = True

    elif values["-TASK NAME-"] == "":
        clear_task_values()
        clear_organism_links()

    elif event == "ADD PROGRESS":
        if "task" in globals():  # Prevents crashes if add progress clicked before task creation
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

            progress_window = sg.Window(
                "Add Progress", progress_layout, keep_on_top=True
            )

            while True:
                progress_event, progress_values = progress_window.read()
                print(progress_event, progress_values)

                if progress_event == "Add":
                    task.update_completed_dates(progress_values)

                if progress_event in (sg.WIN_CLOSED, "Add"):
                    progress_window.close()
                    window.Enable()
                    break

    elif values["-TASK NAME-"]:  # Something is highlighted in the dropdown
        # When a task is selected populate the relevant fields with its values
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

    ########################################################################

# Finish up by removing from the screen
window.close()
