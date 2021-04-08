from calendar import Calendar
import pickle
from tkinter.constants import SUNKEN, RAISED, RIDGE, GROOVE
import traceback

import PySimpleGUI as sg

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
except (OSError, IOError) as e:
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
        sg.Combo([], default_value=garden.name, size=(30, 1), key="-SELECT GARDEN-"),
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
        size=CREATURE_FIELD_SIZE,
        key="-CREATURE NAME-",
        enable_events=True,
    ),
]
# fmt: off
creature_type = [
    creature_label("Creature type:"),
    sg.Combo(
        sorted([""] + [creature.creature_type for creature in garden.creatures.values()]),
        size=CREATURE_FIELD_SIZE,
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
        size=PLANT_FIELD_SIZE,
        key="-PLANT NAME-",
        enable_events=True,
    ),
]

plant_type = [
    plant_label("Plant type:"),
    sg.Combo(
        sorted([""] + [plant.plant_type for plant in garden.plants.values()]),
        size=PLANT_FIELD_SIZE,
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
    sg.Combo(
        ["outstanding", "in progress", "completed", "completed early"],
        size=TASK_FIELD_SIZE,
        key="-TASK PROGRESS-",
        enable_events=True,
    ),
]

task_last_completed = [
    sg.Text("Last completed:", size=(13, 1), pad=(0, (6, 0))),
    sg.Input(size=TASK_FIELD_SIZE, key="-TASK LAST COMPLETED DATE-", pad=(5, (6, 0))),
    sg.CalendarButton("PICK", format="%d/%m/%Y", pad=(0, (6, 0)), key="-TASK PICK COMPLETED-"),
]

task_next_due = [
    sg.Text("Next due:", size=(13, 1), pad=(0, (10, 0))),
    sg.Text("", size=(22, 1), relief=SUNKEN, pad=(5, (16, 2)), key="-TASK NEXT DUE-"),
]

task_first_horizontal_line = [sg.Text("_" * 41, pad=(0, 0))]

task_first_due = [
    sg.Text("First due:", size=(13, 1), pad=(0, (16, 10))),
    sg.Input(size=TASK_FIELD_SIZE, key="-TASK FIRST DUE DATE-", pad=(5, (6, 0))),
    sg.CalendarButton("PICK", format="%d/%m/%Y", pad=(0, (6, 0)), key="-TASK PICK FIRST DUE-"),
]

task_assignee = [
    task_label("Assignee:"),
    sg.Input(size=TASK_FIELD_SIZE, key="-TASK ASSIGNEE-"),
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
        values=('Listbox Item 1', 'Listbox Item 2', 'Listbox Item 3'),
        select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED, size=(17, 5), pad=((1, 26), 0), key="-LINKED CREATURES-"),
    sg.Listbox(
        values=('Listbox Item 1', 'Listbox Item 2', 'Listbox Item 3'),
        select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED, size=(17, 5), key="-LINKED PLANTS-"),
]

task_status = [
    sg.Text("Status:", size=(8, 1), pad=((2, 0), 10)),
    sg.Combo(["current", "archived"], size=TASK_FIELD_SIZE, key="-TASK STATUS-"),
]

task_notes_label = [sg.Text("Description:", size=(10, 1), pad=(2, 10))]

task_description_field = [sg.Multiline(size=(37, 5), pad=(5, (10, 15)), key="-TASK NOTES-")]

task_repeat_start = [
    sg.Text("Start date:", size=(8, 1), pad=(3, (13, 0))),
    sg.Input(size=(18, 1), key="-TASK REPEAT START DATE-", pad=(5, (13, 0))),
    sg.CalendarButton("PICK", format="%d/%m/%Y", pad=((0, 7), (13, 0)), key="-TASK PICK REPEAT START-"),
]

task_repeat_frequency = [
    sg.Text("Frequency:", size=(8, 1), pad=(3, (6, 0))),
    sg.Combo(["daily", "weekly", "monthly", "yearly"], size=(18, 1), pad=(5, (6, 0)), key="-TASK REPEAT FREQUENCY-"),
]

