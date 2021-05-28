"""Contains classes to represent creatures and plants."""

from organism import Organism


class Creature(Organism):
    """Class to represent a creature."""
    def __init__(self, *args, appeared=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.appeared = appeared

    def __str__(self):
        return f"Creature name: {self.name}. Creature type: {self.org_type}."


class Plant(Organism):
    """Class to represent a plant."""
    def __init__(self, *args, edible=False, planted=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.edible = edible
        self.planted = planted

    def __str__(self):
        return f"Plant name: {self.name}. Plant type: {self.org_type}."
