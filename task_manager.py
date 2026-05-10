import json
from pathlib import Path

from task import Task, TaskStatus

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "task.json"


class TaskManager:
    """Manages the lifecycle of tasks including persistence, filtering, and updates."""

    def __init__(self, filename=None):
        """
        Initialize TaskManager and load tasks from the specified file.

        Args:
            filename (str, optional): Custom path to the JSON database file.
        """
        self._tasks: dict[int, Task] = {}
        self.database_path = Path(filename) if filename else DATABASE_PATH
        self._last_id = 0

        if not self.database_path.exists():
            # create file
            with open(self.database_path, "w") as json_file:
                json.dump([], json_file)
        else:
            self._load_from_file()

    def add_task(self, desc: str):
        """
        Create a new task and save it to the database.

        Args:
            desc (str): description of the task.

        Returns:
            int: The unique ID assigned to the new task.
        """
        self._last_id += 1
        new_task = Task(id=self._last_id, desc=desc)
        self._tasks[self._last_id] = new_task
        self._save_to_file()
        return self._last_id

    def update_task(self, id: int, new_desc: str = None, new_status: str = None):
        """
        Update the description, status, or both for a specific task.

        Args:
            id (int): ID of the task to update.
            new_desc (str, optional): New text for the task description.
            new_status (str, optional): New status string (must match TaskStatus values).

        Raises:
            KeyError: If the task ID does not exist.
        """
        if new_desc is None and new_status is None:
            return

        task = self._tasks.get(id)

        if not task:
            raise KeyError(f"Cannot update: Task {id} does not exist.")

        if new_desc:
            task.desc = new_desc
        if new_status:
            task.status = TaskStatus(new_status)
        self._save_to_file()

    def get_task(self, id: int) -> Task:
        """Return Task obj with given id or raise KeyError"""
        try:
            return self._tasks[id]
        except KeyError:
            raise KeyError(f"Task with ID {id} does not exist")

    def delete_task(self, id: int):
        if id not in self._tasks:
            raise KeyError(f"Task with ID: {id} does not exist and cannot be deleted")

        self._tasks.pop(id)
        self._save_to_file()

    def _load_from_file(self):
        with open(self.database_path, "r") as json_file:
            data = json.load(json_file)
            self._last_id = data.get("last_id", 0)
            for item in data.get("tasks", []):
                task = Task.from_dict(item)
                self._tasks[task.id] = task

    def _save_to_file(self):
        tasks_to_dict = [task.to_dict() for task in self._tasks.values()]
        output = {"last_id": self._last_id, "tasks": tasks_to_dict}
        with open(self.database_path, "w") as jsonfile:
            json.dump(output, jsonfile, indent=4)

    def get_tasks_by_status(self, status: TaskStatus = TaskStatus.TODO):
        """Return a list of tasks filtered by their current status."""
        return [task for task in self._tasks.values() if task.status == status]


if __name__ == "__main__":
    pass
