from status import Status


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


class Organism:
    def __init__(
        self, 
        name,  # Eg Badger, Mouse, Ash, Leek 
        org_type,  # Eg Mammal, Rodent, Tree, Vegetable
        notes=None,
        age=None,
        impact=3,
        prevalence=3,
        trend=3,
    ):
        self.name = name
        self.org_type = org_type
        self.notes = notes
        self.age = age
        self.impact = impact
        self.prevalence = prevalence
        self.trend = trend
        self.status = Status()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.org_type})"

    def __eq__(self, other):
        return self.org_type == other.org_type and self.name == other.name

    @property
    def impact(self):
        return self._impact

    @impact.setter
    def impact(self, impact):
        if impact not in range(1, 6):
            raise ValueError(f"{impact} is not a valid impact level")
        self._impact = impact

    @property
    def prevalence(self):
        return self._prevalence

    @prevalence.setter
    def prevalence(self, prevalence):
        if prevalence not in range(1, 6):
            raise ValueError(f"{prevalence} is not a valid prevalence level")
        self._prevalence = prevalence

    @property
    def trend(self):
        return self._trend

    @trend.setter
    def trend(self, trend):
        if trend not in range(1, 6):
            raise ValueError(f"{trend} is not a valid trend level")
        self._trend = trend

    def get_level(self, measure):
        return LEVELS[f"{measure}_levels"][getattr(self, measure)]
