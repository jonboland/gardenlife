from organism import Organism


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
            status="current",
            organism_kind="plant",
        )
        self.plant_type = plant_type  # Eg Tree, Vegetable, Flower, Weed
        self.plant_name = plant_name  # Eg Ash, Bean, Poppy, Thistle
        self.planted = planted

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
