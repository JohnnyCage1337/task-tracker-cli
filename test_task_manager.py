import os
import unittest

from task import TaskStatus
from task_manager import TaskManager


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        """Prepare a fresh test environment before each test."""
        self.test_db = "test_tasks.json"
        self.tm = TaskManager(filename=self.test_db)

    def tearDown(self):
        """Clean up the environment by removing the temporary databse file."""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_persistence_between_instances(self):
        """Verify that data is correctly persisted to disk and reloaded by a new instance."""
        self.tm.add_task("Task 1")

        # Simulate application restart
        new_tm = TaskManager(filename=self.test_db)

        # Check if data exist were loaded from file
        self.assertEqual(len(new_tm._tasks), 1)
        self.assertEqual(new_tm.get_task(1).desc, "Task 1")

    def test_id_sequence(self):
        """Verify task ID generation logic(always increase by 1, never reapeat)."""
        task1_id = self.tm.add_task("Task 1")
        self.tm.delete_task(task1_id)

        task2_id = self.tm.add_task("Task 2")
        self.assertEqual(task2_id, 2)

    def test_if_update_at_change(self):
        """Ensure the 'updated_at timestamp is refreshed upon task modification."""
        task_id = self.tm.add_task("Task 1")
        old_date = self.tm.get_task(task_id).updated_at

        self.tm.update_task(task_id, new_desc="new_desc")
        new_date = self.tm.get_task(task_id).updated_at

        self.assertNotEqual(old_date, new_date)

    def test_add_task_increases_count(self):
        """Verify if adding a task increaments the internal task dictionary count by one"""
        initial_count = len(self.tm._tasks)
        self.tm.add_task("Testowe zadanie")
        self.assertEqual(len(self.tm._tasks), initial_count + 1)

    def test_update_task_with_status_and_desc(self):
        """Validate updates for description and status fields bot independently and simulaneously."""
        task1 = self.tm.add_task("Task 1")
        task2 = self.tm.add_task("Task 2")
        task3 = self.tm.add_task("Task 3")

        self.tm.update_task(id=task1, new_status="done")
        self.tm.update_task(id=task2, new_desc="new_desc")
        self.tm.update_task(id=task3, new_status="done", new_desc="new_desc")

        t1 = self.tm.get_task(task1)
        t2 = self.tm.get_task(task2)
        t3 = self.tm.get_task(task3)

        self.assertEqual(TaskStatus.DONE, t1.status)
        self.assertEqual(
            "new_desc",
            t2.desc,
        )
        self.assertEqual(TaskStatus.DONE, t3.status)
        self.assertEqual("new_desc", t3.desc)

    def test_get_tasks_by_status(self):
        """Ensure filtering logic correctly retrives sublists of tasks based on their status"""
        self.tm.add_task("Task 1")
        self.tm.add_task("Task 2")
        self.tm.add_task("Task 3")
        in_progress_task1 = self.tm.add_task("Task 4")
        in_progress_task2 = self.tm.add_task("Task 5")
        self.tm.update_task(id=in_progress_task1, new_status="in-progress")
        self.tm.update_task(id=in_progress_task2, new_status="in-progress")
        done_task1 = self.tm.add_task("Task 6")
        self.tm.update_task(id=done_task1, new_status="done")

        todo_tasks = self.tm.get_tasks_by_status(status=TaskStatus.TODO)
        in_progress_tasks = self.tm.get_tasks_by_status(status=TaskStatus.IN_PROGRESS)
        done_tasks = self.tm.get_tasks_by_status(status=TaskStatus.DONE)

        self.assertEqual(len(todo_tasks), 3)
        self.assertEqual(len(in_progress_tasks), 2)
        self.assertEqual(len(done_tasks), 1)

    def test_get_task_not_found(self):
        """Verify that requesting a non-existent task ID raises a KeyError."""
        with self.assertRaises(KeyError):
            self.tm.get_task(999)

    def test_delete_task_success(self):
        """Verify that an existing task is sucessfully removed from the manager's memory"""
        task_id = self.tm.add_task("Task 1")
        self.tm.delete_task(task_id)
        self.assertNotIn(task_id, self.tm._tasks)

    def test_delete_task_not_found(self):
        """Ensure that attempting to delete a non-existent task raises a KeyError."""
        with self.assertRaises(KeyError):
            self.tm.delete_task(999)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTaskManager)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print(f"Tests run: {result.testsRun}")
