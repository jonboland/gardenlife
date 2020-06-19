from organism import Organism


class Creature(Organism):
    def __init__(
        self,
        creature_type,
        creature_name,
        impact="neutral",
        prevalence="medium",
        trend="stable",
    ):
        super().__init__(impact, prevalence, trend, organism_kind="creature")
        self.creature_type = creature_type  # Eg Mammal, Rodent, Insect, Bird
        self.creature_name = creature_name  # Eg Badger, Mouse, Bee, Pigeon

    def __repr__(self):
        return (
            f"This creature is a {self.creature_name}. "
            f"{self.creature_name.title()}s are {self.creature_type}s."
        )

    def __eq__(self, other):
        return (
            self.creature_type == other.creature_type
            and self.creature_name == other.creature_name
        )
