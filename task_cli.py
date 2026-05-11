import sys

from task_manager import TaskManager


class TaskCLI:
    """Manages I/O of the Task Tracker Program."""

    example_usage_str = """\
    # Adding a new task
    task-cli add "Buy groceries"

    # Output: Task added successfully (ID: 1)
    # Updating and deleting tasks
    task-cli update 1 "Buy groceries and cook dinner"
    task-cli delete 1

    # Marking a task as in progress or done
    task-cli mark-in-progress 1
    task-cli mark-done 1

    # Listing all tasks
    task-cli list

    # Listing tasks by status
    task-cli list done
    task-cli list todo
    task-cli list in-progress"""

    def __init__(self):
        """Initialize TaskCli with TaskManager obj."""
        self.tm = TaskManager()

    def _print_tasks(self, tasks):
        if not tasks:
            print("No tasks found.")
            return
        print()
        print("TASK LIST")
        print("=" * 91)
        print(f"| {'ID':^8} | {'DESC':^60} | {'STATUS':^13} |")
        print("=" * 91)
        for t in tasks:
            print(f"| {t.id:^8} | {t.desc:^60} | {t.status.value:^13} |")
            print("-" * 91)
        print("=" * 91)

    def run(self):
        try:
            match sys.argv[1:]:
                case ["add", description]:
                    id = self.tm.add_task(description)
                    print(f"Success: Task added with ID {id}")
                case ["update", id, description]:
                    self.tm.update_task(int(id), new_desc=description)
                    print(f"Success: Task {id} has been updated")
                case ["delete", id]:
                    self.tm.delete_task(int(id))
                    print(f"Success: Task {id} has been deleted")
                case ["mark-in-progress", id]:
                    self.tm.update_task(int(id), new_status="in-progress")
                    print(f"Success: Task {id} marked as 'in-progress'")
                case ["mark-done", id]:
                    self.tm.update_task(int(id), new_status="done")
                    print(f"Success: Task {id} marked as 'done'")
                case ["mark-todo", id]:
                    self.tm.update_task(int(id), new_status="todo")
                    print(f"Success: Task {id} marked as 'todo'")
                case ["list"]:
                    tasks = self.tm.get_tasks_by_status()
                    self._print_tasks(tasks)
                case ["list", status]:
                    from task import TaskStatus

                    try:
                        # Konwertujemy string "done" na TaskStatus.DONE
                        status_obj = TaskStatus(status)
                        tasks = self.tm.get_tasks_by_status(status_obj)
                        self._print_tasks(tasks)
                    except ValueError:
                        print(
                            f"Error: '{status}' is not a valid status (todo, in-progress, done)."
                        )

                # Obsługa błędnych komend lub braku argumentów
                case ["help"]:
                    print(TaskCLI.example_usage_str)
                case []:
                    print(
                        "Usage: task-cli [command] [arguments]. task-cli help for example usage"
                    )
                case _:
                    print("Unknown command. Type 'task-cli help' to see example usage.")

        except KeyError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occured: {e}")


if __name__ == "__main__":
    cli = TaskCLI()
    cli.run()
