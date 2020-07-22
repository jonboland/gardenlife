from datetime import datetime, date
from time import strftime


class Garden:
    """Class to represent a garden."""

    def __init__(self, name, location, size, since, *owners):
        self.name = name
        self.location = location
        self.size = size
        self.owners = owners
        self.since = since
        self.creatures = []
        self.plants = []
        self.tasks = []

    def __repr__(self):
        return (
            f"{self.__class__.__name__} in {self.location} called {self.name}, "
            f"which is approximately {self.size} acres in size."
        )

    def ownership(self):
        """Return who currently owns the garden."""
        if len(self.owners) == 1:
            return f"The owner of {self.name} is {self.owners[0]}."
        elif len(self.owners) == 2:
            return f"The owners of {self.name} are {' and '.join(self.owners)}."
        return (
            f"The owners of {self.name} are {', '.join(self.owners[:-1])} "
            f"and {self.owners[-1]}."
        )

    def ownership_length(self, today=str(date.today())):
        """Return current garden ownership length in days."""
        now = datetime.strptime(today, "%Y-%m-%d")
        ago = datetime.strptime(self.since, "%d/%m/%Y")
        dif = now - ago
        years, days = divmod(dif.days, 365)
        print(years, days)
        if days > 270:
            years += 1
        elif days > 90:
            years += 0.5
        return (
            f"{self.name} has been in the same hands for {dif.days:,d} days.\n"
            f"That's about {years} years."
        )

    @classmethod
    def from_string(cls, garden_details):
        """Construct a garden from a hyphen separated string."""
        name, location, size, since, *owners = garden_details.split("-")
        return cls(name, location, size, since, *owners)

    @staticmethod
    def season(current_month=strftime("%B")):
        """Return the current season."""
        seasons = {
            "Spring": ["March", "April", "May"],
            "Summer": ["June", "July", "August"],
            "Autumn": ["September", "October", "November"],
            "Winter": ["December", "January", "February"],
        }
        for season, months in seasons.items():
            if current_month in months:
                return season
