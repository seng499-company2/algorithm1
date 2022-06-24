from src.coursescheduler.constraints import profs, Qualified_Course_Prof
# from coursescheduler import Qualified_Course_Prof


def test_qualified_course_profs_pass():
    test = Qualified_Course_Prof(profs["Bird"], "csc110")
    x = 10
    assert x == 10
    assert test.satisfied() == True

# class PyTestConstraints(TestCase):
#     def test_always_fails(self):
#         self.assertTrue(True)
#     def test_qualified_course_profs_pass(self):
#         test = Qualified_Course_Prof(profs["Bird"], "csc110")
#         assert (test.satisfied()) == True

    # def test_qualified_course_profs_fails(self):
    #     test = Qualified_Course_Prof(profs["Bird"], "seng474")
    #     self.assertFalse(test.satisfied())
    #
    # def test_requires_PENG_pass(self):
    #     test = Requires_PENG(profs["Adams"], "seng474")
    #     self.assertTrue(test.satisfied())
    #
    # def test_doesnt_require_PENG_pass(self):
    #     test = Requires_PENG(profs["Bird"], "csc110")
    #     self.assertTrue(test.satisfied())
    #
    # def test_requires_PENG_fails(self):
    #     test = Requires_PENG(profs["Bird"], "ece310")
    #     self.assertFalse(test.satisfied())
    #
    # def test_assigned_teaching_load_passes(self):
    #     test = Assigned_Teaching_Load(profs["Bird"], "csc110")
    #     self.assertTrue(test.satisfied())
    #
    # def test_Assigned_Teaching_Load_Fails(self):
    #     test = Assigned_Teaching_Load(profs["Bird"], "csc110")
    #     self.assertFalse(test.satisfied())
    #
    # def test_all_courses_assigned_professors_pass(self):
    #     test = All_Courses_Assigned_Professors()
    #     self.assertTrue(test.satisfied())
    #
    # def test_all_courses_assigned_professors_fails(self):
    #     print(courses["csc110"]["Professor"])
    #     self.assertTrue(True)
