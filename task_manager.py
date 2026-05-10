import json
from pathlib import Path

from task import Task, TaskStatus

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "task.json"


class TaskManager:
    def __init__(self, filename=None):
        self._tasks: dict[int, Task] = {}
        self._database_path = Path(filename) if filename else DATABASE_PATH

        if not DATABASE_PATH.exists():
            # create file
            with open(DATABASE_PATH, "w") as json_file:
                json.dump([], json_file)
        else:
            self._load_from_file()

    def add_task(self, desc: str):
        assert isinstance(desc, str), "Opis musi być tekstem"

        next_id = max(self._tasks.keys(), default=0) + 1

        new_task = Task(id=next_id, desc=desc)
        self._tasks[next_id] = new_task

        self._save_to_file()

        return next_id

    def update_task(self, id: int, new_desc: str = None, new_status: str = None):

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

    def delete_task(self, id: int):
        if id not in self._tasks:
            raise KeyError(f"Task with ID: {id} does not exist and cannot be deleted")

        self._tasks.pop(id)
        self._save_to_file()

    def _load_from_file(self):
        with open(DATABASE_PATH, "r") as json_file:
            data = json.load(json_file)
            for item in data:
                task = Task.from_dict(item)
                self._tasks[task.id] = task

    def _save_to_file(self):
        tasks_to_dict = [task.to_dict() for task in self._tasks.values()]
        with open(DATABASE_PATH, "w") as jsonfile:
            print(self._tasks)
            json.dump(tasks_to_dict, jsonfile, indent=4)

    def get_tasks_by_status(self, status: TaskStatus = TaskStatus.TODO):
        return [task for task in self._tasks if task.status == status]


if __name__ == "__main__":
    tm = TaskManager()
    tm.add_task("dupa")
    tm.upda
