from constraint import *


def main():
    num_solutions_to_show = 3

    # Note: data does not reflect the real world and is for testing only
    courses = {
        "csc110": {"pengRequired": False},
        "csc111": {"pengRequired": False},
        "seng265": {"pengRequired": False},
        "csc225": {"pengRequired": False},
        "csc226": {"pengRequired": False},
        "ece260": {"pengRequired": True},
        "ece310": {"pengRequired": True},
        "seng475": {"pengRequired": True}
    }

    # Note: data does not reflect the real world and is for testing only
    profs = {
        "Bird": {
            "isPeng": False,
            "qualifiedCourses": ["csc110", "csc111", "csc225", "csc226"],
            "teachingObligations": 2
        },
        "Zastre": {
            "isPeng": False,
            "qualifiedCourses": ["csc110", "csc111", "seng265"],
            "teachingObligations": 1
        },
        "Tzanatakis": {
            "isPeng": False,
            "qualifiedCourses": ["csc225", "csc226"],
            "teachingObligations": 3
        },
        "Adams": {
            "isPeng": True,
            "qualifiedCourses": ["ece260", "seng475"],
            "teachingObligations": 2
        },
        "Gebali": {
            "isPeng": True,
            "qualifiedCourses": ["ece260", "ece310"],
            "teachingObligations": 1
        }
    }

    # Split profs into peng profs and non peng profs
    peng_profs = {k: v for (k, v) in profs.items() if v["isPeng"] is True}
    no_peng_profs = {k: v for (k, v) in profs.items() if v["isPeng"] is False}

    # Split courses into isPeng profs required and non peng profs
    peng_course = {k: v for (k, v) in courses.items() if v["pengRequired"] is True}
    no_peng_course = {k: v for (k, v) in courses.items() if v["pengRequired"] is False}

    problem = Problem()

    # For each course generate a list of qualified professors based on peng and the courses they can teach
    for course in courses:
        qual_prof_list = []

        for prof in profs:
            if course in profs.get(prof)["qualifiedCourses"]:
                if (courses.get(course)["pengRequired"] is True and profs.get(prof)["isPeng"] is True) or \
                        courses.get(course)["pengRequired"] is False:
                    qual_prof_list.append(prof)

        # Add a variable for each course with that course's qualified prof list as possible assignment values
        problem.addVariable(course, qual_prof_list)

    # Maximum number of courses a prof can teach constraint
    for i, item in enumerate(list(profs.keys())):
        problem.addConstraint(
            SomeNotInSetConstraint({list(profs.keys())[i]}, len(courses) - profs.get(item)["teachingObligations"], False))

    # Create an iterator to call repeatedly. Each call to next(solution_iter) returns a possible schedule.
    solution_iter = problem.getSolutionIter()

    # problem.getSolutions() returns a list of all possible solutions
    total = len(problem.getSolutions())

    # Call the iterator some number of times until there are no possible solutions left.
    try:
        for i in range(num_solutions_to_show):
            print("Solution {}:\n{}\n".format(i, next(solution_iter)))
    except StopIteration:
        print("No more possible solutions found.")

    print("\nTotal solutions: {}".format(total))


if __name__ == '__main__':
    main()
