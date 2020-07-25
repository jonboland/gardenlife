from organism import Organism


class Creature(Organism):
    def __init__(
        self,
        creature_type,
        creature_name,
        appeared="unknown",
        age="unknown",
        impact="neutral",
        prevalence="medium",
        trend="stable",
    ):
        super().__init__(age, impact, prevalence, trend, organism_kind="creature")
        self.creature_type = creature_type  # Eg Mammal, Rodent, Insect, Bird
        self.creature_name = creature_name  # Eg Badger, Mouse, Bee, Pigeon
        self.appeared = appeared

    def __repr__(self):
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
