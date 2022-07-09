import json
import os
import datetime
import time
from pprint import pprint

from .constraints import professor_teaching_load, course_timeslot_conflicts
from .csp import CSP
from .datamodels import transform_input, timeslot_determination, transform_output


# Initial plug & play algorithm
def generate_schedule(professors, schedule, jsonDebug=False):
    if jsonDebug:
        # Temp load json files as input:
        if professors is None:
            prof_file = open(os.path.join(os.path.dirname(__file__), 'temp_json_input/professor_object.json'))
            professors = json.load(prof_file)
            prof_file.close()

        if schedule is None:
            schedule_file = open(os.path.join(os.path.dirname(__file__), 'temp_json_input/schedule_object.json'))
            schedule = json.load(schedule_file)
            schedule_file.close()

    # Convert timeslot lists to tuples as per the specification if not already tuples
    for professor in professors:
        for semester, days in professor["preferredTimes"].items():
            for day, timeslots in days.items():
                if timeslots[0] is not None:
                    tuple_list = [tuple(timeslot) for timeslot in timeslots]
                else:
                    tuple_list = None
                professor["preferredTimes"][semester][day] = tuple_list

    courses, professors = transform_input(schedule, professors)

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

    # run csp 1
    solution_csp_1 = csp_1.backtracking_search(config=config)
    if solution_csp_1 is None:
        return None

    # update the "courses" data structure with the professors assigned
    for semester, all_courses in courses.items():
        for course, values in all_courses.items():
            if course in solution_csp_1.keys():
                values["professor"] = solution_csp_1[course]

    # csp 2
    course_variables = []
    course_variables.extend(list(courses["fall"].keys()))
    course_variables.extend(list(courses["spring"].keys()))
    course_variables.extend(list(courses["summer"].keys()))

    # Create data structure of all possible timeslot configurations
    timeslot_configs = timeslot_determination()

    # Set the domains of each variable.
    timeslot_ids = timeslot_configs.keys()
    domains_csp_2 = {}
    semesters = courses.keys()
    for semester in semesters:
        for course in courses[semester]:
            timeslot_list = courses[semester][course]["timeSlots"]
            if (timeslot_list != []):

                # Convert timeslots from their format in the input,
                # to the corresponding format as it would appear in timeslot_configs.
                # timeslot_configs uses datetimes, the input uses strings.
                static_course_timeslots = []
                for timeslot_dict in timeslot_list:
                    # Convert the dictionary to a list of form ["DAY", datetime(start), datetime(end)]
                    start_time_string = timeslot_dict["timeRange"][0].split(':')
                    end_time_string = timeslot_dict["timeRange"][1].split(':')
                    start_datetime = datetime.datetime(100, 1, 1, int(start_time_string[0]), int(start_time_string[1]))
                    end_datetime = datetime.datetime(100, 1, 1, int(end_time_string[0]), int(end_time_string[1]))
                    timeslot = [
                        timeslot_dict["dayOfWeek"],
                        start_datetime,
                        end_datetime
                    ]
                    static_course_timeslots.append(timeslot)
                for key, timeslot in timeslot_configs.items():
                    if timeslot == static_course_timeslots:
                        domains_csp_2[course] = [key]
            else:
                domains_csp_2[course] = timeslot_ids

    domains_csp_2 = {course: timeslot_ids for course in course_variables}
    csp_2 = CSP(course_variables, domains_csp_2)

    # Add constraints: courses in the same academic year must not overlap.
    csp_2 = add_year_timeslot_constraint(csp_2, courses, timeslot_configs, "fall")
    csp_2 = add_year_timeslot_constraint(csp_2, courses, timeslot_configs, "spring")
    csp_2 = add_year_timeslot_constraint(csp_2, courses, timeslot_configs, "summer")

    # Add constraints: courses having the same professor must not overlap.
    all_profs = [k for k in professors.keys()]
    for prof_id in all_profs:
        for semester in ["fall", "spring", "summer"]:
            professor_teaching_courses = [course for course in courses[semester].keys() if
                                          courses[semester][course]["professor"] == prof_id]
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
    solution_csp_2 = csp_2.backtracking_search(config=config_csp_2)
    if solution_csp_2 is None:
        return None

    # update the "courses" data structure with the timeslots assigned
    for semester, all_courses in courses.items():
        for course, values in all_courses.items():
            if course in solution_csp_2.keys():
                values["timeSlots"] = timeslot_configs[solution_csp_2[course]]

    # format outputs and return generated schedule.
    schedule = transform_output(courses, schedule, professors)
    return schedule


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
    result = generate_schedule(None, None, True)
    # pprint(result)
