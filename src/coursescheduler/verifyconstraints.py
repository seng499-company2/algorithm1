from typing import List, TypeVar

from tests.datamodels_tester import temp_profs, temp_courses
from .csp import Constraint

V = TypeVar('V')  # variable type
D = TypeVar('D')  # domain type


class verify_qualified_course_prof(Constraint):

    def __init__(self, professor, courseName) -> None:
        super().__init__([temp_courses])
        self.professor = professor
        self.courseName = courseName

    def satisfied(self) -> bool:
        if self.courseName in self.professor["qualifiedCoursePreferences"]:
            return True
        return False

class verify_requires_peng(Constraint):

    def __init__(self, professor, course) -> None:
        super().__init__([temp_courses])
        self.professor = professor
        self.course = course

    def satisfied(self) -> bool:
        if self.course["pengRequired"]:
            if self.professor["isPeng"]:
                return True
            else:
                return False
        else:
            return True

class verify_assigned_teaching_load(Constraint):

    def __init__(self) -> None:
        super().__init__([temp_courses])
        self.allProfessors = temp_profs

    def satisfied(self) -> bool:
        professor_courseload = {}

        for prof, values in self.allProfessors.items():
            professor_courseload[prof] = 0

        for course, values in self.variables[0].items():
            professor_courseload[values["professor"]] += 1

        for prof, value in professor_courseload.items():
            if value > self.allProfessors[prof]["teachingObligations"]:
                return False
        return True


class verify_all_courses_assigned_professors(Constraint):

    def __init__(self) -> None:
        super().__init__([temp_courses])
        self.allProfessors = temp_profs

    def satisfied(self) -> bool:
        for course, values in self.variables[0].items():
            if values["professor"] == '':
                return False
        return True
