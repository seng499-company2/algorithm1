# Experimental implementation of simple csp scheduling algorithm

# From / based on: https://freecontent.manning.com/constraint-satisfaction-problems-in-python/

################################################################
# CSP solver framework:

from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractmethod

V = TypeVar('V')  # variable type
D = TypeVar('D')  # domain type


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

    def backtracking_search(self, config=None) -> Optional[Dict[V, D]]:
        if config is not None and config.get('mrv') is True and config.get('degree') is True:
            print("Cannot use MRV and Degree variable heuristics simultaneously. Please modify config.")
            exit()

        # If using MRV heuristic, sort variables in increasing order of domain size.
        if config is not None and config.get('mrv'):
            def get_domain_size(var):
                return len(self.domains[var])
            self.variables.sort(key=get_domain_size)

        # If using degree heuristic, sort variables in decreasing order of degree.
        if config is not None and config.get('degree'):
            constraints_degrees = []
            for var in self.variables:
                curr_constraints = self.constraints[var]
                curr_degree = 0
                for constraint in curr_constraints:
                    curr_degree += len(constraint.variables) - 1
                constraints_degrees.append(curr_degree)

            zipped_degrees_constraints = list(zip(constraints_degrees, self.variables))
            zipped_sorted = sorted(zipped_degrees_constraints, key=lambda x: x[0])
            self.variables = list(zip(*zipped_sorted))[1]

        variable_conflict_set = {}
        if config["forward_checking"]:
            for variable in self.variables:
                curr_conflicting_variables = []
                for constraint in self.constraints[variable]:
                    for const_var in constraint.variables:
                        if const_var != variable and const_var not in curr_conflicting_variables:
                            curr_conflicting_variables.append(const_var)
                variable_conflict_set[variable] = curr_conflicting_variables

        # Backtracking search with no forward checking
        def backtracking_search_recursive(assignment_: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
            # Assignment is complete if every variable is assigned (our base case)
            if len(assignment_) == len(self.variables):
                return assignment_

            # Get all variables in the CSP but not in the assignment
            unassigned: List[V] = [v for v in self.variables if v not in assignment_]

            # Get the every possible domain value of the first unassigned variable
            first: V = unassigned[0]
            for value in self.domains[first]:
                local_assignment = assignment_.copy()
                local_assignment[first] = value
                # If we're still consistent, we recurse (continue)
                if self.consistent(first, local_assignment):
                    result_: Optional[Dict[V, D]] = backtracking_search_recursive(local_assignment)
                    # If we didn't find the result, we will end up backtracking
                    if result_ is not None:
                        return result_
            return None

        # Backtracking with forward checking enabled
        def backtracking_search_fc(domains, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
            # Assignment is complete if every variable is assigned (our base case)
            if len(assignment) == len(self.variables):
                return assignment

            # Get all variables in the CSP but not in the assignment
            unassigned: List[V] = [v for v in self.variables if v not in assignment]

            # Get the every possible domain value of the first unassigned variable
            first: V = unassigned[0]
            for value in domains[first]:
                local_assignment = assignment.copy()
                local_assignment[first] = value
                # If we're still consistent, we recurse (continue)
                if self.consistent(first, local_assignment):
                    domains_copy = {k: v.copy() for (k, v) in domains.items()}
                    # For each neighbor of the current variable:
                    for neighbor in variable_conflict_set[first]:
                        # For each value in the neighbor's domain:
                        for value_ in domains_copy[neighbor]:
                            local_assignment_copy = local_assignment.copy()
                            local_assignment_copy[neighbor] = value_
                            # If not consistent:
                            if not self.consistent(neighbor, local_assignment_copy):
                                # Remove value from neighbor's domain.
                                del domains_copy[neighbor][value_]
                            # If neighbor's domain is now empty:
                            if len(domains_copy[neighbor]) <= 0:
                                # Backtrack
                                return None

                    result_: Optional[Dict[V, D]] = backtracking_search_fc(domains=domains_copy,
                                                                           assignment=local_assignment)
                    # If we didn't find the result, we will end up backtracking
                    if result_ is not None:
                        return result_
            return None

        if config["forward_checking"]:
            domains_initial = self.domains.copy()
            result = backtracking_search_fc(domains=domains_initial)
        else:
            result = backtracking_search_recursive()
        return result
