import json
import time

from csp import Constraint
from constraints import professor_teaching_load

from coursescheduler.csp import CSP
from datamodels import tranform_input


# Initial plug & play algorithm
def generate_schedule(historicalData, professors, schedule):
    # Temp load json files as input:
    prof_file = open('temp_json_input/professor_object.json')
    professors = json.load(prof_file)
    for professor in professors:
        for semester, days in professor["preferredTimes"].items():
            for day, timeslots in days.items():
                if timeslots[0] is not None:
                    tuple_list = [tuple(timeslot) for timeslot in timeslots]
                else:
                    tuple_list = None
                professor["preferredTimes"][semester][day] = tuple_list
    prof_file.close()

    schedule_file = open('temp_json_input/schedule_object.json')
    schedule = json.load(schedule_file)
    schedule_file.close()

    courses, professors = tranform_input(schedule, professors)

    non_static_courses = {
        "fall": {k: v for (k, v) in courses["fall"].items() if v["professor"] is None},
        "spring": {k: v for (k, v) in courses["spring"].items() if v["professor"] is None},
        "summer": {k: v for (k, v) in courses["summer"].items() if v["professor"] is None}
    }

    peng_profs = {k: v for (k, v) in professors.items() if v["isPeng"]}

    # set domains
    domains_csp_1 = {}
    for semester, offerings in non_static_courses.items():
        for course, course_data in offerings.items():
            original_course_id = course.split("_")[0]
            if course_data["pengRequired"]:
                qualified_peng_profs = {k: v for (k, v) in peng_profs.items() if v["qualifiedCoursePreferences"][original_course_id] != 0}
                if len(qualified_peng_profs) > 0:
                    domains_csp_1[course] = qualified_peng_profs
            else:
                qualified_profs = {k: v for (k, v) in professors.items() if
                                   v["qualifiedCoursePreferences"][original_course_id] != 0}
                if len(qualified_profs) > 0:
                    domains_csp_1[course] = qualified_profs

    # initialize csp solvers
    course_variables = []
    course_variables.extend(list(non_static_courses["fall"].keys()))
    course_variables.extend(list(non_static_courses["spring"].keys()))
    course_variables.extend(list(non_static_courses["summer"].keys()))

    csp_1 = CSP(course_variables, domains_csp_1)

    # add constraints
    csp_1.add_constraint(professor_teaching_load(course_variables, professors))

    # set search config values
    config = {
            "mrv": True,
            "degree": False,
            "forward_checking": False,
            "max_steps": 50000
        }

    # run search
    start = time.time()
    solution_csp_1 = csp_1.backtracking_search(config=config)
    end = time.time()
    print(f"Time taken is: {end-start}" )
    if solution_csp_1 is None:
        print("No solution found!")
    else:
        print("Done!")
        print()
        print('Timetable:')
        timetable_list = []
        for course, prof_id in solution_csp_1.items():
            timetable_list.append(f'{professors[prof_id]["name"]:24} {course} ')
        timetable_list.sort()
        for x in timetable_list:
            print(x)

    # format outputs

    # return schedule

    return "OK"


if __name__ == '__main__':
    generate_schedule(None, None, None)
