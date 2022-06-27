from typing import List, TypeVar

from .datamodels import temp_profs, temp_courses, courses, professors
from .csp import Constraint

V = TypeVar('V')  # variable type
D = TypeVar('D')  # domain type


# Hard constraint: instructors may only be assigned to courses for which they are qualified.
# Note: this constraint currently isn't used.
# Instead, we exclude any unqualified professors from the domain of each variable in CSP 1.
class Qualified_Course_Prof(Constraint):
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

class Course_Requires_PENG(Constraint):
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

class Professor_Teaching_Load(Constraint):
    def __init__(self, courses) -> None:
        super().__init__(courses)

    def satisfied(self, assignment) -> bool:
        teaching_loads_dict = {prof : 0 for prof in temp_profs}

        for course in self.variables:
            if course not in assignment:
                continue
            prof = assignment[course]
            teaching_loads_dict[prof] += 1

        for prof, teachingLoad in teaching_loads_dict.items():
            if teachingLoad > temp_profs[prof]["teachingObligations"]:
                return False

        return True

# TODO: Create timeslots for the courses
# TODO: Create the hard constraints for:
#  overlapping courses
#  no-double booked professor

# Hard constraint: the specified courses may not be assigned to overlapping timeslots.
# class CourseTimeslotOverlapConstraint(Constraint):
#     def __init__(self, courses) -> None:
#         super().__init__(courses)
#         self.courses_ = courses
#
#     def satisfied(self, assignment) -> bool:
#         # Obtain all timeslots for the courses to which this constraint applies.
#         timeslots: List[TimeSlot] = []
#         for course in self.courses_:
#             if course not in assignment:
#                 continue
#             for timeslot in assignment[course].timeslots_:
#                 timeslots.append(timeslot)
#
#         # Check for conflicts.
#         for i in range(len(timeslots)):
#             for j in range(i + 1, len(timeslots)):
#                 if (timeslots[i].day_ == timeslots[j].day_):
#                     if (timeslots[i].start_ >= timeslots[j].start_ and timeslots[i].start_ <= timeslots[j].end_):
#                         return False
#                     if (timeslots[j].start_ >= timeslots[i].start_ and timeslots[j].start_ <= timeslots[i].end_):
#                         return False
#         return True


# # Soft constraint: instructors should only be scheduled to teach when they are available.
# # Creates a score indicating how much assigned teaching time falls outside of professor's preferred hours.
# # If this score exceeds a threshold, then the constraint is violated.
# class InstructorAvailabilityConstraint(Constraint[Course, TimeSlotConfiguration]):
#     def __init__(self, courses: Course) -> None:
#         super().__init__(courses)
#         self.courses_ = courses
#
#     def satisfied(self, assignment: Dict[Course, TimeSlotConfiguration]) -> bool:
#         score = 0
#         for course in self.courses_:
#             if course not in assignment:
#                 continue
#             for timeslot in assignment[course].timeslots_:
#                 for preferred_time in course.instructor_.preferred_times_:
#                     if (timeslot.day_ == preferred_time.day_):
#                         if (timeslot.start_ < preferred_time.start_):
#                             score -= (preferred_time.start_ - timeslot.start_) ** 2
#                         if (preferred_time.end_ < timeslot.end_):
#                             score -= (timeslot.end_ - preferred_time.end_) ** 2
#         if (score < -400):
#             return False
#
#         return True
#
#
# class InstructorNoDoubleBookingConstraint(Constraint[Course, TimeSlotConfiguration]):
#     def __init__(self, courses: List[Course]) -> None:
#         super().__init__(courses)
#         self.courses_: List[Course] = courses
#
#     def satisfied(self, assignment: Dict[Course, TimeSlotConfiguration]) -> bool:
#         timeslots = []
#         for course in self.courses_:
#             if course not in assignment:
#                 continue
#             timeslots += assignment[course].timeslots_
#
#         for i in range(len(timeslots)):
#             for j in range(i + 1, len(timeslots)):
#                 if (timeslots[i].day_ == timeslots[j].day_):
#                     if (timeslots[i].start_ >= timeslots[j].start_ and timeslots[i].start_ <= timeslots[j].end_):
#                         return False
#                     if (timeslots[j].start_ >= timeslots[i].start_ and timeslots[j].start_ <= timeslots[i].end_):
#                         return False
#
#         return True
#
#
# class InstructorCoursePreferenceConstraint(Constraint[Course, Instructor]):
#     def __init__(self, courses: List[Course]) -> None:
#         super().__init__(courses)
#         self.courses_: List[Course] = courses
#
#     # Constraint on per-professor means of preference scores
#     def satisfied(self, assignment: Dict[Course, Instructor]) -> bool:
#         assigned_courses_dict = {instructor.name_: [] for instructor in instructors}
#         for course in self.courses_:
#             if course not in assignment:
#                 continue
#             assigned_courses_dict[assignment[course].name_].append(course)
#
#         for instructor in instructors:
#             if (len(assigned_courses_dict[instructor.name_]) > 0):
#                 sum = 0
#                 for course in assigned_courses_dict[instructor.name_]:
#                     sum += instructor.qualifications_[course.name_]
#                 mean = sum / len(assigned_courses_dict[instructor.name_])
#                 if mean < 120:
#                     return False
#         return True
#
