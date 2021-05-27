"""
GUI for gardenlife. 

Gardenlife is a garden management app. 
It allows you to keep track of the creatures and plants in your garden (or gardens).
You can also use it to schedule one-off/repeat tasks and record progress.

"""

from calendar import Calendar
from datetime import datetime
from operator import attrgetter
import logging
import pickle
from tkinter.constants import SUNKEN, GROOVE
import webbrowser

import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Column

from constants import ACCENT_COLOR, FIELD_SIZE, IB_TEXT, ICON, MG_FIELD_SIZE, MONTHS, RB_TEXT
from garden import Garden
from organisms import Creature, Plant
from task import Task
import event_funcs
import popups
import subwindows
import tab_funcs


def load_gardens():
    """
    Load the dictionary of gardens if it already exists.
    Otherwise, create it and add the default garden.
    """
    try:
        with open("gardens.pickle", "rb") as file:
            gardens = pickle.load(file)
    except FileNotFoundError:
        gardens = {}
        default_garden = Garden("", "", 0, datetime.today().strftime("%d/%m/%Y"), " ")
        gardens[""] = default_garden

    return gardens


def load_garden(gardens):
    """Load the most recently created/updated garden."""
    return max(gardens.values(), key=attrgetter("timestamp"))


def create_window(gardens, garden):
    """
    Define the layout and create the window.
    Use details from the loaded garden (and gardens dict) to populate fields and dropdowns.
    """
    # -------------------------------------- Theme ------------------------------------- #

    sg.theme(new_theme="LightGray1")
    sg.theme_button_color(("white", ACCENT_COLOR))
    sg.theme_input_background_color("light grey")
    sg.theme_input_text_color("black")
    sg.theme_slider_color(ACCENT_COLOR)
    sg.set_global_icon(ICON)

    # -------------------------------------- Menu -------------------------------------- #

    menu_definition = [["File", ["Save", "Exit"]], ["Help", ["About...", "Open web tutorial"]]]

    # ------------------------------- Garden Summary Tab ------------------------------- #

    summary_details = {
        "Garden name:": garden.name,
        "Location:": garden.location,
        "Size:": garden.garden_size(),
        "Owned by:": garden.ownership(),
        "Owned for:": garden.ownership_length(),
        "Total creatures:": len(garden.creatures),
        "Total plants:": len(garden.plants),
        "Total tasks:": len(garden.tasks),
        "Outstanding tasks:": sum(
            task.get_current_progress() in {"Due", "Overdue", "Very overdue"}
            for task in garden.tasks.values()
        ),
        "Current season:": garden.season(),
    }

    summary = [
        [
            sg.Text(label, size=(15, 1), pad=(0, 10), justification="right"),
            sg.Text(value, size=(30, 1), relief=SUNKEN, key=f"-SUMMARY {label[:-1].upper()}-"),
        ]
        for label, value in summary_details.items()
    ]

    report_buttons = [[sg.Button(name, size=(20, 2), pad=(0, 10), border_width=2)] for name in RB_TEXT]

    summary_tab = [
        [
            sg.Column(summary, pad=((30, 40), 40)),
            sg.Column(report_buttons, size=(200, 260), pad=((25, 40), 0)),
        ]
    ]

    # -------------------------------- Manage Garden Tab ------------------------------- #

    garden_details = {
        "Garden name:": garden.name,
        "Location:": garden.location,
        "Size:": garden.size,
        "Owner names:": " ".join(garden.owners),
    }

    select_garden = [
        tab_funcs.garden_label_format("Select garden:"),
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
            tab_funcs.garden_label_format(label),
            sg.Input(value, size=MG_FIELD_SIZE, key=f"-{label[:-1].upper()}-"),
        ]
        for label, value in garden_details.items()
    ]

    owned_since = [
        tab_funcs.garden_label_format("Owned since:"),
        sg.Input(garden.since, size=MG_FIELD_SIZE, tooltip="DD/MM/YYYY", key="-OWNED SINCE-"),
        sg.CalendarButton("PICK", format="%d/%m/%Y", pad=(0, 0)),
    ]

    garden_buttons = [
        sg.Button(name, size=(18, 2), pad=((32.5, 0), 30), key=f"GARDEN {name}") for name in IB_TEXT
    ]

    garden_elements = [select_garden, garden_blank] + garden_details + [owned_since, garden_buttons]

    garden_tab = [[sg.Column(garden_elements, pad=((30, 40), 40))]]

    # ------------------------------ Manage Creatures Tab ------------------------------ #

    creature_name = [
        tab_funcs.item_label("Creature name:"),
        sg.Combo(
            sorted([""] + list(garden.creatures)),
            size=(25, 10),
            key="-CREATURE NAME-",
            enable_events=True,
        ),
    ]

    creature_type = [
        tab_funcs.item_label("Creature type:"),
        sg.Combo(
            sorted([""] + list(set(c.org_type for c in garden.creatures.values() if c.org_type))),
            size=(25, 10),
            key="-CREATURE TYPE-",
        ),
    ]

    creature_appeared = [
        sg.Text("Appeared date:", size=(13, 1), pad=(0, (6, 30))),
        sg.Input(
            size=FIELD_SIZE, pad=(5, (6, 30)), tooltip="DD/MM/YYYY", key="-CREATURE APPEARED DATE-"
        ),
        sg.CalendarButton("PICK", format="%d/%m/%Y", pad=(0, (6, 30))),
    ]

    creature_impact = [
        tab_funcs.organism_slider_label("Impact level:"),
        tab_funcs.organism_slider(
            key="-CREATURE IMPACT SLIDER-",
            tooltip="Impact levels — 1: Very Negative, 2: Negative, "
            "3: Neutral, 4: Positive, 5: Very Positive",
        ),
    ]

    creature_prevalence = [
        tab_funcs.organism_slider_label("Prevalence level:"),
        tab_funcs.organism_slider(
            key="-CREATURE PREVALENCE SLIDER-",
            tooltip="Prevalence levels — 1: Very Low, 2: Low, " "3: Medium, 4: High, 5: Very High",
        ),
    ]

    creature_trend = [
        tab_funcs.organism_slider_label("Trend level:"),
        tab_funcs.organism_slider(
            key="-CREATURE TREND SLIDER-",
            tooltip="Trend levels — 1: Rapid Decrease, 2: Decreasing, "
            "3: Stable, 4: Increasing, 5: Rapid Increase",
        ),
    ]

    creature_status = [
        sg.Text("Status:", size=(8, 1), pad=(0, 10)),
        sg.Combo(
            ["", "Current", "Archived"],
            size=FIELD_SIZE,
            readonly=True,
            background_color="#F2F2F2",
            key="-CREATURE STATUS-",
        ),
    ]

    creature_notes_label = [sg.Text("Notes:", size=(8, 1), pad=(0, 10))]

    creature_notes_field = [sg.Multiline(size=(35, 10), pad=(0, 10), key="-CREATURE NOTES-")]

    creature_buttons = [
        sg.Button(name, size=(15, 2), pad=((0, 7), (32, 0)), key=f"CREATURE {name}") for name in IB_TEXT
    ]

    creatures_left_column = [
        creature_name,
        creature_type,
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
        tab_funcs.item_label("Plant name:"),
        sg.Combo(
            sorted([""] + list(garden.plants)),
            size=(25, 10),
            key="-PLANT NAME-",
            enable_events=True,
        ),
    ]

    plant_type = [
        tab_funcs.item_label("Plant type:"),
        sg.Combo(
            sorted([""] + list(set(p.org_type for p in garden.plants.values() if p.org_type))),
            size=(25, 10),
            key="-PLANT TYPE-",
        ),
    ]

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
        tab_funcs.organism_slider_label("Impact level:"),
        tab_funcs.organism_slider(
            key="-PLANT IMPACT SLIDER-",
            tooltip="Impact levels — 1: very negative, 2: negative, "
            "3: neutral, 4: positive, 5: very positive",
        ),
    ]

    plant_prevalence = [
        tab_funcs.organism_slider_label("Prevalence level:"),
        tab_funcs.organism_slider(
            key="-PLANT PREVALENCE SLIDER-",
            tooltip="Prevalence levels — 1: very low, 2: low, " "3: medium, 4: high, 5: very high",
        ),
    ]

    plant_trend = [
        tab_funcs.organism_slider_label("Trend level:"),
        tab_funcs.organism_slider(
            key="-PLANT TREND SLIDER-",
            tooltip="Trend levels — 1: rapidly decreasing, 2: decreasing, "
            "3: stable, 4: increasing, 5: rapidly increasing",
        ),
    ]

    plant_status = [
        sg.Text("Status:", size=(8, 1), pad=(0, 10)),
        sg.Combo(
            ["", "Current", "Archived"],
            size=FIELD_SIZE,
            readonly=True,
            background_color="#F2F2F2",
            key="-PLANT STATUS-",
        ),
    ]

    plant_edible = [
        sg.Text("Edible:", size=(8, 1), pad=(0, 10)),
        sg.Checkbox("", pad=(0, 0), key="-PLANT EDIBLE-"),
    ]

    plant_notes_label = [sg.Text("Notes:", size=(8, 1), pad=(0, 10))]

    plant_notes_field = [sg.Multiline(size=(35, 10), pad=(0, 10), key="-PLANT NOTES-")]

    plant_buttons = [
        sg.Button(name, size=(15, 2), pad=((0, 7), (32, 0)), key=f"PLANT {name}") for name in IB_TEXT
    ]

    plants_left_column = [
        plant_name,
        plant_type,
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
        tab_funcs.item_label("Task name:"),
        sg.Combo(
            sorted([""] + list(garden.tasks)),
            size=FIELD_SIZE,
            key="-TASK NAME-",
            enable_events=True,
        ),
    ]

    task_progress = [
        tab_funcs.item_label("Progress:"),
        sg.Text("", size=(22, 1), relief=SUNKEN, key="-TASK PROGRESS-"),
    ]

    task_next_due = [
        tab_funcs.item_label("Next due:"),
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
            ["", "Current", "Archived"],
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
            ["", "Daily", "Weekly", "Monthly", "Yearly"],
            size=(18, 1),
            pad=(5, (6, 0)),
            readonly=True,
            background_color="#F2F2F2",
            tooltip="Defaults to monthly if no selection made",
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
        sg.Button(name, size=(15, 2), pad=((4, 4), (22, 0)), key=f"TASK {name}") for name in IB_TEXT
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
    return sg.Window("Gardenlife", layout, keep_on_top=True, enable_close_attempted_event=True)


##########################################################################################


def run_event_loop(logger, gardens, garden, window):
    """Display and interact with the main window and subwindows using an event loop."""

    # Keeps track of whether any changes have been made since the gardens dict was saved
    gardens_changed = False

    try:
        while True:
            event, values = window.read()
            print(event, values)

            ##################### Menu & Window Closure Events #####################

            # See if user wants to quit or attempted to close the window
            if event in ("Exit", sg.WINDOW_CLOSE_ATTEMPTED_EVENT):

                if gardens_changed:
                    subwindows.unsaved_changes_window(window, gardens)
                else:
                    break

            elif event == "Save":
                with open("gardens.pickle", "wb") as file:
                    pickle.dump(gardens, file)
                gardens_changed = False

            elif event == "About...":
                popups.about()

            elif event == "Open web tutorial":
                webbrowser.open("https://github.com/jonboland/gardenlife/blob/master/README.rst")

            ################ Creature, Plant, & Task Summary Events ################

            elif event == "VIEW ALL CREATURES":
                subwindows.view_creatures_window(window, garden)

            elif event == "VIEW ALL PLANTS":
                subwindows.view_plants_window(window, garden, "name")

            elif event == "VIEW EDIBLE PLANTS":
                subwindows.view_plants_window(window, garden, "edible")

            elif event == "VIEW ALL TASKS":
                subwindows.view_tasks_window(window, garden)

            ######################### Manage Garden Events #########################

            if event == "GARDEN CREATE/UPDATE":
                # Validate garden name and ownership info
                g_name = values["-GARDEN NAME-"].strip()
                g_owners = values["-OWNER NAMES-"].strip()
                g_since = values["-OWNED SINCE-"].strip()
                if not g_name:
                    popups.invalid_name("garden name")
                    continue
                if not g_owners:
                    popups.invalid_name("owner names")
                    continue
                try:
                    event_funcs.check_date_validity(g_since)
                except ValueError:
                    popups.invalid_date(field="owned since", date=g_since)
                # If there are no validation errors, create/update the garden
                else:
                    cu_garden = Garden(
                        g_name, values["-LOCATION-"], values["-SIZE-"], g_since, g_owners.split()
                    )
                    # If garden already exists add all existing items to the updated version
                    garden_instance = gardens.get(g_name)
                    if garden_instance:
                        cu_garden.creatures = garden_instance.creatures
                        cu_garden.plants = garden_instance.plants
                        cu_garden.tasks = garden_instance.tasks
                    # Add created/updated garden to gardens dict. Overwrite if already exists
                    gardens[g_name] = cu_garden
                    # Update dropdowns and clear field values and links
                    event_funcs.update_garden_dropdown(window, gardens)
                    event_funcs.clear_all_item_dropdowns(window)
                    event_funcs.clear_all_values_and_links(window, garden)
                    gardens_changed = True

            elif event == "GARDEN REMOVE":
                g_confirmation = popups.remove_confirmation(garden.name, "garden")
                if g_confirmation == "OK":
                    del gardens[values["-GARDEN NAME-"]]
                    event_funcs.update_garden_dropdown(window, gardens)
                    event_funcs.clear_all_item_dropdowns(window)
                    event_funcs.clear_all_values_and_links(window, garden)
                    gardens_changed = True

            elif event == "-SELECT GARDEN-":  # A garden is selected from the dropdown
                # Load the selected garden
                garden = gardens[values["-SELECT GARDEN-"]]
                # If the default garden (blank row) is selected, clear fields
                if not values["-SELECT GARDEN-"]:
                    event_funcs.clear_garden_values(window)
                    event_funcs.clear_summary_values(window)
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
                    window["-SUMMARY OUTSTANDING TASKS-"].update(
                        sum(
                            task.get_current_progress() in {"Due", "Overdue", "Very overdue"}
                            for task in garden.tasks.values()
                        )
                    )
                # Then update the item dropdowns and clear item field values and links
                event_funcs.update_all_item_dropdowns(window, garden)
                event_funcs.clear_all_item_values_and_links(window, garden)

            ####################### Manage Creatures Events ########################

            if event == "CREATURE CREATE/UPDATE":
                # Validate garden name, creature name and appeared date
                c_name = values["-CREATURE NAME-"].strip()
                c_appeared = values["-CREATURE APPEARED DATE-"].strip()
                # Check that a garden has been selected
                if not values["-SELECT GARDEN-"]:
                    popups.garden_not_selected("creature")
                    continue
                if not c_name:
                    popups.invalid_name("creature name")
                    continue
                try:
                    if c_appeared:
                        event_funcs.check_date_validity(c_appeared)
                except ValueError:
                    popups.invalid_date(field="appeared date", date=c_appeared)

                else:
                    creature = Creature(
                        name=c_name,
                        org_type=values["-CREATURE TYPE-"],
                        appeared=c_appeared,
                        notes=values["-CREATURE NOTES-"],
                        impact=values["-CREATURE IMPACT SLIDER-"],
                        prevalence=values["-CREATURE PREVALENCE SLIDER-"],
                        trend=values["-CREATURE TREND SLIDER-"],
                    )
                    if values["-CREATURE STATUS-"] == "Archived":
                        creature.status.archive()
                    garden.add_item("creatures", creature)
                    event_funcs.update_creature_dropdowns(window, garden)
                    event_funcs.clear_creature_values(window)
                    window["-SUMMARY TOTAL CREATURES-"].update(len(garden.creatures))
                    gardens_changed = True

            elif event == "CREATURE REMOVE":
                c_confirmation = popups.remove_confirmation(values["-CREATURE NAME-"], "creature")
                if c_confirmation == "OK":
                    garden.remove_item("creatures", values["-CREATURE NAME-"])
                    event_funcs.update_creature_dropdowns(window, garden)
                    event_funcs.clear_creature_values(window)
                    window["-SUMMARY TOTAL CREATURES-"].update(len(garden.creatures))
                    gardens_changed = True

            elif values["-CREATURE NAME-"] == "":
                event_funcs.clear_creature_values(window)

            # If a creature is selected populate the relevant fields with its values
            elif event == "-CREATURE NAME-":
                creature_instance = garden.creatures.get(values["-CREATURE NAME-"])
                window["-CREATURE NAME-"].update(creature_instance.name)
                window["-CREATURE TYPE-"].update(creature_instance.org_type)
                window["-CREATURE APPEARED DATE-"].update(creature_instance.appeared)
                window["-CREATURE STATUS-"].update(creature_instance.status.get())
                window["-CREATURE NOTES-"].update(creature_instance.notes)
                window["-CREATURE IMPACT SLIDER-"].update(creature_instance.impact)
                window["-CREATURE PREVALENCE SLIDER-"].update(creature_instance.prevalence)
                window["-CREATURE TREND SLIDER-"].update(creature_instance.trend)

            ######################### Manage Plant Events ##########################

            if event == "PLANT CREATE/UPDATE":
                # Validate plant name and planted date
                p_name = values["-PLANT NAME-"].strip()
                p_planted = values["-PLANT PLANTED DATE-"].strip()
                # Check that a garden has been selected
                if not values["-SELECT GARDEN-"]:
                    popups.garden_not_selected("plant")
                    continue
                if not p_name:
                    popups.invalid_name("plant name")
                    continue
                try:
                    if p_planted:
                        event_funcs.check_date_validity(p_planted)
                except ValueError:
                    popups.invalid_date(field="planted date", date=p_planted)

                else:
                    plant = Plant(
                        name=p_name,
                        org_type=values["-PLANT TYPE-"],
                        planted=p_planted,
                        edible=values["-PLANT EDIBLE-"],
                        notes=values["-PLANT NOTES-"],
                        impact=values["-PLANT IMPACT SLIDER-"],
                        prevalence=values["-PLANT PREVALENCE SLIDER-"],
                        trend=values["-PLANT TREND SLIDER-"],
                    )
                    if values["-PLANT STATUS-"] == "Archived":
                        plant.status.archive()
                    garden.add_item("plants", plant)
                    event_funcs.update_plant_dropdowns(window, garden)
                    event_funcs.clear_plant_values(window)
                    window["-SUMMARY TOTAL PLANTS-"].update(len(garden.plants))
                    gardens_changed = True

            elif event == "PLANT REMOVE":
                p_confirmation = popups.remove_confirmation(values["-PLANT NAME-"], "plant")
                if p_confirmation == "OK":
                    garden.remove_item("plants", values["-PLANT NAME-"])
                    event_funcs.update_plant_dropdowns(window, garden)
                    event_funcs.clear_plant_values(window)
                    window["-SUMMARY TOTAL PLANTS-"].update(len(garden.plants))
                    gardens_changed = True

            elif values["-PLANT NAME-"] == "":
                event_funcs.clear_plant_values(window)

            # If a plant is selected populate the relevant fields with its values
            elif event == "-PLANT NAME-":
                plant_instance = garden.plants.get(values["-PLANT NAME-"])
                window["-PLANT NAME-"].update(plant_instance.name)
                window["-PLANT TYPE-"].update(plant_instance.org_type)
                window["-PLANT PLANTED DATE-"].update(plant_instance.planted)
                window["-PLANT STATUS-"].update(plant_instance.status.get())
                window["-PLANT EDIBLE-"].update(plant_instance.edible)
                window["-PLANT NOTES-"].update(plant_instance.notes)
                window["-PLANT IMPACT SLIDER-"].update(plant_instance.impact)
                window["-PLANT PREVALENCE SLIDER-"].update(plant_instance.prevalence)
                window["-PLANT TREND SLIDER-"].update(plant_instance.trend)

            ########################## Manage Task Events ##########################

            if event == "TASK CREATE/UPDATE":
                # Check that a garden has been selected
                if not values["-SELECT GARDEN-"]:
                    popups.garden_not_selected("creature")
                    continue
                # Strip and validate task name and set schedule values
                # NB: Frequency is not validated because it's a readonly dropdown
                t_name = values["-TASK NAME-"].strip()
                start_date = values["-TASK START-"].strip()
                count = values["-TASK COUNT-"].strip()
                bymonth = values["-TASK BY MONTH-"].strip()
                interval = values["-TASK INTERVAL-"].strip()
                if not t_name:
                    popups.invalid_name("task name")
                    continue
                try:
                    if start_date:
                        event_funcs.check_date_validity(start_date)
                except ValueError:
                    popups.invalid_date(field="first due", date=start_date)
                    continue
                if count and not count.isdigit():
                    popups.invalid_digit(field="count", digit=count)
                elif bymonth and any(month not in MONTHS for month in bymonth.split(" ")):
                    popups.invalid_bymonth(bymonth)
                elif interval and not interval.isdigit():
                    popups.invalid_digit(field="interval", digit=interval)
                # If there are no validation errors, create/update the task
                else:
                    task = Task(
                        name=t_name,
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
                        popups.no_due_dates()
                        continue

                    if values["-TASK STATUS-"] == "Archived":
                        task.status.archive()
                    # If the task already exists add any pre-existing completed dates to it
                    task_instance = garden.tasks.get(values["-TASK NAME-"])
                    if task_instance:
                        task.completed_dates = task_instance.completed_dates
                    # Add the task to the garden, overwriting the old version if it already exists
                    garden.add_item("tasks", task)
                    event_funcs.update_task_dropdown(window, garden)
                    # Clear the task fields and variable once the task has been added to the garden
                    event_funcs.clear_task_values(window)
                    event_funcs.clear_organism_links(window, garden)
                    task = None
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
                t_confirmation = popups.remove_confirmation(values["-TASK NAME-"], "task")
                if t_confirmation == "OK":
                    garden.remove_item("tasks", values["-TASK NAME-"])
                    event_funcs.update_task_dropdown(window, garden)
                    event_funcs.clear_task_values(window)
                    task = None
                    event_funcs.clear_organism_links(window, garden)
                    window["-SUMMARY TOTAL TASKS-"].update(len(garden.tasks))
                    window["-SUMMARY OUTSTANDING TASKS-"].update(
                        sum(
                            task.get_current_progress() in {"Due", "Overdue", "Very overdue"}
                            for task in garden.tasks.values()
                        )
                    )
                    gardens_changed = True

            elif values["-TASK NAME-"] == "":
                event_funcs.clear_task_values(window)
                event_funcs.clear_organism_links(window, garden)
                task = None

            elif event == "ADD PROGRESS":
                if task:
                    subwindows.add_progress_window(window, task)
                else:
                    popups.task_not_created()
            # If a task is selected populate the relevant fields with its values
            elif event == "-TASK NAME-":
                task_instance = garden.tasks[values["-TASK NAME-"]]
                window["-TASK PROGRESS-"].update(task_instance.get_current_progress())
                window["-TASK NEXT DUE-"].update(task_instance.get_next_due_date())
                window["-TASK ASSIGNEE-"].update(task_instance.assignee)
                window["-TASK LENGTH-"].update(task_instance.length)
                window["-TASK LINKED CREATURES-"].set_value(task_instance.linked_creatures)
                window["-TASK LINKED PLANTS-"].set_value(task_instance.linked_plants)
                window["-TASK STATUS-"].update(task_instance.status.get())
                window["-TASK NOTES-"].update(task_instance.description)
                window["-TASK START-"].update(task_instance.raw_schedule["start date"])
                window["-TASK FREQUENCY-"].update(task_instance.raw_schedule["freq"])
                window["-TASK COUNT-"].update(task_instance.raw_schedule["count"])
                window["-TASK BY MONTH-"].update(task_instance.raw_schedule["bymonth"])
                window["-TASK INTERVAL-"].update(task_instance.raw_schedule["interval"])
                # Assign instance to task variable so progress can be added
                task = task_instance

    # Handle fatal exceptions gracefully and log them in the gardenlife.log file
    except Exception as e:
        logger.exception("Fatal Error")
        popups.fatal_error(e)

    # Finish up by removing from the screen
    window.close()


##########################################################################################


def main():
    """
    Run the gardenlife app.
    
    Set up error logging, load the gardens dict and most recently created/updated garden, 
    create the window, and run the event loop.
    """
    logging.basicConfig(
        filename="gardenlife.log", format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    logger = logging.getLogger(__name__)
    gardens = load_gardens()
    garden = load_garden(gardens)
    window = create_window(gardens, garden)
    run_event_loop(logger, gardens, garden, window)


if __name__ == "__main__":
    main()
