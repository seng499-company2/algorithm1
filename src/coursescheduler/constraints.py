from typing import List, TypeVar

from .csp import Constraint
from .csp import SoftConstraint
import datetime

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


# Hard Constraint: Checks if the course requires a PENG
# Currently not used as the CSP Domain is restricted directly in the Scheduler.py file
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


# Hard Constraint: Checks if the professor's assigned courses doesn't surpass their maximum teaching load
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


# Hard Constraint: Checks a given time slot and compares if it conflicts with a list of other time slots
class course_timeslot_conflicts(Constraint):
    def __init__(self, courses, timeslot_configs, static_courses) -> None:
        super().__init__(courses)
        self.timeslot_configs = timeslot_configs
        self.static_courses = static_courses

    def satisfied(self, variable, assignment) -> bool:
        for course in self.variables:
            if course not in assignment:
                continue

            other_courses = [x for x in assignment if x != course and x in self.variables]

            for compare_course in other_courses:
                if course in self.static_courses and compare_course in self.static_courses:
                    continue
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

                            if self.check_if_conflicts(timeslot_config_1[i], timeslot_config_2[j]):
                                return False
        return True

    def check_if_conflicts(self, timeslot_1, timeslot_2):
        course_start_time = timeslot_1[1]
        course_end_time = timeslot_1[2]

        compare_course_start_time = timeslot_2[1]
        compare_course_end_time = timeslot_2[2]

        # Checks if the start time of course 2 is in between the course 1 time
        if (course_start_time <= compare_course_start_time) and (course_end_time >= compare_course_start_time):
            return True

        # Checks if the start time of course 1 is in between the course 2 time
        if (compare_course_start_time <= course_start_time) and (compare_course_end_time >= course_start_time):
            return True

        return False


# Hard Constraint: Checks if a research prof isn't assigned a course during their research semester
# Currently not used as the CSP 1 domain restricts the research professors so they're not considered when scheduling
# a course during their semester off
class research_professor_semester_off(Constraint):
    def __init__(self, courses, professors) -> None:
        super().__init__(courses)
        self.professors = professors

    def satisfied(self, variable, assignment) -> bool:

        for course in self.variables:
            if course not in assignment:
                continue
            prof_id = assignment[course]
            if self.professors[prof_id]["facultyType"] == "RESEARCH":
                semester = course.split("_")[1]
                if self.professors[prof_id]["preferredNonTeachingSemester"] and semester == self.professors[prof_id]["preferredNonTeachingSemester"].lower():
                    return False

        return True


# Hard Constraint for any type of professor on leave.
# Scenarios:
# Teaching profs:
# no leave - 6 courses - 3 semesters on Already considered
# half leave - 3 courses - 2 semesters on (1 semester off Hard Constraint)
# full leave - 2 courses - 1 semester on ( 2 semesters off Hard Constraint)
#
# Research prof:
# no leave - 3 courses - 2 semesters on (1 semester off Hard Constraint) Already considered
# half leave - 1 course - 1 semester on ( 2 semesters off Hard Constraint) Already considered
# full leave - 0 courses - 0 semesters on ( 3 semesters off Hard Constraint) Already considered
class professor_on_leave(Constraint):
    def __init__(self, courses, professors) -> None:
        super().__init__(courses)
        self.professors = professors

    def satisfied(self, variable, assignment) -> bool:
        professor_courses = {prof: [] for prof in self.professors}

        for course in self.variables:
            if course not in assignment:
                continue
            prof_id = assignment[course]
            professor_courses[prof_id] += [course]

        for prof_id, courses in professor_courses.items():
            if self.professors[prof_id]["facultyType"] == "TEACHING":
                for course in courses:
                    semester = course.split("_")[1]
                    if self.professors[prof_id]["teachingObligations"] == 3:
                        if self.professors[prof_id]["preferredTimes"][semester] is None:
                            return False

                    if self.professors[prof_id]["teachingObligations"] == 2:
                        if self.professors[prof_id]["preferredTimes"][semester] is None:
                            return False

        return True


# Soft Constraint for CSP 1
class course_preferences_constraint(SoftConstraint):
    def __init__(self, courses, professors) -> None:
        super().__init__(courses)
        self.professors = professors

    def satisfaction_score(self, assignment, variable=None) -> float:
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

            # Subtracting the overall number courses that exceed the number of courses per semester
            # This weights the amount of courses exceeding the preferred number of courses per semester
            # Such as 1 exceeding courses is weighted lower than 2 exceeding courses
            enthusiasm_preferred_courses_per_semester = (1 - (total_courses_exceeding_pref_num_courses /
                                                              self.professors[prof_id]["teachingObligations"]))

            overall_course_prefs_per_semester_sum += enthusiasm_preferred_courses_per_semester

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

            enthusiasm_pref_non_teaching_semester = pref_non_teaching_semester
            overall_pref_non_teach_semester_sum += enthusiasm_pref_non_teaching_semester

        # Compute aggregate satisfactions scores for each soft constraint.
        overall_enthusiasm_mean = overall_enthusiasm_sum / len(profs)
        overall_enthusiasm_mean_course_per_sem = overall_course_prefs_per_semester_sum / len(profs)
        overall_enthusiasm_mean_non_teach_semester = overall_pref_non_teach_semester_sum / len(profs)

        # Compute and return a single overall satisfaction score combining all soft constraints.
        return ((overall_enthusiasm_mean * 4) + overall_enthusiasm_mean_course_per_sem) / 5


