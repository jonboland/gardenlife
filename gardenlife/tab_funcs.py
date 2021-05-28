"""Tab functions for the gardenlife application."""


import PySimpleGUI as sg


def garden_label_format(label):
    """Return formatted garden label."""
    return sg.Text(label, size=(15, 1), pad=(0, 10), justification="right")


def item_label(label):
    """Return formatted item label."""
    return sg.Text(label, size=(13, 1), pad=(0, 10))


def organism_slider_label(label):
    """Return formatted slider label."""
    return sg.Text(label, size=(12, 1), pad=((0, 8), (20, 0)))


def organism_slider(key=None, tooltip=None):
    """Return a creature or plant slider."""
    return sg.Slider(
        range=(1, 5),
        key=key,
        orientation="horizontal",
        default_value=3,
        size=(19.7, 19),
        tooltip=tooltip,
    )
