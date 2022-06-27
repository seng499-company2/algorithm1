from unittest import TestCase

import pytest
from src.coursescheduler.verifyconstraints import Verify_Requires_PENG, \
    Verify_Assigned_Teaching_Load, Verify_All_Courses_Assigned_Professors, Verify_Qualified_Course_Prof
from src.coursescheduler.datamodels import temp_profs, temp_courses


class PyTestConstraints(TestCase):

    def test_qualified_course_profs_pass(self):
        test = Verify_Qualified_Course_Prof(temp_profs["Bird"], "csc110")
        assert (test.satisfied()) == True

    def test_qualified_course_profs_fails(self):
        test = Verify_Qualified_Course_Prof(temp_profs["Bird"], "seng474")
        self.assertFalse(test.satisfied())

    def test_requires_PENG_pass(self):
        test = Verify_Requires_PENG(temp_profs["Adams"], temp_courses["seng475"])
        self.assertTrue(test.satisfied())

    def test_doesnt_require_PENG_pass(self):
        test = Verify_Requires_PENG(temp_profs["Bird"], temp_courses["csc110"])
        self.assertTrue(test.satisfied())

    def test_requires_PENG_fails(self):
        test = Verify_Requires_PENG(temp_profs["Bird"], temp_courses["seng475"])
        self.assertFalse(test.satisfied())

    @pytest.mark.skip
    def test_assigned_teaching_load_passes(self):
        test = Verify_Assigned_Teaching_Load()
        self.assertTrue(test.satisfied())



    def test_all_courses_assigned_professors_fails(self):
        temp_courses["csc110"]["professor"] = ""
        test = Verify_All_Courses_Assigned_Professors()
        self.assertFalse(test.satisfied())
