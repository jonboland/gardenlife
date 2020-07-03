from organism import Organism


class Plant(Organism):
    def __init__(
        self,
        plant_type,
        plant_name,
        age="unknown",
        appeared="unknown",
        impact="neutral",
        prevalence="medium",
        trend="stable",
    ):
        super().__init__(
            age, appeared, impact, prevalence, trend, organism_kind="plant"
        )
        self.plant_type = plant_type  # Eg Tree, Vegetable, Flower, Weed
        self.plant_name = plant_name  # Eg Ash, Bean, Poppy, Thistle

    def __repr__(self):
        if self.plant_name[0] in "aeiou":
            name = f"This plant is an {self.plant_name}"
        else:
            name = f"This plant is a {self.plant_name}"
        return (
            f"{name}, which is a {self.plant_type}."
        )

    def __eq__(self, other):
        return (
            self.plant_type == other.plant_type
            and self.plant_name == other.plant_name
        )
