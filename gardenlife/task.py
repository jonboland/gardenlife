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
        self.creatures = []
        self.plants = []
        self.status = Status()

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, progress):
        if progress not in (None, "outstanding", "in progress", "complete"):
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

    def add_progress(self, progress, completed_date=None):
        self.progress = progress
        if self.progress == "complete":
            if not completed_date:
                completed_date = datetime.today()
            else:
                completed_date = datetime.strptime(completed_date, "%d/%m/%Y")
            self.completed_dates.append(completed_date)
            *_, last_scheduled_date = self.schedule
            if completed_date > last_scheduled_date:
                self.status.archive()

    def refresh_progress(self, day=None):
        if not day:
            day = datetime.today()
        if self.progress != "outstanding":
            for idx, due_date in enumerate(self.schedule):
                if due_date > today:
                    break
                if self.completed_dates and self.completed_dates[-1] >= due_date:
                    break
                if self.progress == "in progress":
                    try:
                        if self.schedule[idx + 1] > today:
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

    def link_creatures(self):
        pass

    def link_plants(self):
        pass
