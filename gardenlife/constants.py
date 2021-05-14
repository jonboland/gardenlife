from dateutil.rrule import DAILY, WEEKLY, MONTHLY, YEARLY


# general
ACCENT_COLOR = "#004225"

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
        1: "very negative",
        2: "negative",
        3: "neutral",
        4: "positive",
        5: "very positive",
    },
    "prevalence_levels": {
        1: "very low", 
        2: "low", 
        3: "medium", 
        4: "high", 
        5: "very high"
    },
    "trend_levels": {
        1: "rapid decrease",
        2: "decreasing",
        3: "stable",
        4: "increasing",
        5: "rapid increase",
    },
}

# subwindows.py
CREATURE_HEADS = ("Name", "Type", "Appeared", "Impact", "Prevalence", "Trend", "Status")
PLANT_HEADS = ("Name", "Type", "Planted", "Impact", "Prevalence", "Trend", "Status")
TASK_HEADS = ("Name", "Progress", "Next Due", "Assignee", "Length", "Creatures", "Plants", "Status")

# task.py
FREQS = {"daily": DAILY, "weekly": WEEKLY, "monthly": MONTHLY, "yearly": YEARLY}