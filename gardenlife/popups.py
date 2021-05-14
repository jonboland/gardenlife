import traceback

import PySimpleGUI as sg


def fatal_error(error):
    sg.popup(
        "Sorry for the disruption.",
        "Unfortunately, gardenlife has stopped working because the following fatal error occured:",
        error,
        traceback.format_exc(),
        title="Fatal Error",
        keep_on_top=True,
    )


def about():
    sg.popup(
        "gardenlife v1.0\n\n" "A garden management application created by Jon Boland.\n",
        title="About...",
        keep_on_top=True,
    )


def garden_not_selected(item):
    return sg.popup(
        f"It wasn't possible to add the {item} because a garden hasn't been selected. "
        "Please choose a garden on the Manage Garden tab and try again.",
        title="Garden Not Selected Error",
        keep_on_top=True,
    )


def task_not_created():
    sg.popup(
        "The task must be created before progress is added.\n",
        title="Task Not Created Error", 
        keep_on_top=True,
    )


def remove_confirmation(name, element):
    return sg.popup_ok_cancel(
        f"Are you sure you want to remove {name}?",
        f"This {element} will be permanently deleted.\n",
        "Click OK if you wish to proceed.\n",
        title="Remove Confirmation",
        keep_on_top=True,
    )


def invalid_name(field):
    return sg.popup(
        f"The {field} field cannot be blank. Please add a name and try again.",
        title="Blank Name Error",
        keep_on_top=True,
    )


def invalid_date(field, date):
    return sg.popup(
        f"The {field} field contains {date}, which is not a valid date. "
        "The format should be DD/MM/YYYY. Please correct and try again.",
        title="Date Format Error",
        keep_on_top=True,
    )


def invalid_digit(field, digit):
    return sg.popup(
        f"The {field} field contains {digit}, which is not a valid digit. "
        "Please correct and try again.",
        title="Digit Error",
        keep_on_top=True,
    )


def invalid_bymonth(bymonth):
    return sg.popup(
        f'The by month field contains "{bymonth}", which includes an invalid month or months. '
        "Months must be digits between 1 and 12, separated by a single space.",
        "Please correct and try again.",
        title="Month Format Error",
        keep_on_top=True,
    )


def no_due_dates():
    return sg.popup(
        "Based on the current schedule, there are no due dates for this task. "
        "Please alter the schedule and try again.",
        title="No Due Dates Error",
        keep_on_top=True,
    )
