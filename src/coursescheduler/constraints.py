from typing import List, TypeVar

from .csp import Constraint

# from tests.datamodels_tester import temp_profs, temp_courses
# from coursescheduler.csp import Constraint

V = TypeVar('V')  # variable type
D = TypeVar('D')  # domain type


# Hard constraint: instructors may only be assigned to courses for which they are qualified.
# Note: this constraint currently isn't used.
# Instead, we exclude any unqualified professors from the domain of each variable in CSP 1.
class qualified_course_prof(Constraint):
    def __init__(self, course, professors):
        super().__init__([course])
        self.professors = professors

    def satisfied(self, assignment) -> bool:
        course = self.variables[0]
        if course not in assignment:
            return True

        prof = assignment[course]
        if course in self.professors[prof]["qualifiedCoursePreferences"]:
            return True

        return False


class course_requires_peng(Constraint):
    def __init__(self, course, professors):
        super().__init__([course])
        self.professors = professors

    def satisfied(self, assignment) -> bool:
        course = self.variables[0]
        if course not in assignment:
            return True

        prof = assignment[course]
        if self.professors[prof]["isPeng"]:
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


# Possibly edit to incLude a dictionary to continuously count the professor load
class course_timeslot_conflicts(Constraint):
    def __init__(self, courses, timeslot_configs) -> None:
        super().__init__(courses)
        self.timeslot_configs = timeslot_configs

    def satisfied(self, assignment) -> bool:
        for course in self.variables:
            if course not in assignment:
                continue

            other_courses = [x for x in assignment if x != course and x in self.variables]

            for compare_course in other_courses:
                # print("comparing courses {} to {}".format(course, compare_course))

                timeslot_config_1 = self.timeslot_configs[assignment[course]]
                timeslot_config_2 = self.timeslot_configs[assignment[compare_course]]
                num_days_1 = len(timeslot_config_1)
                num_days_2 = len(timeslot_config_2)

                # If the timeslot configurations have the same number of days:
                if num_days_1 == num_days_2:
                    # If the day of the first timeslot in each configuration is not the same,
                    # then they must be 3-hour slots on different days, and cannot overlap.
                    if timeslot_config_1[0][0] != timeslot_config_2[0][0]:
                        continue
                    # Otherwise, they are either both TWF, or both MTh,
                    # so just check for an overlap on the first day,
                    # since the times will be the same on the other days.
                    if self.check_if_conflicts(timeslot_config_1[0], timeslot_config_2[0]):
                        return False

                # If timeslot has only 1 number of days, it's an ANY day configuration, timeslot
                # Meaning the other timeslot is MTh or TWF, all timeslots must be compared to ensure there's no overlap
                elif num_days_1 == 1 or num_days_2 == 1:

                    for i in range(num_days_1):
                        for j in range(num_days_2):

                            if self.check_if_conflicts(timeslot_config_1, timeslot_config_2[j]):
                                return False
        return True

    def check_if_conflicts(self, timeslot_1, timeslot_2):
        course_start_time = timeslot_1[1]
        course_end_time = timeslot_1[2]

        compare_course_start_time = timeslot_2[1]
        compare_course_end_time = timeslot_2[2]

        # Checks if the start time of course 2 is in between the course 1 time
        if (course_start_time <= compare_course_start_time) and (course_end_time >= compare_course_start_time):
            # print("Comparing: {} to {} VS {} to {}.".format(course_start_time.time(), course_end_time.time(),
            #                                                 compare_course_start_time.time(),
            #                                                 compare_course_end_time.time()))
            return True

        # Checks if the start time of course 1 is in between the course 2 time
        if (compare_course_start_time <= course_start_time) and (compare_course_end_time >= course_start_time):
            # print("Comparing: {} to {} VS {} to {}.".format(course_start_time.time(), course_end_time.time(),
            #                                                 compare_course_start_time.time(),
            #                                                 compare_course_end_time.time()))
            return True

        return False

