from typing import List, TypeVar

from .csp import Constraint
from .csp import SoftConstraint

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

    def satisfied(self, variable, assignment) -> bool:
        course = self.variables[0]
        if course not in assignment:
            return True

        prof = assignment[course]
        for i in range(len(self.professors[prof]["qualifiedCoursePreferences"])):
            if course in self.professors[prof]["qualifiedCoursePreferences"][i]["courseCode"] and \
                    self.professors[prof]["qualifiedCoursePreferences"][i]["enthusiasmScore"] != 0:
                return True

        return False


class course_requires_peng(Constraint):
    def __init__(self, course, professors):
        super().__init__([course])
        self.professors = professors

    def satisfied(self, variable, assignment) -> bool:
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

    def satisfied(self, variable, assignment) -> bool:
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

    def satisfied(self, variable, assignment) -> bool:
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


class csp_1_happiness_constraint(Constraint):

    def __init__(self, courses, professors, happiness_threshold) -> None:
        super().__init__(courses)
        self.professors = professors
        self.happiness_threshold = happiness_threshold

    def satisfied(self, variable, assignment) -> bool:
        # Get list of courses having the same professor as course currently under consideration.
        prof_id = assignment[variable]
        prof_courses = [course for course in assignment.keys() if (assignment[course] == prof_id)]

        enthusiasm_sum = 0
        num_courses_fall = 0
        num_courses_spring = 0
        num_courses_summer = 0
        for course in prof_courses:
            # Get sum of enthusiasm scores for professor assigned to course currently under consideration.
            for course_preferences in self.professors[prof_id]["qualifiedCoursePreferences"]:
                if course_preferences["courseCode"] == course.split("_")[0]:
                    enthusiasm_sum += course_preferences["enthusiasmScore"]

            # Record number of courses assigned to the professor for each semester.
            if course.split("_")[1] == "fall":
                num_courses_fall += 1
            elif course.split("_")[1] == "spring":
                num_courses_spring += 1
            elif course.split("_")[1] == "summer":
                num_courses_summer += 1

        # Compute happiness regarding course preferences.
        enthusiasm_mean = enthusiasm_sum / len(prof_courses)
        happiness_course_preferences = (enthusiasm_mean - 20) / (195 - 20)

        # Compute happiness regarding preferred courses per semester.
        preferred_num_courses_fall = self.professors[prof_id]["preferredCoursesPerSemester"]["fall"]
        preferred_num_courses_spring = self.professors[prof_id]["preferredCoursesPerSemester"]["spring"]
        preferred_num_courses_summer = self.professors[prof_id]["preferredCoursesPerSemester"]["summer"]

        happiness_preferred_courses_semester = 0
        if num_courses_fall <= preferred_num_courses_fall:
            happiness_preferred_courses_semester += 1
        if num_courses_spring <= preferred_num_courses_spring:
            happiness_preferred_courses_semester += 1
        if num_courses_summer <= preferred_num_courses_summer:
            happiness_preferred_courses_semester += 1

        happiness_preferred_courses_semester = happiness_preferred_courses_semester / 3

        # Compute happiness regarding preferred non-teaching semester.
        pref_non_teaching_semester = 1
        if self.professors[prof_id]["preferredNonTeachingSemester"] is not None:

            preferred_non_teach_semester = self.professors[prof_id]["preferredNonTeachingSemester"].lower()
            if preferred_non_teach_semester == "fall" and num_courses_fall == 0:
                pref_non_teaching_semester += 1
            elif preferred_non_teach_semester == "spring" and num_courses_fall == 0:
                pref_non_teaching_semester += 1
            elif preferred_non_teach_semester == "summer" and num_courses_fall == 0:
                pref_non_teaching_semester += 1

        happiness_pref_non_teaching_semester = pref_non_teaching_semester / 1

        # Compute happiness score.
        happiness = (happiness_course_preferences + happiness_preferred_courses_semester + \
                     happiness_pref_non_teaching_semester) / 3

        if happiness >= self.happiness_threshold:
            return True
        return False


