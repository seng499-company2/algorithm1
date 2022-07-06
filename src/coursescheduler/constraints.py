from typing import List, TypeVar

from csp import Constraint
from tests.datamodels_tester import temp_profs, temp_courses

V = TypeVar('V')  # variable type
D = TypeVar('D')  # domain type


# Hard constraint: instructors may only be assigned to courses for which they are qualified.
# Note: this constraint currently isn't used.
# Instead, we exclude any unqualified professors from the domain of each variable in CSP 1.
class qualified_course_prof(Constraint):
    def __init__(self, course):
        super().__init__([course])

    def satisfied(self, assignment) -> bool:
        course = self.variables[0]
        if course not in assignment:
            return True

        prof = assignment[course]
        if course in temp_profs[prof]["qualifiedCoursePreferences"]:
            return True

        return False


class course_requires_peng(Constraint):
    def __init__(self, course):
        super().__init__([course])

    def satisfied(self, assignment) -> bool:
        course = self.variables[0]
        if course not in assignment:
            return True

        prof = assignment[course]
        if temp_profs[prof]["isPeng"]:
            return True

        return False


# Possibly edit to incLude a dictionary to continuously count the professor load
class professor_teaching_load(Constraint):
    def __init__(self, courses, professors) -> None:
        super().__init__(courses)
        self.professors = professors

    def satisfied(self, assignment) -> bool:
        teaching_loads_dict = {prof: 0 for prof in self.professors}

        for course in self.variables:
            if course not in assignment:
                continue
            prof = assignment[course]
            teaching_loads_dict[prof] += 1

        for prof, teachingLoad in teaching_loads_dict.items():
            if teachingLoad > self.professors[prof]["teachingObligations"]:
                return False

        return True

# TODO: Create timeslots for the courses
# TODO: Create the hard constraints for:
#  overlapping courses
#  no-double booked professor