# Soft Constraint for CSP 2
class time_slot_constraint(SoftConstraint):
    def __init__(self, courses, professors, timeslot_configs, csp_1_result) -> None:
        super().__init__(courses)
        self.professors = professors
        self.timeslot_configs = timeslot_configs
        self.csp_1_result = csp_1_result

    def satisfaction_score(self, assignment, variable) -> float:
        if variable not in self.variables:
            return 1
        # Check for this professor have scheduled them outside-of their preferred hours

        # Dictionary of time codes used in time slots preferences
        time_codes = {"monday": "M", "tuesday": "T",
                      "wednesday": "W", "thursday": "Th", "friday": "F"}

        # Grab the professor for the course currently under consideration.
        prof_id = self.csp_1_result[variable]

        # Grab the professor's preferred course day spread (list).
        preferred_course_day_spread_list = self.professors[prof_id]["preferredCourseDaySpreads"]

        # Grab the timeslot configuration currently assigned to the variable.
        timeslot_config = self.timeslot_configs[assignment[variable]]

        # Compute satisfaction regarding preferred course day spreads.
        # *** NOTE ***
        # This soft constraint is currently not considered as the preferred time slots tok higher precendence than
        # the time slot configuration
        enthusiasm_score_for_preferred_days = 1
        if preferred_course_day_spread_list:
            enthusiasm_score_for_preferred_days = 0

            if len(timeslot_config) == 3 and "TWF" in preferred_course_day_spread_list:
                enthusiasm_score_for_preferred_days += 1
            elif len(timeslot_config) == 2 and "MTh" in preferred_course_day_spread_list:
                enthusiasm_score_for_preferred_days += 1
            elif len(timeslot_config) == 1:
                if time_codes[timeslot_config[0][0].lower()] in preferred_course_day_spread_list:
                    enthusiasm_score_for_preferred_days += 1

        # CSP 2 Soft Constraint 2 for professor preferred teaching hour preferences.
        semester = variable.split("_")[1]
        prof_preferred_course_times_in_semester = self.professors[prof_id]["preferredTimes"][semester] # could be null

        satisfaction_preferred_times = 1
        if prof_preferred_course_times_in_semester:
            # Get the days in the candidate timeslot.
            days = []
            # If the assigned timeslot config is a 3-day config:
            if len(timeslot_config) == 3:
                days = ["tuesday", "wednesday", "friday"]
            elif len(timeslot_config) == 2:
                days = ["monday", "thursday"]
            else:
                days = [timeslot_config[0][0].lower()]

            # Compute satisfaction provided by this timeslot.
            satisfaction_score_total = 0
            for day in days:
                satisfaction_score_day = 1

                if prof_preferred_course_times_in_semester[day] is not None:
                    # Compute quality score for day by comparing the assigned time with the preferred ranges.
                    start_time = timeslot_config[0][1]
                    end_time = timeslot_config[0][2]
                    worst_diffs = []
                    for time_range in prof_preferred_course_times_in_semester[day]:
                        # Get preferred start time.
                        pref_start_time_tuple = time_range[0].split(":")
                        preferred_start_time = datetime.datetime(100, 1, 1, int(pref_start_time_tuple[0]), int(pref_start_time_tuple[1]))
                        # Get preferred end time.
                        pref_end_time_tuple = time_range[1].split(":")
                        preferred_end_time = datetime.datetime(100, 1, 1, int(pref_end_time_tuple[0]), int(pref_end_time_tuple[1]))
                        # If assigned time begins before preferred start time, record the difference.
                        start_diff = datetime.timedelta(seconds=0)
                        if start_time < preferred_start_time:
                            start_diff = preferred_start_time - start_time
                        # If assigned time ends after preferred end time, record the difference.
                        end_diff = datetime.timedelta(seconds=0)
                        if end_time > preferred_end_time:
                            end_diff = end_time - preferred_end_time
                        # Determine which of the start time, end time is a worse violation of the preferred time.
                        worst_diff = max(start_diff.seconds, end_diff.seconds)
                        # Record the worst violation.
                        worst_diffs.append(worst_diff)
                    # Compute satisfaction score for the assigned timeslot relative to
                    # the preferred time range to which the assigned timeslot is the closest.
                    satisfaction_score_day -= min(worst_diffs) / 45000
                satisfaction_score_total += satisfaction_score_day
            satisfaction_preferred_times = satisfaction_score_total / len(days)

        return ((satisfaction_preferred_times * 2) + enthusiasm_score_for_preferred_days) / 3


