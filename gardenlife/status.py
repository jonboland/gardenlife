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

    def change_status(self):
        if self.status == "current":
            self.status = "archived"
        elif self.status == "archived":
            self.status = "current"
