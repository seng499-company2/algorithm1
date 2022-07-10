from unittest import TestCase
from src.coursescheduler import generate_schedule
from src.coursescheduler.models import Schedule

class PyTestTesting(TestCase):
    def test_always_passes(self):
        self.assertTrue(True)

    def test_scheduler_output_meets_spec(self):
        schedule = generate_schedule(None, None, True)
        Schedule.validate(schedule)