task_repeat_interval = [
    sg.Text("Interval:", size=(8, 1), pad=(3, (8, 0))),
    sg.Input(size=(18, 1), key="-TASK REPEAT INTERVAL-", pad=(5, (8, 0))),
]

task_repeat_count = [
    sg.Text("Count:", size=(8, 1), pad=(3, (8, 20))),
    sg.Input(size=(18, 1), key="-TASK REPEAT COUNT-", pad=(5, (8, 20))),
]

repeat_contents = [
    task_repeat_start, 
    task_repeat_frequency, 
    task_repeat_interval, 
    task_repeat_count
]

task_repeat_frame = [
    sg.Frame(
        "Repeat schedule", 
        repeat_contents, 
        relief=GROOVE, # SUNKEN, RAISED, RIDGE, GROOVE
        border_width=2,
        size=(25, 5),
    )
]

task_buttons = [
    sg.Button(name, size=(15, 2), pad=((4, 4), (36, 0)), key=f"TASK {name}")
    for name in TASK_BUTTON_TEXT
]

plants_left_column = [
    task_name,
    task_progress,
    task_last_completed,
    task_next_due,
    task_first_horizontal_line,
    task_first_due,
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
    task_repeat_frame,
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
window = sg.Window("gardenlife", layout, keep_on_top=True)


# ----------------------------------- Event Loop ----------------------------------- #


# Display and interact with the window using an event loop
while True:
    event, values = window.read()
    print(event, values)

    ############################## Menu Events ##############################

    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break

    elif event == "Save":
        with open("garden.pickle", "wb") as file:
            pickle.dump(garden, file)

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

    ####################### Manage Creatures Events ########################

    def clear_creature_values():
        for value in ("NAME", "TYPE", "AGE", "APPEARED DATE", "STATUS", "NOTES"):
            window[f"-CREATURE {value}-"].update("")
        for value in ("IMPACT", "PREVALENCE", "TREND"):
            window[f"-CREATURE {value} SLIDER-"].update(3)


    def creature_instance():
        return garden.creatures[values["-CREATURE NAME-"]]


    def update_creature_dropdowns():
        creature_names = sorted([""] + [creature for creature in garden.creatures])
        creature_types = sorted(
            [""] + [creature.creature_type for creature in garden.creatures.values()]
        )
        return (
            window["-CREATURE NAME-"].update(values=creature_names),
            window["-CREATURE TYPE-"].update(values=creature_types),
        )

    # fmt: off
    try:
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

        elif event == "CREATURE REMOVE":
            garden.remove_item("creatures", values["-CREATURE NAME-"])
            update_creature_dropdowns()
            clear_creature_values()
            window["-SUMMARY TOTAL CREATURES-"].update(len(garden.creatures))

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
            window["-CREATURE PREVALENCE SLIDER-"].update(creature_instance().prevalence)
            window["-CREATURE TREND SLIDER-"].update(creature_instance().trend)

    except ValueError as error_description:
        sg.popup(error_description, keep_on_top=True)

    ######################### Manage Plant Events ##########################

    def clear_plant_values():
        for value in ("NAME", "TYPE", "AGE", "PLANTED DATE", "STATUS", "NOTES"):
            window[f"-PLANT {value}-"].update("")
        for value in ("IMPACT", "PREVALENCE", "TREND"):
            window[f"-PLANT {value} SLIDER-"].update(3)


    def plant_instance():
        return garden.plants[values["-PLANT NAME-"]]


    def update_plant_dropdowns():
        plant_names = sorted([""] + [plant for plant in garden.plants])
        plant_types = sorted(
            [""] + [plant.plant_type for plant in garden.plants.values()]
        )
        return (
            window["-PLANT NAME-"].update(values=plant_names),
            window["-PLANT TYPE-"].update(values=plant_types),
        )

    # fmt: off
    try:
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

        elif event == "PLANT REMOVE":
            garden.remove_item("plants", values["-PLANT NAME-"])
            update_plant_dropdowns()
            clear_plant_values()
            window["-SUMMARY TOTAL PLANTS-"].update(len(garden.plants))

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

    except ValueError as error_description:
        sg.popup(error_description, keep_on_top=True)
    # fmt: on

    ########################## Manage Task Events ##########################

    ########################################################################

# Finish up by removing from the screen
window.close()