# Soft Constraint for CSP 1
class course_preferences_constraint(SoftConstraint):
    def __init__(self, courses, professors) -> None:
        super().__init__(courses)
        self.professors = professors

    def satisfaction_score(self, assignment) -> float:
        overall_enthusiasm_sum = 0
        overall_course_prefs_per_semester_sum = 0
        overall_pref_non_teach_semester_sum = 0

        # For each professor:
        profs = set(assignment.values())
        for prof_id in profs:
            # Get list of courses having the same professor as course currently under consideration.
            prof_courses = [course for course in assignment.keys() if (assignment[course] == prof_id)]

            # Loop through prof's courses to compute satisfaction regarding the various soft constraints.
            prof_enthusiasm_sum = 0
            num_courses_fall = 0
            num_courses_spring = 0
            num_courses_summer = 0
            for course in prof_courses:
                # Get sum of enthusiasm scores for professor assigned to course currently under consideration.
                for course_preferences in self.professors[prof_id]["qualifiedCoursePreferences"]:
                    if course_preferences["courseCode"] == course.split("_")[0]:
                        prof_enthusiasm_sum += course_preferences["enthusiasmScore"]

                # Record number of courses assigned to the professor for each semester.
                # Used to compute the statisfaction regarding courses per semester and non-teaching semesters
                if course.split("_")[1] == "fall":
                    num_courses_fall += 1
                elif course.split("_")[1] == "spring":
                    num_courses_spring += 1
                elif course.split("_")[1] == "summer":
                    num_courses_summer += 1
            # Compute satisfaction regarding course preferences.
            prof_enthusiasm_mean = prof_enthusiasm_sum / len(prof_courses)
            prof_enthusiasm_mean_normalized = (prof_enthusiasm_mean - 20) / (195 - 20)
            overall_enthusiasm_sum += prof_enthusiasm_mean_normalized

            # Compute satisfaction regarding preferred number of courses per semester.
            preferred_num_courses_fall = self.professors[prof_id]["preferredCoursesPerSemester"]["fall"]
            preferred_num_courses_spring = self.professors[prof_id]["preferredCoursesPerSemester"]["spring"]
            preferred_num_courses_summer = self.professors[prof_id]["preferredCoursesPerSemester"]["summer"]

            # Getting the value of how many courses are being taught in the professors preferred course teachings
            # per semester
            total_courses_exceeding_pref_num_courses = 0
            if num_courses_fall > preferred_num_courses_fall:
                total_courses_exceeding_pref_num_courses += (num_courses_fall - preferred_num_courses_fall)
            if num_courses_spring > preferred_num_courses_spring:
                total_courses_exceeding_pref_num_courses += (num_courses_spring - preferred_num_courses_spring)
            if num_courses_summer > preferred_num_courses_summer:
                total_courses_exceeding_pref_num_courses += (num_courses_summer - preferred_num_courses_summer)

            # Subtracting the overall exceeding preferred number of courses per semester
            # To ensure the amount of exceeding courses are weighted higher the more courses a professor is teaching
            happiness_preferred_courses_semester = (1 - (total_courses_exceeding_pref_num_courses /
                                                         self.professors[prof_id]["teachingObligations"]))

            overall_course_prefs_per_semester_sum += happiness_preferred_courses_semester

            # Compute satisfaction regarding preferred non-teaching semester
            # *** NOTE ***
            # This soft constraint is not currently being included in the final satisfaction score.
            # It is handled by the previous soft constraint (preferred num courses per semester).
            # If a professor wishes not to teach in a particular semester,
            # their preferred number of courses for that semester should be zero.
            # Then the previous constraint will handle this.
            # In the case that the professor is a research professor (making this a hard constraint),
            # the constraint will be handled during value-pruning before the CSP runs.
            pref_non_teaching_semester = 1
            if self.professors[prof_id]["preferredNonTeachingSemester"] is not None:
                preferred_non_teach_semester = self.professors[prof_id]["preferredNonTeachingSemester"]
                if preferred_non_teach_semester == "FALL" and num_courses_fall != 0:
                    pref_non_teaching_semester -= 1
                elif preferred_non_teach_semester == "SPRING" and num_courses_spring != 0:
                    pref_non_teaching_semester -= 1
                elif preferred_non_teach_semester == "SUMMER" and num_courses_summer != 0:
                    pref_non_teaching_semester -= 1

            happiness_pref_non_teaching_semester = pref_non_teaching_semester
            overall_pref_non_teach_semester_sum += happiness_pref_non_teaching_semester

        overall_enthusiasm_mean = overall_enthusiasm_sum / len(profs)
        overall_enthusiasm_mean_course_per_sem = overall_course_prefs_per_semester_sum / len(profs)
        overall_enthusiasm_mean_non_teach_semester = overall_pref_non_teach_semester_sum / len(profs)

        # return overall_enthusiasm_mean

        return ((overall_enthusiasm_mean * 4) + overall_enthusiasm_mean_course_per_sem) / 5

