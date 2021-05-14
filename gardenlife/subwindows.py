import pickle
import sys

import PySimpleGUI as sg

from constants import ACCENT_COLOR, CREATURE_HEADS, PLANT_HEADS, TASK_HEADS
import summary_funcs

 
def unsaved_changes_window(window, gardens):
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
        # print(confirm_event, confirm_values)

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


def add_progress_window(window, task):
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
        # print(progress_event, progress_values)

        if progress_event == "Add":
            task.update_completed_dates(progress_values)

        if progress_event in (sg.WIN_CLOSED, "Add"):
            progress_window.close()
            window.Enable()
            break


def view_creatures_window(window, garden):
    window.Disable()

    header_row = [[summary_funcs.summary_head_format(title) for title in CREATURE_HEADS]]

    creatures = [
        summary_funcs.creature_fields(creature)
        for creature in summary_funcs.sorted_organisms(garden.creatures.values(), sort_key="name")
    ]

    creature_table = header_row + creatures

    creature_summary_column = [summary_funcs.organism_column_format(creature_table)]

    creature_summary_layout = [creature_summary_column, [sg.Button("Close")]]

    creature_summary_window = sg.Window("Creature Summary", creature_summary_layout, keep_on_top=True)

    while True:
        creature_sum_event, creature_sum_values = creature_summary_window.read()
        # print(creature_sum_event, creature_sum_values)

        if creature_sum_event in (sg.WIN_CLOSED, "Close"):
            creature_summary_window.close()
            window.Enable()
            break


def view_plants_window(window, garden, attr):
    window.Disable()

    header_row = [[summary_funcs.summary_head_format(title) for title in PLANT_HEADS]]

    plants = [
        summary_funcs.plant_fields(plant)
        for plant in summary_funcs.sorted_organisms(garden.plants.values(), sort_key="name")
        if getattr(plant, attr)
    ]

    plant_table = header_row + plants

    plant_summary_column = [summary_funcs.organism_column_format(plant_table)]

    plant_summary_layout = [plant_summary_column, [sg.Button("Close")]]

    plant_summary_window = sg.Window("Plant Summary", plant_summary_layout, keep_on_top=True)

    while True:
        plant_sum_event, plant_sum_values = plant_summary_window.read()
        # print(plant_sum_event, plant_sum_values)

        if plant_sum_event in (sg.WIN_CLOSED, "Close"):
            plant_summary_window.close()
            window.Enable()
            break


def view_tasks_window(window, garden):
    window.Disable()

    name_head = [
        sg.Input(
            TASK_HEADS[0], size=(18, 1), text_color="white", background_color=ACCENT_COLOR
        )
    ]

    other_head = [summary_funcs.summary_head_format(title) for title in TASK_HEADS[1:]]

    header_row = [name_head + other_head]

    tasks = [
        summary_funcs.task_fields(task) for task in summary_funcs.sorted_tasks(garden.tasks.values())
    ]

    task_table = header_row + tasks

    task_summary_column = [sg.Column(task_table, size=(880, 500), scrollable=True)]

    task_summary_layout = [task_summary_column, [sg.Button("Close")]]

    task_summary_window = sg.Window("Task Summary", task_summary_layout, keep_on_top=True)

    while True:
        task_sum_event, task_sum_values = task_summary_window.read()
        # print(task_sum_event, task_sum_values)

        if task_sum_event in (sg.WIN_CLOSED, "Close"):
            task_summary_window.close()
            window.Enable()
            break
