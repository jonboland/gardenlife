class Status:
    def __init__(self, status="current"):
        self.status = status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if status not in ("current", "archived"):
            raise ValueError(f"{status} is not a valid status")
        self._status = status

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.status}')"

    def archive(self):
        self.status = "archived"

    def unarchive(self):
        self.status = "current"

    def get(self):
        return self.status
