from organism import Organism
from status import Status


class Creature(Organism):
    def __init__(
        self,
        creature_type,
        creature_name,
        appeared=None,
        notes=None,
        age=None,
        impact="neutral",
        prevalence="medium",
        trend="stable",
    ):
        super().__init__(
            notes,
            age,
            impact,
            prevalence,
            trend,
            organism_kind="creature",
        )
        self.creature_type = creature_type  # Eg Mammal, Rodent, Insect, Bird
        self.creature_name = creature_name  # Eg Badger, Mouse, Bee, Pigeon
        self.appeared = appeared
        self.status = Status()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.creature_type}, {self.creature_name})"

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
        plant_type,
        plant_name,
        planted=None,
        notes=None,
        age=None,
        impact="neutral",
        prevalence="medium",
        trend="stable",
    ):
        super().__init__(
            notes,
            age,
            impact,
            prevalence,
            trend,
            organism_kind="plant",
        )
        self.plant_type = plant_type  # Eg Tree, Vegetable, Flower, Weed
        self.plant_name = plant_name  # Eg Ash, Bean, Poppy, Thistle
        self.planted = planted
        self.status = Status()

    def __repr__(self):
        if self.plant_name[0] in "aeiou":
            name = f"This plant is an {self.plant_name}"
        else:
            name = f"This plant is a {self.plant_name}"
        return f"{name}, which is a {self.plant_type}."

    def __eq__(self, other):
        return (
            self.plant_type == other.plant_type and self.plant_name == other.plant_name
        )
