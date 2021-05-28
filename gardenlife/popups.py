"""
Popups for the gardenlife application.
"""


import traceback

import PySimpleGUI as sg

from constants import ICON, LOGO, VERSION_NUMBER


def fatal_error(error):
    """Display popup containing apology and details when fatal error occurs."""
    sg.popup(
        "Sorry for the disruption.",
        "Unfortunately, gardenlife has stopped working because the following fatal error occured:",
        error,
        traceback.format_exc(),
        title="Fatal Error",
        keep_on_top=True,
    )


def about():
    """Display popup with logo, version number, and creator name."""
    sg.popup(
        f"    {VERSION_NUMBER}\n",
        "    A garden management application created by Jon Boland.\n",
        title="   About...",
        image=LOGO,
        keep_on_top=True,
    )


def garden_not_selected(item):
    """Display popup when user attempts to create an item without a garden selected."""
    sg.popup(
        f"It wasn't possible to create the {item} because a garden hasn't been selected. "
        "Please choose a garden on the Manage Garden tab and try again.",
        title="Garden Not Selected Error",
        keep_on_top=True,
    )


def item_not_created(item, action="it can be removed"):
    """Display popup when an attempted action cannot be completed until the item is created."""
    sg.popup(
        f"The {item} must be created before {action}.",
        title="Item Not Created Error",
        keep_on_top=True,
    )


def remove_confirmation(name, element):
    """
    Display confirmation popup when a remove button is clicked.
    Return response as string value. Either "OK" or "Cancel".
    """
    return sg.popup_ok_cancel(
        f"Are you sure you want to remove {name}?",
        f"This {element} will be permanently deleted.\n",
        "Click OK if you wish to proceed.\n",
        # Added because the global icon doesn't appear to be applied to this popup type
        icon=ICON,
        title="Remove Confirmation",
        keep_on_top=True,
    )


def invalid_name(field):
    """Display popup when an action cannot be completed because a name field is blank."""
    sg.popup(
        f"The {field} field cannot be blank. Please add a name and try again.",
        title="Blank Name Error",
        keep_on_top=True,
    )


def invalid_date(field, date):
    """Display popup when create button clicked and date field contains an invalid date."""
    sg.popup(
        f"The {field} field contains {date}, which is not a valid date. "
        "The format should be DD/MM/YYYY. Please correct and try again.",
        title="Date Format Error",
        keep_on_top=True,
    )


def invalid_digit(field, digit):
    """Display popup when create button clicked and a field contains an invalid digit."""
    sg.popup(
        f"The {field} field contains {digit}, which is not a valid digit. "
        "Please correct and try again.",
        title="Digit Error",
        keep_on_top=True,
    )


def invalid_bymonth(bymonth):
    """Display popup when create button clicked and bymonth field contains an invalid month."""
    sg.popup(
        f'The by month field contains "{bymonth}", which includes an invalid month or months. '
        "Months must be digits between 1 and 12, separated by a single space.",
        "Please correct and try again.",
        title="Month Format Error",
        keep_on_top=True,
    )


def no_due_dates():
    """Display popup in rare situation where provided shedule doesn't produce any due dates."""
    sg.popup(
        "Based on the current schedule, there are no due dates for this task. "
        "Please alter the schedule and try again.",
        title="No Due Dates Error",
        keep_on_top=True,
    )
