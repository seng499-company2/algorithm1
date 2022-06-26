from typing import Generic, TypeVar, Dict, List, Optional

from constraints import Qualified_Course_Prof, Course_Requires_PENG, Professor_Teaching_Load
from datamodels import *
from csp import CSP
import sys


def generate_schedule(historicalData, professors, schedule):
    return "Algorithm 1 OK"

# Create variables.
variables_csp_1 = []
for course in temp_courses:
    variables_csp_1.append(course)

# Create domains.
domains_csp_1 = {}
for course in variables_csp_1 :
    domain = []
    for prof in temp_profs:
        domain.append(prof)
    domains_csp_1[course] = domain

# Initialize CSP object.
csp_1 = CSP(variables_csp_1, domains_csp_1)

# Add constraints.
for course in variables_csp_1:
    csp_1.add_constraint(Qualified_Course_Prof(course))

    if temp_courses[course]["pengRequired"]:
        csp_1.add_constraint(Course_Requires_PENG(course))


csp_1.add_constraint(Professor_Teaching_Load(variables_csp_1))


# Run search.
solution_csp_1 = csp_1.backtracking_search()

print("Solving CSP 1. . . ")
csp_1_solved = False
solution_csp_1 = csp_1.backtracking_search()

# If no solution to CSP 1, quit.
if solution_csp_1 is None:
    print("No solution found!")
    sys.exit(0)

# If CSP 1 solved, print results.
csp_1_solved = True
print("Done CSP 1!")
print()
print('CSP 1 results:')
sum_pref_score = 0
for course in solution_csp_1:
    line = ""
    line = line + course + "\t\t"
    line = line + solution_csp_1[course] + "\t\t"
    print(line)
print()
