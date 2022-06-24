from typing import List, TypeVar

from .models import *
from .csp import Constraint

V = TypeVar('V')  # variable type
D = TypeVar('D')  # domain type

courses = {
    "csc110": {
        "pengRequired": False,
        "Professor": "Bird",
        "courseDay": ["monday", "tuesday", "wednesday"]
    },
    "csc111": {
        "pengRequired": False,
        "Professor": "Bird"
    },
    "seng265": {
        "pengRequired": False,
        "Professor": "Zastre"
    },
    "csc225": {
        "pengRequired": False,
        "Professor": "Zastre"
    },
    "csc226": {
        "pengRequired": False,
        "Professor": "Zastre"
    },
    "ece260": {
        "pengRequired": True,
        "Professor": "Zastre"
    },
    "ece310": {
        "pengRequired": True,
        "Professor": "Zastre"
    },
    "seng475": {
        "pengRequired": True,
        "Professor": "Zastre"
    }
}

# Note: data does not reflect the real world and is for testing only
profs = {
    "Bird": {
        "Name": "Bird",
        "isPeng": False,
        "qualifiedCourses": ["csc110", "csc111", "csc225", "csc226"],
        "teachingObligations": 2,
        "assigned_Courses": 3
    },
    "Zastre": {
        "Name": "Zastre",
        "isPeng": False,
        "qualifiedCourses": ["csc110", "csc111", "seng265"],
        "teachingObligations": 1

    },
    "Tzanatakis": {
        "Name": "Tzanatakis",
        "isPeng": False,
        "qualifiedCourses": ["csc225", "csc226"],
        "teachingObligations": 3
    },
    "Adams": {
        "Name": "Adams",
        "isPeng": True,
        "qualifiedCourses": ["ece260", "seng475"],
        "teachingObligations": 2
    },
    "Gebali": {
        "Name": "Gebali",
        "isPeng": True,
        "qualifiedCourses": ["ece260", "ece310"],
        "teachingObligations": 1
    }
}

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
        self.profs = profs
        self.courses = courses

    def satisfied(self) -> bool:
        professor_courseload = {}

        for prof, values in profs.items():
            professor_courseload[prof] = 0

        for course, values in courses.items():
            professor_courseload[values["Professor"]] += 1

        for prof, value in professor_courseload.items():
            if value > profs[prof]["teachingObligations"]:
                return False
        return True


class All_Courses_Assigned_Professors(Constraint):

    def __init__(self) -> None:
        super().__init__(self)
        self.profs = profs
        self.courses = courses

    def satisfied(self) -> bool:
        for course, values in courses.items():
            if values["Professor"] == '':
                return False
        return True


def main():
    test = Qualified_Course_Prof(profs["Bird"], "csc110")
    print(test.satisfied())

    test = Requires_PENG(profs["Bird"], courses["csc110"])
    print(test.satisfied())

    test = Assigned_Teaching_Load()
    print(test.satisfied())

    test = All_Courses_Assigned_Professors()
    print(test.satisfied())

if __name__ == "__main__":
    main()