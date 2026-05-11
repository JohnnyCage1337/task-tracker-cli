import datetime
import time
import unittest

from task import Task, TaskStatus


class TestTask(unittest.TestCase):
    def test_task_creation_with_only_obliagory_args_success(self):
        """Validation if optional arguements are set up properly."""
        before_creation = datetime.datetime.now().replace(microsecond=0)
        tk = Task(1, "Test 1")
        after_creation = datetime.datetime.now().replace(microsecond=0)

        self.assertEqual(tk.id, 1)
        self.assertEqual(tk.desc, "Test 1")
        self.assertEqual(tk.status, TaskStatus.TODO)
        self.assertTrue(before_creation <= tk.created_at <= after_creation)
        self.assertTrue(before_creation <= tk.updated_at <= after_creation)

        self.assertEqual(tk.created_at, tk.updated_at)

    def test_task_creation_with_all_args_success(self):
        """Validation if all given arguements are set up properly."""
        id = 5
        desc = "Test"
        status = TaskStatus("done")
        now = datetime.datetime.now()
        created_at = (now - datetime.timedelta(days=2)).replace(microsecond=0)
        updated_at = (now - datetime.timedelta(days=1)).replace(microsecond=0)

        created_at_str = created_at.strftime(Task.date_format)
        updated_at_str = updated_at.strftime(Task.date_format)

        tk = Task(id, desc, status, created_at_str, updated_at_str)

        self.assertEqual(tk.id, id)
        self.assertEqual(tk.desc, desc)
        self.assertEqual(tk.status, status)
        self.assertEqual(tk.created_at, created_at)
        self.assertEqual(tk.updated_at, updated_at)

    def test_task_updates_timestamp_on_property_change(self):
        """Ensure that updated_at changes when desc or status is modified."""
        tk = Task(1, "Original Desc")
        original_time = tk.updated_at

        # small latency for confirm change of updated_at
        time.sleep(1)

        # Desc change test
        tk.desc = "New Desc"
        self.assertGreater(
            tk.updated_at, original_time, "updated_at should increase after desc change"
        )

        # status change test
        new_updated_at_time = tk.updated_at
        time.sleep(1)
        tk.status = TaskStatus.IN_PROGRESS
        self.assertGreater(
            tk.updated_at,
            new_updated_at_time,
            "updated_at should increase after status change",
        )

    def test_to_dict_and_from_dict_serialization_cycle(self):
        """Validate if created task will still after serialization."""
        task_serialized = Task(10, desc="Testing", status=TaskStatus("in-progress"))
        task_to_dict = task_serialized.to_dict()
        task_deserialized = Task.from_dict(task_to_dict)

        self.assertEqual(task_serialized, task_deserialized)

    def test_set_status_failure(self):
        "Ensure that given unexisted status rise KeyError"
        with self.assertRaises(ValueError):
            tk = Task(11, "Test")
            tk.status = TaskStatus("will-do")

    def test_task_equality(self):
        """Ensure two tasks with same data are considered equal."""
        tk1 = Task(1, "Test")
        tk2 = Task(1, "Test")

        self.assertEqual(tk1, tk2)
        tk2.desc = "Testing"
        self.assertNotEqual(tk1, tk2)

    def test_from_dict_missing_keys(self):
        """Check behavior when dictionary is incomplete."""
        incomplete_dict = {"id": 1, "desc": "No status here"}
        with self.assertRaises(KeyError):
            Task.from_dict(incomplete_dict)

    def test_from_dict_invalid_date_format(self):
        """Check behavior when date string is malformed."""
        bad_data = {
            "id": 1,
            "description": "Test",
            "status": "todo",
            "createdAt": "2024/01/01",  # błędny format
            "updatedAt": "2024/01/01",
        }
        with self.assertRaises(ValueError):
            Task.from_dict(bad_data)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTask)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print(f"Tests run: {result.testsRun}")
