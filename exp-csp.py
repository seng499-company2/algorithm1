# Experimental implementation of simple csp scheduling algorithm

# From / based on: https://freecontent.manning.com/constraint-satisfaction-problems-in-python/


import random
import time
import sys

################################################################
# CSP solver framework:

from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractmethod
  
V = TypeVar('V') # variable type
D = TypeVar('D') # domain type
  

# Base class for all constraints
class Constraint(Generic[V, D], ABC):
    # The variables that the constraint is between
    def __init__(self, variables: List[V]) -> None:
        self.variables = variables
  
    # Must be overridden by subclasses
    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
         return


# A constraint satisfaction problem consists of variables of type V
# that have ranges of values known as domains of type D and constraints
# that determine whether a particular variable's domain selection is valid
class CSP(Generic[V, D]):
    
    # Creates constraints dict.
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        
        # Variables to be constrained
        self.variables: List[V] = variables

        # Domain of each variable
        self.domains: Dict[V, List[D]] = domains

        # Constraints
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain assigned to it.")
  
    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)

    # Check if the value assignment is consistent by checking all constraints
    # for the given variable against it
    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search(self, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        # Assignment is complete if every variable is assigned (our base case)
        if len(assignment) == len(self.variables):
            return assignment
  
        # Get all variables in the CSP but not in the assignment
        unassigned: List[V] = [v for v in self.variables if v not in assignment]
  
        # Get the every possible domain value of the first unassigned variable
        first: V = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            # If we're still consistent, we recurse (continue)
            if self.consistent(first, local_assignment):
                result: Optional[Dict[V, D]] = self.backtracking_search(local_assignment)
                # If we didn't find the result, we will end up backtracking
                if result is not None:
                    return result
        return None


################################################################
# CSP scheduler prototype.

class Course:
    def __init__(self, name, academic_year, pengRequired = False, instructor = None, timeslot_configuration = None):
        self.name_ = name
        self.academic_year_ = academic_year
        self.pengRequired_ = pengRequired
        self.instructor_ = instructor
        self.timeslot_configuration = timeslot_configuration

class TimeSlot:
    def __init__(self, day, start, end):
        self.day_ = day
        self.start_ = start
        self.end_ = end

class TimeSlotConfiguration:
    def __init__(self, timeslots):
        self.timeslots_ = timeslots

class Instructor:
    def __init__(self, name, qualifications, teaching_load, preferred_times = None):
        self.name_ = name
        self.qualifications_ = qualifications
        self.teaching_load_ = teaching_load
        self.preferred_times_ = preferred_times

# Hard constraint: instructors may only be assigned to courses for which they are qualified.
# Note: this connstraint currently isn't used.
# Instead, we exclude any unqualified professors from the domain of each variable in CSP 1.
class CourseInstructorQualificationsConstraint(Constraint[Course, Instructor]):
    def __init__(self, course: Course) -> None:
        super().__init__([course])
        self.course_ = course

    def satisfied(self, assignment: Dict[Course, Instructor]) -> bool:
        if self.course_ not in assignment:
            return True

        if self.course_.name_ in (assignment[self.course_]).instructor_.qualifications_:
            return True
        else:
            return False

# Hard constraint: the specified courses may not be assigned to overlapping timeslots.
class CourseTimeslotOverlapConstraint(Constraint[Course, TimeSlotConfiguration]):
    def __init__(self, courses: List[Course]) -> None:
        super().__init__(courses)
        self.courses_: List[Course] = courses

    def satisfied(self, assignment: Dict[Course, TimeSlotConfiguration]) -> bool:
        # Obtain all timeslots for the courses to which this constraint applies.
        timeslots: List[TimeSlot] = []
        for course in self.courses_:
            if course not in assignment:
                continue
            for timeslot in assignment[course].timeslots_:
                timeslots.append(timeslot)

        # Check for conflicts.
        for i in range(len(timeslots)):
            for j in range(i + 1, len(timeslots)):
                if (timeslots[i].day_ == timeslots[j].day_):
                    if (timeslots[i].start_ >= timeslots[j].start_ and timeslots[i].start_ <= timeslots[j].end_):
                        return False
                    if (timeslots[j].start_ >= timeslots[i].start_ and timeslots[j].start_ <= timeslots[i].end_):
                        return False
        return True

# Soft constraint: instructors should only be scheduled to teach when they are available.
# Creates a score indicating how much assigned teaching time falls outside of professor's preferred hours.
# If this score exceeds a threshold, then the constraint is violated.
class InstructorAvailabilityConstraint(Constraint[Course, TimeSlotConfiguration]):
    def __init__(self, courses: Course) -> None:
        super().__init__(courses)
        self.courses_ = courses

    def satisfied(self, assignment: Dict[Course, TimeSlotConfiguration]) -> bool:
        score = 0
        for course in self.courses_:
            if course not in assignment:
                continue
            for timeslot in assignment[course].timeslots_:
                for preferred_time in course.instructor_.preferred_times_:
                    if (timeslot.day_ == preferred_time.day_):
                        if (timeslot.start_ < preferred_time.start_):
                            score -= (preferred_time.start_ - timeslot.start_) ** 2
                        if (preferred_time.end_ < timeslot.end_):
                            score -= (timeslot.end_ - preferred_time.end_) ** 2
        if (score < -400):
            return False
        
        return True

class InstructorTeachingLoadConstraint(Constraint[Course, Instructor]):
    def __init__(self, courses: List[Course]) -> None:
        super().__init__(courses)
        self.courses_: List[Course] = courses
    
    def satisfied(self, assignment: Dict[Course, Instructor]) -> bool:
        teaching_loads_dict = {instructor.name_ : 0 for instructor in instructors}
        for course in self.courses_:
            if course not in assignment:
                continue
            teaching_loads_dict[assignment[course].name_] += 1
        for instructor in instructors:
            if (teaching_loads_dict[instructor.name_] > instructor.teaching_load_):
                return False
        return True

class InstructorNoDoubleBookingConstraint(Constraint[Course, TimeSlotConfiguration]):
    def __init__(self, courses: List[Course]) -> None:
        super().__init__(courses)
        self.courses_: List[Course] = courses

    def satisfied(self, assignment: Dict[Course, TimeSlotConfiguration]) -> bool:
        timeslots = []
        for course in self.courses_:
            if course not in assignment:
                continue
            timeslots += assignment[course].timeslots_

        for i in range(len(timeslots)):
                for j in range(i + 1, len(timeslots)):
                    if (timeslots[i].day_ == timeslots[j].day_):
                        if (timeslots[i].start_ >= timeslots[j].start_ and timeslots[i].start_ <= timeslots[j].end_):
                            return False
                        if (timeslots[j].start_ >= timeslots[i].start_ and timeslots[j].start_ <= timeslots[i].end_):
                            return False

        return True

class InstructorCoursePreferenceConstraint(Constraint[Course, Instructor]):
    def __init__(self, courses: List[Course]) -> None:
        super().__init__(courses)
        self.courses_: List[Course] = courses

    # Constraint on per-professor means of preference scores
    def satisfied(self, assignment: Dict[Course, Instructor]) -> bool:
        assigned_courses_dict = {instructor.name_ : [] for instructor in instructors}
        for course in self.courses_:
            if course not in assignment:
                continue
            assigned_courses_dict[assignment[course].name_].append(course)
        
        for instructor in instructors:
            if (len(assigned_courses_dict[instructor.name_]) > 0):
                sum = 0
                for course in assigned_courses_dict[instructor.name_]:
                    sum += instructor.qualifications_[course.name_]
                mean = sum / len(assigned_courses_dict[instructor.name_])
                if mean < 120:
                    return False
        return True            

if __name__ == "__main__":
    
    start_time = time.time()

    ################################################
    # CSP 1: assign professors to courses
    print("Intiializing CSP 1: assign professors to courses.")

    # Initialize variables.
    print("Initializing variables.")
    variables: List[Course] = [Course("CSC111", 1, True),
                               Course("CSC115", 1),
                               Course("CSC230", 2, True), Course("SENG265", 2, True),
                               Course("CSC225", 2), Course("SENG275", 2, True), Course("SENG310", 2, True),
                               Course("CSC361", 3, True), Course("CSC226", 3), Course("SENG321", 3, True), Course("SENG371", 3, True),
                               Course("CSC355", 3), Course("CSC320", 3), Course("CSC360", 3, True), Course("CSC370", 3), Course("SENG350", 3), Course("SENG360", 3),
                               Course("SENG401", 4, True), Course("CSC460", 4)]

    # Initialize domains.
    print("Initializing domains.")
    instructors: List[Instructor] = [Instructor("Berg, Celina", {"CSC111" : 78, "CSC115" : 20, "CSC225" : 20, "CSC226" : 20, "CSC230" : 20, "SENG265" : 20, "SENG275": 20, "CSC370" : 20, "SENG310" : 78, "SENG350" : 20}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Bird, Bill", {"CSC111" : 78, "CSC115" : 20, "CSC225" : 20, "CSC226" : 20, "CSC230" : 20, "CSC355" : 78, "CSC360" : 20, "CSC370" : 20, "SENG310" : 195}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Chester, Sean", {"CSC111" : 40, "CSC115" : 40, "SENG275" : 195, "CSC361" : 78, "CSC460" : 78}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Corless, Jason", {"CSC111" : 195, "CSC115" : 40, "CSC225" : 40, "CSC226" : 40, "CSC230" : 40, "CSC355" : 195, "CSC361" : 78, "CSC460" : 78}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Damian, Daniela", {"CSC111" : 78, "CSC115" : 20, "CSC225" : 195, "CSC226" : 20, "CSC230" : 195, "SENG265" : 20, "CSC320" : 20, "CSC355" : 40, "CSC360" : 78, "CSC370" : 78, "SENG321" : 39}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Ernst, Neil", {"CSC111" : 78, "CSC115" : 78, "CSC225" : 40, "CSC226" : 20, "CSC230" : 78, "SENG275" : 20, "CSC320" : 20, "CSC355" : 78, "CSC360" : 40, "CSC370" : 20, "SENG310" : 78, "SENG321" : 20, "SENG360" : 20, "SENG401" : 40}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Estey, Anthony", {"CSC115" : 78, "CSC226" : 78, "SENG275" : 78}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Ganti, Sudhakar", {"CSC111" : 78, "CSC115" : 195, "CSC230" : 20, "SENG275" : 20, "CSC355" : 78}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("German, Daniel", {"CSC111" : 78, "CSC230" : 78, "SENG265" : 78, "CSC355" : 20, "CSC361" : 40, "SENG310" : 20, "SENG321" : 195, "SENG350" : 195, "SENG360" : 20, "SENG371" : 20, "CSC460" : 40, "SENG401" : 195}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Haworth, Brando", {"CSC111" : 40, "CSC115" : 40, "CSC225" : 20, "CSC226" : 40, "CSC355" : 40, "CSC360" : 195}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Jabbari, Hosna", {"CSC111" : 40}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Jackson, LillAnne", {"CSC111" : 40, "CSC115" : 78, "CSC225" : 40, "CSC226" : 40}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Kapron, Bruce", {"CSC111" : 40, "CSC115" : 20, "CSC225" : 40, "CSC226" : 20, "CSC320" : 20, "CSC355" : 78, "CSC360" : 20, "CSC361" : 195, "CSC370" : 195, "SENG371" : 20}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("King, Valerie", {"CSC111" : 20, "CSC230" : 40, "SENG265" : 40, "CSC355" : 20, "CSC370" : 40, "SENG321" : 40, "SENG350" : 195, "SENG360" : 195, "SENG401" : 78}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Koroth, Sajin", {"CSC111" : 78, "CSC115" : 20, "CSC225" : 20, "CSC226" : 20, "CSC230" : 20, "CSC355" : 78, "CSC360" : 20, "CSC370" : 20, "CSC310" : 195}, 4, [TimeSlot("Mon", 830, 1230), TimeSlot("Tue", 830, 1230), TimeSlot("Wed", 830, 1230), TimeSlot("Thu", 830, 1230), TimeSlot("Fri", 830, 1230)]),
                                     Instructor("Little, Rich", {"CSC111" : 20, "CSC115" : 20, "CSC226" : 20, "CSC230" : 20, "SENG265" : 195, "CSC355" : 20, "CSC370" : 20, "CSC310" : 195, "SENG321" : 20, "CSC460" : 40, "SENG401" : 20}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Mehta, Nishant", {"CSC111" : 20, "CSC115" : 40, "CSC226" : 40, "SENG275" : 195, "CSC355" : 20}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Muller, Hausi", {"CSC111" : 195, "CSC115" : 195, "CSC225" : 195, "CSC226" : 195, "CSC230" : 195, "SENG276" : 40, "SENG275" : 40, "CSC320" : 40, "CSC355" : 78, "CSC360" : 40}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Nacenta, Miguel", {"CSC111" : 20, "CSC115" : 20, "CSC230" : 40, "SENG265" : 20, "CSC355" : 20, "SENG310" : 195, "SENG321" : 40}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Numanaqic, Ibrahim", {"CSC111" : 20, "CSC355" : 20, "SENG310" : 195}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Pan, Jianping", {"CSC115" : 20, "CSC226" : 78, "SENG371" : 195}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Perin, Charles", {"CSC111" : 40, "CSC115" : 195, "CSC225" : 40, "CSC226" : 195, "SENG275" : 195, "CSC355" : 40, "CSC370" : 40}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Scheider, Teseo", {"CSC111" : 20, "CSC115" : 195, "CSC226" : 195, "CSC230" : 78, "SENG275" : 20, "CSC355" : 78, "CSC361" : 40, "SENG371" : 40, "SENG401" : 40}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Somanath, Sowmy", {"CSC111" : 195, "CSC115" : 78, "CSC225" : 195, "CSC226" : 20, "CSC230" : 40, "CSC320" : 195, "CSC355" : 78, "CSC360" : 40, "CSC361" : 40, "SENG350" : 40}, 4,[TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Srinivasan, Venkatesh", {"CSC111" : 20, "CSC225" : 195, "CSC320" : 195, "CSC355" : 78, "CSC360" : 40, "SENG350" : 40}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Stege, Ulrike", {"CSC115" : 40, "SENG275" : 20, "SENG371" : 20}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Storey, Margaret-Anne", {"CSC115" : 20, "CSC226" : 78, "SENG371" : 195}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Summers, Cecilia", {"CSC226" : 78, "SENG275" : 195}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Thomo, Alex", {"CSC111" : 40, "CSC115" : 40, "CSC226" : 40, "CSC370" : 195, "SENG371" : 195}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Tzanetakis, George", {"CSC115" : 40, "CSC226" : 20, "SENG265" : 20, "CSC355" : 40, "CSC361" : 20, "CSC370" : 78, "SENG371" : 40, "CSC460" : 20}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Weber, Jens", {"CSC230" : 40, "CSC361" : 39, "SENG321" : 78, "CSC460" : 39}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Wu, Kui", {"CSC111" : 195, "CSC225" : 195, "CSC230" : 195, "SENG265" : 20, "CSC355" : 78, "CSC360" : 195, "SENG350" : 40}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)]),
                                     Instructor("Zastre, Michael", {"CSC111" : 40, "CSC115" : 78, "CSC225" : 78, "CSC226" : 40, "CSC230" : 195, "SENG265" : 20, "SENG275" : 40, "CSC355" : 195, "CSC360" : 78, "CSC370" : 39, "SENG310" : 40}, 4, [TimeSlot("Mon", 830, 1830), TimeSlot("Tue", 830, 1830), TimeSlot("Wed", 830, 1830), TimeSlot("Thu", 830, 1830), TimeSlot("Fri", 830, 1830)])]

    domains_csp_1: Dict[Course, List[Instructor]] = {}
    for course in variables:
        domain: List[Instructor] = []
        for instructor in instructors:
            # For each course, exclude professors that are not qualified for that course
            if (course.name_ in instructor.qualifications_):
                domain.append(instructor)
        domains_csp_1[course] = domain

    # Initialize CSP 1 solver.
    print("Initializing CSP 1 solver.")
    csp_1: CSP[Course, Instructor] = CSP(variables, domains_csp_1)

    # Initialize CSP 1 constraints.
    print("Adding constraints.")
    csp_1.add_constraint(InstructorTeachingLoadConstraint(variables))
    csp_1.add_constraint(InstructorCoursePreferenceConstraint(variables))

    # Solve CSP 1. If solution found, print the assignments of professors and timeslots to courses.
    print("Solving CSP 1. . . ")
    csp_1_solved = False
    solution_csp_1: Optional[Dict[Course, Instructor]] = csp_1.backtracking_search()
    
    # If no solution to CSP 1, quit.
    if solution_csp_1 is None:
        print("No solution found!")
        stop_time = time.time()
        runtime = stop_time - start_time
        print('Time elapsed: ', runtime)
        sys.exit()
  
    # If CSP 1 solved, print results.
    csp_1_solved = True
    print("Done CSP 1!")
    print()
    print('CSP 1 results:')
    sum_pref_score = 0
    for course in solution_csp_1:
        line = ""
        line = line + course.name_ + "\t\t"
        line = line + solution_csp_1[course].name_ + "\t\t"
        line = line + str(solution_csp_1[course].qualifications_[course.name_]) + "\t\t"
        print(line)
        sum_pref_score += solution_csp_1[course].qualifications_[course.name_]
    mean_pref_score = sum_pref_score / len(solution_csp_1)
    print("Mean pref score: " + str(mean_pref_score))
    print()

    ################################################
    # CSP 2: assign timeslots to courses.
    print("Intiializing CSP 2: assign courses to timeslots.")

    # Update variables with CSP 1 results.
    # Now our variables have form (course, instructor).
    for course in variables:
        course.instructor_ = solution_csp_1[course]

    # Create domains.
    print("Initializing domains.")
    timeslot_configurations: List[TimeSlotConfiguration] = []
    
    def add_30_mins(time_val):
        mins = time_val % 100
        mins += 30
        if mins >= 60:
            time_val += 100
            mins = mins % 60
        time_val = time_val - (time_val % 100) + mins
        return time_val 

    start = 830
    end = 950
    while end < 2200:
        timeslot_configurations.append(TimeSlotConfiguration([TimeSlot("Mon", start, end), TimeSlot("Thu", start, end)]))
        start = add_30_mins(start)
        end = add_30_mins(end)

    start = 830
    end = 920
    while end < 2200:
        timeslot_configurations.append(TimeSlotConfiguration([TimeSlot("Tue", start, end), TimeSlot("Wed", start, end), TimeSlot("Fri", start, end)]))
        start = add_30_mins(start)
        end = add_30_mins(end)

    start = 830
    end = 1120
    while end < 2200:
        days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        for day in days:
            timeslot_configurations.append(TimeSlotConfiguration([TimeSlot(day, start, end)]))
        start = add_30_mins(start)
        end = add_30_mins(end)

    domains_csp_2: Dict[Course, List[TimeSlotConfiguration]] = {}
    for course in variables:
        domains_csp_2[course] = timeslot_configurations

    # Initialize CSP 2 solver and add constraints.
    print("Initializing CSP 2 solver.")
    csp_2: CSP[Course, Instructor] = CSP(variables, domains_csp_2)

    print("Adding constraints.")
    for instructor in instructors:
        courses = [course for course in variables if course.instructor_.name_ == instructor.name_]
        if (len(courses) > 0):
            pass
            csp_2.add_constraint(InstructorNoDoubleBookingConstraint(courses))
            csp_2.add_constraint(InstructorAvailabilityConstraint(courses))

    first_year_courses = [course for course in variables if course.academic_year_ == 1]
    second_year_courses = [course for course in variables if course.academic_year_ == 2]
    third_year_courses = [course for course in variables if course.academic_year_ == 3]
    fourth_year_courses = [course for course in variables if course.academic_year_ == 4]
    csp_2.add_constraint(CourseTimeslotOverlapConstraint(first_year_courses))
    csp_2.add_constraint(CourseTimeslotOverlapConstraint(second_year_courses))
    csp_2.add_constraint(CourseTimeslotOverlapConstraint(third_year_courses))
    csp_2.add_constraint(CourseTimeslotOverlapConstraint(fourth_year_courses))

    # Solve CSP 2. If solution found, print the assignments of professors and timeslots to courses.
    print("Solving. . . ")
    solution_2: Optional[Dict[Course, TimeSlotConfiguration]] = csp_2.backtracking_search()
    if solution_2 is None:
        print("No solution found!")
    else:
        print("Done!")
        print()
        print('Timetable:')
        sum_pref_score = 0
        for course in solution_2:
            line = ""
            line = line + course.name_ + "\t\t"
            line = line + course.instructor_.name_ + "\t\t"
            line = line + str(course.instructor_.qualifications_[course.name_]) + "\t\t"
            for timeslot in solution_2[course].timeslots_:
                line = line + timeslot.day_ + ": " + str(timeslot.start_) + " " + str(timeslot.end_) + "\t\t"
            print(line)
            sum_pref_score += course.instructor_.qualifications_[course.name_]
        mean_pref_score = sum_pref_score / len(solution_2)
        print("Mean pref score: " + str(mean_pref_score))

    stop_time = time.time()
    runtime = stop_time - start_time
    print('Time elapsed: ', runtime)