from garden import DATE, SEASONS


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
        status="current",
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
        self.status = status

    def __repr__(self):
        f"Task named: {self.task_name}"

