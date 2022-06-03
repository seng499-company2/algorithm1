# Experimental implementation of simple csp scheduling algorithm

# From / based on: https://freecontent.manning.com/constraint-satisfaction-problems-in-python/


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
# Simple scheduler using CSP framework:
# Assigns courses to timeslots.
# Assigns professors to courses.
# Courses in the same year may not occupy overlapping timeslots.
# Professors may only teach courses for which they are qualified.

class Course:
    def __init__(self, name, year):
        self.name_ = name
        self.year_ = year

class TimeSlot:
    def __init__(self, start):
        self.start_ = start 

class Instructor:
    def __init__(self, name, qualifications):
        self.name_ = name
        self.qualifications_ = qualifications

class DomainObject:
    def __init__(self, timeslot, instructor):
        self.timeslot_ = timeslot
        self.instructor_ = instructor

# Constraint: instructors may only be assigned to courses for which they are qualified.
class CourseInstructorQualificationsConstraint(Constraint[Course, DomainObject]):
    def __init__(self, course: Course) -> None:
        super().__init__([course])
        self.course_ = course

    def satisfied(self, assignment: Dict[Course, DomainObject]) -> bool:
        if self.course_ not in assignment:
            return True

        if self.course_.name_ in (assignment[self.course_]).instructor_.qualifications_:
            return True
        else:
            return False

# Constraint: the courses specified by the "courses" parameter may not be assigned to overlapping timeslots.
class CourseTimeslotOverlapConstraint(Constraint[Course, DomainObject]):
    def __init__(self, courses: List[Course]) -> None:
        super().__init__(courses)
        self.courses_: List[Course] = courses

    def satisfied(self, assignment: Dict[Course, DomainObject]) -> bool:
        timeslots: List[TimeSlot] = []
        for course in self.courses_:
            if course not in assignment:
                continue
            timeslots.append(assignment[course].timeslot_.start_)

        # Convert timeslots from a list to a set.
        # If the size does not decrease, then the timeslots are unique, ie they do not overlap.
        return (len(set(timeslots)) == len(timeslots))

if __name__ == "__main__":
    
    # Initialize the "variables". Our variables are courses.
    variables: List[Course] = [Course("CSC111", 1), Course("MATH100", 1), Course("PHYS110", 1),
                                Course("CSC230", 2), Course("SENG265", 2), Course("STAT260", 2),
                                Course("CSC361", 3), Course("ECE360", 3), Course("SENG321", 3),
                                Course("SENG480A", 4), Course("SENG480B", 4), Course("SENG480C", 4)]

    # Initialize domain of the variables.
    # The domain of each course is every possible tuple of form (timeslot, instructor).
    instructors: List[Instructor] = [Instructor("instructor_1", ["CSC111", "MATH100", "PHYS110"]),
                                    Instructor("instructor_2", ["CSC230", "SENG265", "STAT260"]),
                                    Instructor("instructor_3", ["CSC361", "ECE360", "SENG321"]),
                                    Instructor("instructor_4", ["SENG480A", "SENG480B", "SENG480C"])]

    timeslots: List[TimeSlot] = [TimeSlot(830), TimeSlot(930), TimeSlot(1030)]

    domain_objects: List[DomainObject] = []
    for timeslot in timeslots:
        for instructor in instructors:
            domain_objects.append(DomainObject(timeslot, instructor))

    domains: Dict[Course, List[Instructor]] = {}
    for variable in variables:
        domains[variable] = domain_objects

    # Initialize CSP solver and add constraints.
    csp: CSP[Course, DomainObject] = CSP(variables, domains)

    for course in variables:
        csp.add_constraint(CourseInstructorQualificationsConstraint(course))

    first_year_courses = variables[0 : 3]
    second_year_courses = variables[3 : 6]
    third_year_courses = variables[6 : 9]
    fourth_year_courses = variables[9 : ]
    csp.add_constraint(CourseTimeslotOverlapConstraint(first_year_courses))
    csp.add_constraint(CourseTimeslotOverlapConstraint(second_year_courses))
    csp.add_constraint(CourseTimeslotOverlapConstraint(third_year_courses))
    csp.add_constraint(CourseTimeslotOverlapConstraint(fourth_year_courses))

    # Obtain solution. If solution found, print the assignments of professors and timeslots to courses.
    solution: Optional[Dict[Course, DomainObject]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        print("Done!")
        print()
        print('Timetable:')
        for course in solution:
            print(course.name_ + ": " + solution[course].instructor_.name_ + ": " + str(solution[course].timeslot_.start_))
        print()


################################################################
################################################################
# Basic CSP algorithm experiment.
# Assigns professors to classes for which they are qualified.


# class Course:
#     def __init__(self, name, year):
#         self.name_ = name
#         self.year_ = year

# class Instructor:
#     def __init__(self, name, qualifications):
#         self.name_ = name
#         self.qualifications_ = qualifications

# class CourseInstructorQualificationsConstraint(Constraint[Course, Instructor]):
#     def __init__(self, course: Course) -> None:
#         super().__init__([course])
#         self.course_ = course

#     def satisfied(self, assignment: Dict[Course, Instructor]) -> bool:
#         if self.course_ not in assignment:
#             return True

#         print("Iteration:")
#         print("Course: " + self.course_.name_)
#         print("Instructor " + assignment[self.course_].name_)
#         print("Instructor qualifications:")
#         for qual in assignment[self.course_].qualifications_:
#             print(qual)

#         if self.course_.name_ in (assignment[self.course_]).qualifications_:
#             print("ASSIGNED")
#             print()
#             return True
#         else:
#             print("NOT ASSIGNED")
#             print()
#             return False

# if __name__ == "__main__":
#     # Initialize variables (courses).
#     variables: List[Course] = [Course("CSC111", 1), Course("MATH100", 1), Course("PHYS110", 1),
#         Course("CSC230", 2), Course("SENG265", 2), Course("STAT260", 2), Course("CSC361", 3),
#         Course("ECE360", 3), Course("SENG321", 3), Course("SENG480A", 4), Course("SENG480B", 4),
#         Course("SENG480C", 4)]

#     # Initialize domain of each variable (for each, the set of all possible professors).
#     instructors: List[Instructor] = [Instructor("instructor_1", ["CSC111", "MATH100", "PHYS110"]),
#                                     Instructor("instructor_2", ["CSC230", "SENG265", "STAT260"]),
#                                     Instructor("instructor_3", ["CSC361", "ECE360", "SENG321"]),
#                                     Instructor("instructor_4", ["SENG480A", "SENG480B", "SENG480C"])]

#     domains: Dict[Course, List[Instructor]] = {}
#     for variable in variables:
#         domains[variable] = instructors

#     # Initialize CSP and add constraints.
#     csp: CSP[Course, Instructor] = CSP(variables, domains)
#     for course in variables:
#         csp.add_constraint(CourseInstructorQualificationsConstraint(course))

# solution: Optional[Dict[Course, Instructor]] = csp.backtracking_search()
# if solution is None:
#     print("No solution found!")
# else:
#     for course in solution:
#         print(course.name_)
#         print(solution[course].name_)
#         print()