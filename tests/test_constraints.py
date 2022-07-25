from unittest import TestCase

import pytest

from src.coursescheduler.constraints import (
    qualified_course_prof,
    course_requires_peng,
    professor_teaching_load,
    course_timeslot_conflicts,
)
from src.coursescheduler.datamodels import timeslot_determination
from src.coursescheduler.verifyconstraints import (
    verify_requires_peng,
    verify_assigned_teaching_load,
    verify_all_courses_assigned_professors,
    verify_qualified_course_prof,
)
from tests.datamodels_tester import temp_profs, temp_courses, test_professors, test_assignment, test_time


class PyTestConstraints(TestCase):
    def test_qualified_course_prof_fail(self):
        test = qualified_course_prof("SENG265", test_professors)
        self.assertFalse(test.satisfied([], test_assignment))

    def test_qualified_course_prof_pass(self):
        test = qualified_course_prof("CSC111", test_professors)
        self.assertTrue(test.satisfied([], test_assignment))

    def test_course_requires_peng_fail(self):
        test = course_requires_peng("SENG265", test_professors)
        self.assertFalse(test.satisfied([], test_assignment))

    def test_course_requires_peng_pass(self):
        test = course_requires_peng("CSC111", test_professors)
        self.assertTrue(test.satisfied([], test_assignment))

    def test_professor_teaching_load_fail(self):
        test = professor_teaching_load(["CSC111", "CSC115", "CSC225"], test_professors)
        self.assertFalse(test.satisfied([], test_assignment))

    def test_professor_teaching_load_pass(self):
        test = professor_teaching_load(["SENG265"], test_professors)
        self.assertTrue(test.satisfied([], test_assignment))

    def test_course_timeslot_conflicts_fail(self):
        timeslot_configs = timeslot_determination()
        static_courses = []
        test = course_timeslot_conflicts(["CSC111", "CSC115"], timeslot_configs, static_courses)
        self.assertFalse(test.satisfied([], test_time))

    def test_course_timeslot_conflicts_pass(self):
        timeslot_configs = timeslot_determination()
        static_courses = []
        test = course_timeslot_conflicts(["SENG265", "CSC225"], timeslot_configs, static_courses)
        self.assertTrue(test.satisfied([], test_time))

    @pytest.mark.skip
    def test_assigned_teaching_load_passes(self):
        test = verify_assigned_teaching_load()
        self.assertTrue(test.satisfied())

    def test_qualified_course_profs_pass(self):
        test = verify_qualified_course_prof(temp_profs["Bird"], "csc110")
        self.assertTrue(test.satisfied())

    def test_qualified_course_profs_fails(self):
        test = verify_qualified_course_prof(temp_profs["Bird"], "seng474")
        self.assertFalse(test.satisfied())

    def test_requires_PENG_pass(self):
        test = verify_requires_peng(temp_profs["Adams"], temp_courses["seng475"])
        self.assertTrue(test.satisfied())

    def test_doesnt_require_PENG_pass(self):
        test = verify_requires_peng(temp_profs["Bird"], temp_courses["csc110"])
        self.assertTrue(test.satisfied())

    def test_requires_PENG_fails(self):
        test = verify_requires_peng(temp_profs["Bird"], temp_courses["seng475"])
        self.assertFalse(test.satisfied())

    def test_all_courses_assigned_professors_fails(self):
        temp_courses["csc110"]["professor"] = ""
        test = verify_all_courses_assigned_professors()
        self.assertFalse(test.satisfied())
