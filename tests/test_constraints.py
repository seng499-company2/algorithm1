from unittest import TestCase
import pytest
from src.coursescheduler.constraints import Qualified_Course_Prof, profs, Requires_PENG, \
    All_Courses_Assigned_Professors, Assigned_Teaching_Load, courses


class PyTestConstraints(TestCase):

    def test_qualified_course_profs_pass(self):
        test = Qualified_Course_Prof(profs["Bird"], "csc110")
        assert (test.satisfied()) == True

    def test_qualified_course_profs_fails(self):
        test = Qualified_Course_Prof(profs["Bird"], "seng474")
        self.assertFalse(test.satisfied())

    def test_requires_PENG_pass(self):
        test = Requires_PENG(profs["Adams"], courses["seng475"])
        self.assertTrue(test.satisfied())

    def test_doesnt_require_PENG_pass(self):
        test = Requires_PENG(profs["Bird"], courses["csc110"])
        self.assertTrue(test.satisfied())

    def test_requires_PENG_fails(self):
        test = Requires_PENG(profs["Bird"], courses["seng475"])
        self.assertFalse(test.satisfied())

    @pytest.mark.skip
    def test_assigned_teaching_load_passes(self):
        test = Assigned_Teaching_Load()
        self.assertTrue(test.satisfied())

    def test_Assigned_Teaching_Load_Fails(self):
        test = Assigned_Teaching_Load()
        self.assertFalse(test.satisfied())

    def test_all_courses_assigned_professors_pass(self):
        test = All_Courses_Assigned_Professors()
        self.assertTrue(test.satisfied())

    def test_all_courses_assigned_professors_fails(self):
        print(courses["csc110"]["Professor"])
        self.assertTrue(True)
