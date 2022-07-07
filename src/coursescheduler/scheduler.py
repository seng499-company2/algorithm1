import json
import time
from pprint import pprint

from constraints import professor_teaching_load, course_timeslot_conflicts
from csp import CSP
from datamodels import tranform_input, timeslot_determination


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
                qualified_peng_profs = {k: v for (k, v) in peng_profs.items() if
                                        v["qualifiedCoursePreferences"][original_course_id] != 0}
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
    print(f"Time taken is: {end - start}")
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

    # update the "courses" data structure with the professors assigned
    all_courses_input = {
        "fall": {k: v for (k, v) in courses["fall"].items()},
        "spring": {k: v for (k, v) in courses["spring"].items()},
        "summer": {k: v for (k, v) in courses["summer"].items()}
    }
    for semester, all_courses in all_courses_input.items():
        for course, values in all_courses.items():
            if course in solution_csp_1.keys():
                values["professor"] = solution_csp_1[course]

    # csp 2
    course_variables = []
    course_variables.extend(list(all_courses_input["fall"].keys()))
    course_variables.extend(list(all_courses_input["spring"].keys()))
    course_variables.extend(list(all_courses_input["summer"].keys()))

    # Create data structure of all possible timeslot configurations
    timeslot_configs = timeslot_determination()

    timeslot_ids = timeslot_configs.keys()
    domains_csp_2 = {course: timeslot_ids for course in course_variables}
    csp_2 = CSP(course_variables, domains_csp_2)

    csp_2 = add_year_timeslot_constraint(csp_2, all_courses_input, timeslot_configs, "fall")
    csp_2 = add_year_timeslot_constraint(csp_2, all_courses_input, timeslot_configs, "spring")
    csp_2 = add_year_timeslot_constraint(csp_2, all_courses_input, timeslot_configs, "summer")

    # For every professor, obtain the list of courses to which they are assigned.
    all_profs = [k for k in professors.keys()]

    # For each prof id
    for prof_id in all_profs:
        # Get list of courses the professor is teaching
        for semester in ["fall", "spring", "summer"]:
            professor_teaching_courses = [course for course in all_courses_input[semester].keys() if
                                          all_courses_input[semester][course]["professor"] == prof_id]
            if professor_teaching_courses:
                # For each list:
                csp_2.add_constraint(course_timeslot_conflicts(professor_teaching_courses, timeslot_configs))

    # set search config values
    config_csp_2 = {
        "mrv": True,
        "degree": False,
        "forward_checking": False,
        "max_steps": 50000
    }

    # run search
    start = time.time()
    solution_csp_2 = csp_2.backtracking_search(config=config_csp_2)
    end = time.time()
    print(f"Time taken is: {end - start}")
    if solution_csp_2 is None:
        print("No solution found!")
    else:
        print("Done!")
        print()
        print('Timetable:')
        timetable_list = []

        pprint(professors)

        for course, timeslot_id in solution_csp_2.items():
            #print(course)
            semester = course.split("_")[1]
            timeslots = timeslot_configs[timeslot_id]
            timeslot_out = []
            for timeslot in timeslots:
                day = timeslot[0]
                start = str(timeslot[1].time())
                end = str(timeslot[2].time())
                timeslot_out.append((day, start, end))

            pprint(all_courses_input[semester][course])


            try:
                # Sort by name
                # timetable_list.append(f'{professors[all_courses_input[semester][course]["professor"]]["name"]:<24} {course:<24}  {timeslot_out} ')
                # sort by semester
                timetable_list.append(f'{course.split("_")[1]:<8} {course.split("_")[0]:<8}  {professors[all_courses_input[semester][course]["professor"]]["name"]:<24} {timeslot_out} ')

            except KeyError:
                timetable_list.append(f'{course.split("_")[1]:<8} {course.split("_")[0]:<8}  {all_courses_input[semester][course]["professor"]:<24} {timeslot_out} ')

                timetable_list.append(f'{course:<24} {all_courses_input[semester][course]["professor"]:<24} {timeslot_out} ')
            #timetable_list.append(f'{course:<24} {all_courses_input[semester][course]["professor"]} {timeslot_out} ')
        timetable_list.sort()
        for x in timetable_list:
            print(x)

    # For each static course, reduce the domain to contain a single value,
    # which is the timeslot configuration specified in the input.
    # . . .

    # format outputs

    # return schedule

    return "OK"


def add_year_timeslot_constraint(csp_2, all_courses_input, timeslot_configs, semester):
    # Group courses by year.
    first_year_courses = [course for course in all_courses_input[semester].keys() if
                          all_courses_input[semester][course]["yearRequired"] == 1]
    second_year_courses = [course for course in all_courses_input[semester].keys() if
                           all_courses_input[semester][course]["yearRequired"] == 2]
    third_year_courses = [course for course in all_courses_input[semester].keys() if
                          all_courses_input[semester][course]["yearRequired"] == 3]
    fourth_year_courses = [course for course in all_courses_input[semester].keys() if
                           all_courses_input[semester][course]["yearRequired"] == 4]

    # Add timeslot overlap constraints.
    csp_2.add_constraint(course_timeslot_conflicts(first_year_courses, timeslot_configs))
    csp_2.add_constraint(course_timeslot_conflicts(second_year_courses, timeslot_configs))
    csp_2.add_constraint(course_timeslot_conflicts(third_year_courses, timeslot_configs))
    csp_2.add_constraint(course_timeslot_conflicts(fourth_year_courses, timeslot_configs))

    return csp_2


if __name__ == '__main__':
    generate_schedule(None, None, None)
