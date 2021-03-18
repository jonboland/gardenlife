from organism import Organism
from status import Status


class Creature(Organism):
    def __init__(
        self,
        creature_name,
        creature_type,
        appeared=None,
        notes=None,
        age=None,
        impact=3,
        prevalence=3,
        trend=3,
    ):
        super().__init__(
            notes,
            age,
            impact,
            prevalence,
            trend,
            organism_kind="creature",
        )
        self.creature_name = creature_name  # Eg Badger, Mouse, Bee, Pigeon
        self.creature_type = creature_type  # Eg Mammal, Rodent, Insect, Bird
        self.appeared = appeared
        self.status = Status()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.creature_name}, {self.creature_type})"

    def __str__(self):
        if self.creature_name[0] in "aeiou":
            name = f"This creature is an {self.creature_name}"
        else:
            name = f"This creature is a {self.creature_name}"
        return f"{name}, which is a {self.creature_type}."

    def __eq__(self, other):
        return (
            self.creature_type == other.creature_type
            and self.creature_name == other.creature_name
        )


class Plant(Organism):
    def __init__(
        self,
        plant_name,
        plant_type,
        planted=None,
        notes=None,
        age=None,
        impact=3,
        prevalence=3,
        trend=3,
    ):
        super().__init__(
            notes,
            age,
            impact,
            prevalence,
            trend,
            organism_kind="plant",
        )
        self.plant_name = plant_name  # Eg Ash, Bean, Poppy, Thistle
        self.plant_type = plant_type  # Eg Tree, Vegetable, Flower, Weed
        self.planted = planted
        self.status = Status()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.plant_name}, {self.plant_type})"

    def __str__(self):
        if self.plant_name[0] in "aeiou":
            name = f"This plant is an {self.plant_name}"
        else:
            name = f"This plant is a {self.plant_name}"
        return f"{name}, which is a {self.plant_type}."

    def __eq__(self, other):
        return (
            self.plant_type == other.plant_type and self.plant_name == other.plant_name
        )
