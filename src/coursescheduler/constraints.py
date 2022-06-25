from typing import List, TypeVar

from src.coursescheduler.scheduler import *
from src.coursescheduler.models import temp_profs, temp_courses
from src.coursescheduler.csp import Constraint

V = TypeVar('V')  # variable type
D = TypeVar('D')  # domain type


class Qualified_Course_Prof(Constraint):

    def __init__(self, professor, courseName) -> None:
        super().__init__(self)
        self.professor = professor
        self.courseName = courseName

    def satisfied(self) -> bool:
        if self.courseName in self.professor["qualifiedCourses"]:
            return True
        return False

class Requires_PENG(Constraint):

    def __init__(self, professor, course) -> None:
        super().__init__(self)
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

class Assigned_Teaching_Load(Constraint):

    def __init__(self) -> None:
        super().__init__(self)
        self.allProfessors = temp_profs
        self.allCourses = temp_courses

    def satisfied(self) -> bool:
        professor_courseload = {}

        for prof, values in self.allProfessors.items():
            professor_courseload[prof] = 0

        for course, values in self.allCourses.items():
            professor_courseload[values["professor"]] += 1

        for prof, value in professor_courseload.items():
            if value > self.allProfessors[prof]["teachingObligations"]:
                return False
        return True


class All_Courses_Assigned_Professors(Constraint):

    def __init__(self) -> None:
        super().__init__(self)
        self.allProfessors = temp_profs
        self.allCourses = temp_courses

    def satisfied(self) -> bool:
        for course, values in self.allCourses.items():
            if values["professor"] == '':
                return False
        return True
