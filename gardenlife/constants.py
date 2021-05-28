"""Constants for the gardenlife application."""

from pathlib import Path

from dateutil.rrule import DAILY, WEEKLY, MONTHLY, YEARLY


ASSETS_PATH = Path(__file__).resolve().parent / "assets"


# general
ACCENT_COLOR = "#004225"
ICON = str(ASSETS_PATH / "gardenlife_icon.ico")
VERSION_NUMBER = "v0.1.0"

# garden.py
SEASONS = {
    "Spring": ["March", "April", "May"],
    "Summer": ["June", "July", "August"],
    "Autumn": ["September", "October", "November"],
    "Winter": ["December", "January", "February"],
}

# manage.py
FIELD_SIZE = (25, 1)
IB_TEXT = ("CREATE/UPDATE", "REMOVE")
MG_FIELD_SIZE = (34, 1)
MONTHS = [str(month) for month in range(1, 13)]
RB_TEXT = ("VIEW ALL CREATURES", "VIEW ALL PLANTS", "VIEW EDIBLE PLANTS", "VIEW ALL TASKS")

# organism.py
LEVELS = {
    "impact_levels": {
        1: "Very Negative",
        2: "Negative",
        3: "Neutral",
        4: "Positive",
        5: "Very Positive",
    },
    "prevalence_levels": {
        1: "Very Low",
        2: "Low",
        3: "Medium",
        4: "High",
        5: "Very High"
    },
    "trend_levels": {
        1: "Rapid Decrease",
        2: "Decreasing",
        3: "Stable",
        4: "Increasing",
        5: "Rapid Increase",
    },
}

# popups.py
LOGO = str(ASSETS_PATH / "gardenlife_logo.png")

# subwindows.py
CREATURE_HEADS = ("Name", "Type", "Appeared", "Impact", "Prevalence", "Trend", "Status")
PLANT_HEADS = ("Name", "Type", "Planted", "Impact", "Prevalence", "Trend", "Status")
TASK_HEADS = ("Name", "Progress", "Next Due", "Assignee", "Length", "Creatures", "Plants", "Status")

# task.py
FREQS = {"Daily": DAILY, "Weekly": WEEKLY, "Monthly": MONTHLY, "Yearly": YEARLY}
