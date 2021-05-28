from datetime import datetime
from dateutil.rrule import rrule

from constants import FREQS
from status import Status


class Task:
    """Class to represent a garden task."""
    def __init__(
        self,
        name,
        description=None,
        assignee=None,
        length=None,
        linked_creatures=None,
        linked_plants=None,
    ):
        self.name = name
        self.schedule = [self._set_date()]
        self.description = description
        self.assignee = assignee
        self.length = length
        self.completed_dates = []
        self.linked_creatures = linked_creatures
        self.linked_plants = linked_plants
        self.raw_schedule = None
        self.status = Status()

    def __repr__(self):
        return f"Task: {self.name}"

    def __eq__(self, other):
        return repr(self) == other

    def set_schedule(self, start_date, freq, count, bymonth, interval):
        """Set task's scheduled dates using dateutils.rrule."""
        # Stores the raw schedule values to repopulate UI fields
        self.raw_schedule = {
            "start date": start_date,
            "freq": freq,
            "count": count,
            "bymonth": bymonth,
            "interval": interval,
        }
        # Converts string to datetime object. Sets start date to today if not supplied
        start_date = self._set_date(start_date)
        # Sets the frequency to the required value or monthly if not supplied
        freq = FREQS.get(freq, FREQS["Monthly"])
        count = int(count) if count else 1
        bymonth = [int(month) for month in bymonth.split(" ")] if bymonth else None
        interval = int(interval) if interval else 1
        # Creates the specified list of scheduled dates with dateutils.rrule
        self.schedule = list(
            rrule(
                dtstart=start_date,
                freq=freq,
                count=count,
                bymonth=bymonth,
                interval=interval,
            )
        )

    def update_completed_dates(self, all_progress):
        """
        Take a dict containing all scheduled dates as keys in string format.
        Add or removes dates from completed dates list based on their boolean values.
        """
        for date_string, boolean in all_progress.items():
            date = self._string_to_date(date_string)
            if boolean:
                self._add_completed_date(date)
            else:
                self._remove_completed_date(date)
        self.completed_dates.sort()

    def _add_completed_date(self, date):
        # Add date to completed date list if not already present
        if date not in self.completed_dates:
            self.completed_dates.append(date)

    def _remove_completed_date(self, date):
        # Remove date from completed dates list
        try:
            self.completed_dates.remove(date)
        except ValueError:
            pass

    def get_all_progress(self):
        """
        Return a dict containing all scheduled dates in string format with bool
        indicating whether they are in the completed dates list.
        Any completed dates that are not in the current schedule are also included.
        """
        return {
            self._date_to_string(date): (date in self.completed_dates)
            for date in sorted(self.schedule + self.completed_dates)
        }

    def get_current_progress(self, current_date=None):
        """Return current task progress."""
        # Convert string to datetime object. Set current date to today if no date supplied
        current_date = self._set_date(current_date)

        if not self.completed_dates:
            if current_date < self.schedule[0]:
                return "Not yet due"
            elif current_date == self.schedule[0]:
                return "Due"
            missed_dates_no_completed = sum(
                date < current_date for date in self.schedule
            )
            if missed_dates_no_completed == 1:
                return "Overdue"
            # If number of missed dates isn't 1 it must be greater than 1
            return "Very overdue"

        if current_date in self.schedule and current_date > self.completed_dates[-1]:
            return "Due"
        # Scheduled dates since task last completed, before or on the current date
        missed_dates_with_completed = sum(
            date > self.completed_dates[-1] and date < current_date
            for date in self.schedule
        )
        if missed_dates_with_completed == 1:
            return "Overdue"
        elif missed_dates_with_completed > 1:
            return "Very overdue"
        # If there aren't any missed dates the task is up to date
        return "Completed"

    def get_next_due_date(self):
        """Return task's next due date in string format."""
        if not self.completed_dates:
            return self._date_to_string(self.schedule[0])
        elif self.schedule[-1] <= self.completed_dates[-1]:
            return "No further due dates"
        next_due = min(
            date for date in self.schedule if date > self.completed_dates[-1]
        )
        return self._date_to_string(next_due)

    def _set_date(self, date=None):
        # Return datetime object from string or today if not date
        if date:
            return self._string_to_date(date)
        return datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    def _string_to_date(self, date_string):
        # Convert a string into a datetime object
        return datetime.strptime(date_string, "%d/%m/%Y")

    def _date_to_string(self, date_object):
        # Convert a datetime object into a string
        return datetime.strftime(date_object, "%d/%m/%Y")
