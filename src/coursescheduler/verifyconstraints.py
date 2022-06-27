from typing import List, TypeVar

from .datamodels import temp_profs, temp_courses
from .csp import Constraint

V = TypeVar('V')  # variable type
D = TypeVar('D')  # domain type


class Verify_Qualified_Course_Prof(Constraint):

    def __init__(self, professor, courseName) -> None:
        super().__init__([temp_courses])
        self.professor = professor
        self.courseName = courseName

    def satisfied(self) -> bool:
        if self.courseName in self.professor["qualifiedCoursePreferences"]:
            return True
        return False

class Verify_Requires_PENG(Constraint):

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

class Verify_Assigned_Teaching_Load(Constraint):

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


class Verify_All_Courses_Assigned_Professors(Constraint):

    def __init__(self) -> None:
        super().__init__([temp_courses])
        self.allProfessors = temp_profs

    def satisfied(self) -> bool:
        for course, values in self.variables[0].items():
            if values["professor"] == '':
                return False
        return True
