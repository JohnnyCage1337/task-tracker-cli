import json
from pathlib import Path

from task import Task

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "task.json"


class TaskManager:
    def __init__(self):
        self._tasks = {}
        if not DATABASE_PATH.exists():
            # create file
            with open(DATABASE_PATH, "w") as json_file:
                json.dump([], json_file)
        else:
            self._load_from_file()

    def add_task(self, desc: str):
        try:
            next_id = max(self._tasks.keys()) + 1
        except ValueError:
            self._tasks["1"] = Task(id=1, desc=desc)
            print(self._tasks)
        else:
            self._tasks[next_id] = Task(id=next_id, desc=desc)

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


if __name__ == "__main__":
    tm = TaskManager()
    tm.add_task("dupa")
