from status import Status


class Task:
    def __init__(
        self,
        task_name,
        description=None,
        assignee=None,
        seasons=None,
        length=None,
        frequency=None,
        due_date=None,
    ):
        self.task_name = task_name
        self.description = description
        self.assignee = assignee
        self.seasons = seasons
        self.length = length
        self.frequency = frequency
        self.due_date = due_date
        self.creatures = []
        self.plants = []
        self.status = Status()

    def __repr__(self):
        return f"Task: {self.task_name}"
