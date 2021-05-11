from datetime import datetime
from time import strftime


SEASONS = {
    "Spring": ["March", "April", "May"],
    "Summer": ["June", "July", "August"],
    "Autumn": ["September", "October", "November"],
    "Winter": ["December", "January", "February"],
}


class Garden:
    """Class to represent a garden."""

    def __init__(self, name, location, size, since, owners):
        self.name = name
        self.location = location
        self.size = size
        self.since = since
        self.owners = owners
        self.creatures = dict()
        self.plants = dict()
        self.tasks = dict()
        self.timestamp = datetime.today()

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.name}, {self.location}, "
            f"{self.size}, {self.owners}, {self.since})"
        )

    def __str__(self):
        return (
            f"{self.__class__.__name__} in {self.location} called {self.name}, "
            f"which is approximately {self.garden_size()} in size."
        )

    def ownership(self):
        """Return who currently owns the garden."""
        if len(self.owners) == 1:
            return f"{self.owners[0]}"
        if len(self.owners) == 2:
            return f"{' and '.join(self.owners)}"
        return (
            f"{', '.join(self.owners[:-1])} and {self.owners[-1]}"
        )

    def ownership_length(self, today=None):
        """Return garden ownership length."""
        if not today:
            now = datetime.today()
        else:
            now = datetime.strptime(today, "%d/%m/%Y")
        ago = datetime.strptime(self.since, "%d/%m/%Y")
        dif = now - ago
        years, days = divmod(dif.days, 365)
        if days > 240:
            years += 1
        elif days > 120:
            years += 0.5
        exact_days = f"{dif.days:,d} days"
        if dif.days == 1:
            exact_days = exact_days.replace("days", "day")
        approx_years = f" (around {years} years)"
        return exact_days + approx_years if years > 2 else exact_days

    def garden_size(self):
        acres = "acre" if self.size in {1, "1"} else "acres"
        return f"{self.size} {acres}"

    @classmethod
    def from_string(cls, garden_details):
        """Construct a garden from a hyphen separated string."""
        name, location, size, since, *owners = garden_details.split("-")
        return cls(name, location, size, since, *owners)

    @staticmethod
    def season(current_month=None):
        """Return the current season."""
        if not current_month:
            current_month = strftime("%B")
        for season, months in SEASONS.items():
            if current_month in months:
                return season

    def add_item(self, category, item):
        """Add a creature, plant or task to the garden. Overwrite if already exists."""
        if category not in {"creatures", "plants", "tasks"}:
            raise ValueError(f"{category} is not a valid category")
        item_type = getattr(self, category)
        item_name = getattr(item, f"{category[:-1]}_name")
        item_type[item_name] = item
        self.timestamp = datetime.today()

    def remove_item(self, category, item):
        """Remove a creature, plant or task from the garden."""
        if category not in {"creatures", "plants", "tasks"}:
            raise ValueError(f"{category} is not a valid category")
        item_type = getattr(self, category)
        if item not in item_type:
            raise ValueError(
                f'The {category[:-1]} "{item}" was not found in this garden.'
            )
        del item_type[item]
        self.timestamp = datetime.today()
