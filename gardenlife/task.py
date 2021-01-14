from datetime import datetime
from dateutil.rrule import rrule, WEEKLY, MONTHLY, YEARLY

from status import Status


class Task:
    def __init__(
        self,
        task_name,
        schedule,
        description=None,
        assignee=None,
        length=None,
        progress=None,
    ):
        self.task_name = task_name
        self.schedule = sorted([datetime.strptime(schedule, "%d/%m/%Y")])
        self.description = description
        self.assignee = assignee
        self.length = length
        self.progress = progress
        self.completed_dates = sorted([])
        self.added_date = datetime.today()
        self.linked_creatures = dict()
        self.linked_plants = dict()
        self.status = Status()

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, progress):
        if progress not in {
            None,
            "outstanding",
            "in progress",
            "completed",
            "completed early",
        }:
            raise ValueError(f"{progress} is not a valid progress level")
        self._progress = progress

    def __repr__(self):
        return f"Task: {self.task_name}"

    def __eq__(self, other):
        return repr(self) == other

    def set_schedule(self, start_date=None, frequency=YEARLY, number=50, **kwargs):
        if start_date == None:
            start_date = self.schedule[0]
        else:
            start_date = datetime.strptime(start_date, "%d/%m/%Y")
        self.schedule = list(
            rrule(dtstart=start_date, freq=frequency, count=number, **kwargs)
        )
        self.status.unarchive()

    def view_schedule(self):
        return [datetime.strftime(due_date, "%d/%m/%Y") for due_date in self.schedule]

    def add_progress(self, progress, completed_date=None, add_date=True):
        self.progress = progress
        if self.progress in {"completed", "completed early"}:
            if add_date:
                completed_date = self._format_date(completed_date)
                self.completed_dates.append(completed_date)
            self._archive_if_finished(completed_date)

    def _archive_if_finished(self, completed_date):
        if len(self.schedule) == 1:
            self.status.archive()
        elif len(self.schedule) == 2:
            first_date, last_date = self.schedule
            if (
                completed_date > last_date
                or completed_date > first_date
                and self.progress == "completed early"
            ):
                self.status.archive()
        else:
            *_, penultimate_date, last_date = self.schedule
            if (
                completed_date > last_date
                or completed_date > penultimate_date
                and self.progress == "completed early"
            ):
                self.status.archive()

    def _format_date(self, date):
        if not date:
           return datetime.today()
        return datetime.strptime(date, "%d/%m/%Y")

    def refresh_progress(self, date=None):
        if self.status.get() != "archived" and self.progress != "outstanding":
            date = self._format_date(date)
            for idx, due_date in enumerate(self.schedule):
                if due_date > date:
                    break
                if self.completed_dates and self.completed_dates[-1] >= due_date:
                    continue
                if self.progress in {"in progress", "completed early"}:
                    try:
                        if self.schedule[idx + 1] > date:
                            break
                        self.progress = "outstanding"
                    except IndexError:
                        break
                self.progress = "outstanding"

    def view_progress(self):
        status = self.status.get()
        if status == "archived":
            return status
        return self.progress

    def link_creature(self, creature):
        self.linked_creatures[creature.creature_name] = creature

    def unlink_creature(self, creature_name):
        del self.linked_creatures[creature_name]

    def link_plant(self, plant):
        self.linked_plants[plant.plant_name] = plant

    def unlink_plant(self, plant_name):
        del self.linked_plants[plant_name]
