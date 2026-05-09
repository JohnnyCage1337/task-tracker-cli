import datetime as d
from enum import Enum


# Użycie enum ograniczy błędy przy literówkach ze stringami
# Jest bardziej czytelne
class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


class Task:
    def __init__(
        self,
        id: int,
        desc: str,
        status: TaskStatus,
        created_at: str = None,
        updated_at: str = None,
    ):
        self._id = id
        self._desc = desc
        self._status = status

        # odtwarzanie stanu
        now = d.datetime.now()
        date_format = "%d.%m.%y %H:%M:%S"
        if created_at:
            self._created_at = d.datetime.strptime(created_at, date_format)
        else:
            self._created_at = now

        if updated_at:
            self._updated_at = d.datetime.strptime(updated_at, date_format)
        else:
            self._updated_at = now

    @property
    def id(self):
        return self._id

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, desc):
        self._desc = desc
        self._update_timestamp()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status: TaskStatus):
        if not isinstance(new_status, TaskStatus):
            raise TypeError("new_status is not TaskStatus obj")
        self._status = new_status
        self._update_timestamp()

    @property
    def created_at(self):
        return self._created_at

    @property
    def updated_at(self):
        return self._updated_at

    def _update_timestamp(self):
        """A private method updating date of modification(_updated_at)"""
        self._updated_at = d.datetime.now()
