class Status:
    def __init__(self, status="Current"):
        self.status = status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if status not in ("Current", "Archived"):
            raise ValueError(f"{status} is not a valid status")
        self._status = status

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.status}')"

    def archive(self):
        self.status = "Archived"

    def unarchive(self):
        self.status = "Current"

    def get(self):
        return self.status
