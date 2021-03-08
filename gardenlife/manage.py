from calendar import Calendar
import pickle
from tkinter.constants import SUNKEN

import PySimpleGUI as sg

from garden import Garden
from organisms import Creature, Plant
from task import Task


sg.theme(new_theme="LightGray1")


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
    "Size:": f"{garden.size} acres",
    "Owned by:": garden.ownership(),
    "Owned for:": garden.ownership_length(),
    "Total creatures:": len(garden.creatures),
    "Total plants:": len(garden.plants),
    "Total tasks:": len(garden.tasks),
    "Outstanding tasks:": 0,
}


summary = [
    [
        sg.Text(label, size=(15, 1), pad=(0, 10), justification="right"),
        sg.Text(
            value,
            size=(30, 1),
            relief=SUNKEN,
            # enable_events=True,
            key=f"-SUMMARY {label[:-1].upper()}-",
        ),
    ]
    for label, value in summary_details.items()
]


report_buttons = [
    [
        sg.Button(
            name,
            size=(20, 2),
            pad=(0, 10),
            border_width=2,
            button_color="white on #004225",
        )
    ]
    for name in REPORT_BUTTON_TEXT
]


summary_tab = [
    [
        sg.Text("", size=(1, 20)),  # Blank row to set column sizes
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


garden_elements = [
    [
        garden_label_format("Select garden:"),
        sg.Combo([], default_value=garden.name, size=(30, 1), key="-SELECT GARDEN-"),
    ]
]

garden_elements += [[sg.Text("", size=(0, 1))]]  # Blank row to add space below selector

garden_elements += [
    [
        garden_label_format(label),
        sg.Input(value, size=(30, 1), key=f"-{label[:-1].upper()}-"),
    ]
    for label, value in garden_details.items()
]

garden_elements += [
    [
        sg.Button(
            name,
            size=(15, 2),
            pad=((43, 0), 30),
            button_color="white on #004225",
        )
        for name in GARDEN_BUTTON_TEXT
    ]
]


garden_tab = [[sg.Column(garden_elements, pad=((30, 40), 40))]]


# ------------------------------ Manage Creatures Tab ------------------------------ #


CREATURE_BUTTON_TEXT = ("CREATE CREATURE", "UPDATE CREATURE")


creature_details = {
    "Creature name:": 0,
    "Creature type:": 0,
    "Appeared date:": 0,
    "Age:": 0,
    "Status:": 0,
}


def creature_label_format(label):
    return sg.Text(label, size=(15, 1), pad=(0, 10), justification="right")


creature_elements = [
    [
        creature_label_format("Creature name:"),
        sg.Combo(
            [creature for creature in garden.creatures],
            default_value=0,
            size=(30, 1),
            key="-CREATURE NAME-",
        ),
    ]
]


creature_elements += [
    [
        creature_label_format("Creature type:"),
        sg.Combo(
            ["one", "two", "three"],
            default_value=0,
            size=(30, 1),
            key="-CREATURE TYPE-",
        ),
    ]
]


creature_elements += [
    [
        creature_label_format("Appeared date:"),
        sg.Input(size=(30, 1), key="-APPEARED DATE-"),
        sg.CalendarButton("PICK", button_color="white on #004225", format="%d/%m/%Y"),
    ]
]


creature_elements += [
    [
        creature_label_format("Age:"),
        sg.Input(size=(30, 1), key="-CREATURE AGE-"),
    ]
]


creature_elements += [
    [
        sg.Button(
            name,
            size=(18, 2),
            pad=((43, 0), 30),
            button_color="white on #004225",
            # key=f"-CREATE {name}-",
        )
        for name in CREATURE_BUTTON_TEXT
    ]
]


creatures_tab = [[sg.Column(creature_elements, pad=((30, 40), 40))]]


# -------------------------------- Manage Plants Tab ------------------------------- #


plants_tab = [[sg.Text("This is inside tab 4")], [sg.Input(key="in3")]]


# -------------------------------- Manage Tasks Tab -------------------------------- #


tasks_tab = [[sg.Text("This is inside tab 5")], [sg.Input(key="in4")]]

# task_elements += [
#     [
#         sg.Listbox(values=('Listbox Item 1', 'Listbox Item 2', 'Listbox Item 3'),
#         select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED, size=(30, 5), key="-LINKED CREATURES-"),
#     ]
# ]


# ----------------------------------- Main Layout ---------------------------------- #


tab_details = {
    "Garden Summary": summary_tab,
    "Manage Garden": garden_tab,
    "Manage Creatures": creatures_tab,
    "Manage Plants": plants_tab,
    "Manage Tasks": tasks_tab,
}


all_tabs = [[sg.Tab(label, tab, pad=(10, 10)) for label, tab in tab_details.items()]]


layout = [[sg.Menu(menu_definition)], [sg.TabGroup(all_tabs)]]

# Create the window
window = sg.Window("gardenlife", layout, keep_on_top=True)


# ----------------------------------- Event Loop ----------------------------------- #


# Display and interact with the Window using an Event Loop
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
        window["-SUMMARY SIZE-"].update(f"{garden.size} acres")
        window["-SUMMARY OWNED BY-"].update(garden.ownership())
        window["-SUMMARY OWNED FOR-"].update(garden.ownership_length())

    ####################### Manage Creatures Events ########################

    elif event == "CREATE CREATURE":
        pass


    ######################### Manage Plant Events ##########################

    ########################## Manage Task Events ##########################

# Finish up by removing from the screen

window.close()
