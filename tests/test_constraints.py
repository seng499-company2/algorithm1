from unittest import TestCase

import pytest
from src.coursescheduler.verifyconstraints import verify_requires_peng, \
    verify_assigned_teaching_load, verify_all_courses_assigned_professors, verify_qualified_course_prof
from tests.datamodels_tester import temp_profs, temp_courses


class PyTestConstraints(TestCase):

    def test_qualified_course_profs_pass(self):
        test = verify_qualified_course_prof(temp_profs["Bird"], "csc110")
        assert (test.satisfied()) == True

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

    @pytest.mark.skip
    def test_assigned_teaching_load_passes(self):
        test = verify_assigned_teaching_load()
        self.assertTrue(test.satisfied())



    def test_all_courses_assigned_professors_fails(self):
        temp_courses["csc110"]["professor"] = ""
        test = verify_all_courses_assigned_professors()
        self.assertFalse(test.satisfied())
