from unittest import TestCase
import os, json
from src.coursescheduler import generate_schedule
from src.coursescheduler.models import Schedule


class PyTestTesting(TestCase):
    def test_always_passes(self):
        self.assertTrue(True)

    def test_scheduler_output_meets_spec(self):
        schedule, error = generate_schedule(None, None, True)
        self.assertIsNone(error)
        Schedule.validate(schedule)  # will raise exception if invalid

    def test_scheduler_output_meets_spec_old_input(self):
        schedule_file = open(
            os.path.join(os.path.dirname(__file__), "../src/coursescheduler/temp_json_input/schedule_object.json")
        )
        schedule_input = json.load(schedule_file)
        schedule_file.close()
        schedule, error = generate_schedule(None, schedule_input, True)
        self.assertIsNone(error)
        Schedule.validate(schedule)  # will raise exception if invalid
