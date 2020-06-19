class Organism:
    def __init__(self, impact, prevalence, trend, organism_kind):  # organism_kind,
        self.impact_levels = (
            "very negative",
            "negative",
            "neutral",
            "positive",
            "very positive",
        )
        self.prevalence_levels = ("very low", "low", "medium", "high", "very high")
        self.trend_levels = (
            "rapidly decreasing",
            "decreasing",
            "stable",
            "increasing",
            "rapidly increasing",
        )
        self.impact = impact
        self.prevalence = prevalence
        self.trend = trend
        self.organism_kind = organism_kind

    @property
    def impact(self):
        return self._impact

    @impact.setter
    def impact(self, impact):
        if impact not in self.impact_levels:
            raise ValueError(f"{impact} is not a valid impact level")
        self._impact = impact

    @property
    def prevalence(self):
        return self._prevalence

    @prevalence.setter
    def prevalence(self, prevalence):
        if prevalence not in self.prevalence_levels:
            raise ValueError(f"{prevalence} is not a valid prevalence level")
        self._prevalence = prevalence

    @property
    def trend(self):
        return self._trend

    @trend.setter
    def trend(self, trend):
        if trend not in self.trend_levels:
            raise ValueError(f"{trend} is not a valid trend level")
        self._trend = trend

    def __repr__(self):
        return f"{self.__class__.__name__} of type {self.kind}."

    def change_level(self, measure, direction):
        item = getattr(self, measure)
        setting = getattr(self, f"{measure}_levels")
        if direction == "increase" and item != setting[-1]:
                setattr(self, measure, setting[setting.index(item) + 1])
        elif direction == "decrease" and item != setting[0]:
                setattr(self, measure, setting[setting.index(item) - 1])
        else:
            print(f"{measure.title()} already set to {item}")

test_org = Organism("neutral", "medium", "stable", "creature")
