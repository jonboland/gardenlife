class Status:
    """
    Class to represent the status of an item. 
    Status can either be current or archived.
    Default status is current.
    
    """
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
        """Set item status to archived."""
        self.status = "Archived"

    def unarchive(self):
        """Set item status to current."""
        self.status = "Current"

    def get(self):
        """Get the item's status."""
        return self.status
