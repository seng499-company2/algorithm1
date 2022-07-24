import json
import os
import datetime
import time

from threading import Thread, Event
from .constraints import professor_teaching_load, course_timeslot_conflicts, course_preferences_constraint, \
    time_slot_constraint, research_professor_semester_off, professor_on_leave
from .csp import CSP
from .datamodels import transform_input, timeslot_determination, transform_output

# Set max runtime to five minutes
max_time_seconds = 5 * 60
stop_event = Event()


def log_message(message):
    print("[SCHEDULER] " + message)


def generate_schedule(professors, schedule, jsonDebug=False):
    result_object = {
        "schedule": None,
        "message": None
    }
    main_alg_thread = Thread(target=generate_schedule_timer, args=(professors, schedule, result_object, jsonDebug))
    main_alg_thread.start()
    main_alg_thread.join(timeout=max_time_seconds)
    if main_alg_thread.is_alive():
        stop_event.set()
        main_alg_thread.join()

    if result_object["schedule"] is None and result_object["message"] is None:
        result_object["message"] = "No schedule could be generated."
    return result_object["schedule"], result_object["message"]


# Initial plug & play algorithm
# TODO Add checks for stop_event to prevent the algorithm from running too long
def generate_schedule_timer(professors, schedule, result_object, jsonDebug=False):
    if jsonDebug:
        # Temp load json files as input:
        if professors is None:
            prof_file = open(os.path.join(os.path.dirname(__file__), 'temp_json_input/professor_object.json'))
            professors = json.load(prof_file)
            prof_file.close()

            # Convert timeslot lists to tuples as per the specification if not already tuples
            for professor in professors:
                # Error case: converting timeslots lists to tuples timed out.
                if stop_event.isSet():
                    result_object["schedule"] = None
                    result_object["message"] = "Error: Timeout due to large input size."
                    return
                for semester, days in professor["preferredTimes"].items():
                    if days is not None:
                        for day, timeslots in days.items():
                            if len(timeslots) > 0:
                                tuple_list = [tuple(timeslot) for timeslot in timeslots]
                            else:
                                tuple_list = None
                            professor["preferredTimes"][semester][day] = tuple_list

        if schedule is None:
            schedule_file = open(os.path.join(os.path.dirname(__file__), 'temp_json_input/schedule_object.json'))
            schedule = json.load(schedule_file)
            schedule_file.close()

    # TODO validate schedule object here

    # TODO validate professor object here

    start_time = time.time()

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
            # Error case: adding the domains to each variable timed out.
            if stop_event.isSet():
                result_object["schedule"] = None
                result_object["message"] = "Error: Timeout due to large professor or course offering input size."
                return
            original_course_id = course.split("_")[0]
            if course_data["pengRequired"]:
                qualified_peng_profs = [k for (k, v) in peng_profs.items()
                                        for course_preferences in v["qualifiedCoursePreferences"]
                                        if course_preferences["courseCode"] == original_course_id and
                                        course_preferences["enthusiasmScore"] != 0]
                if len(qualified_peng_profs) > 0:
                    # Sort values (professors) in descending order of enthusiasm score for the variable (course).
                    def get_enthusiasm_score(prof):
                        enthusiasm_score_ = 0
                        for enthusiasm_dict in professors[prof]["qualifiedCoursePreferences"]:
                            if enthusiasm_dict["courseCode"] == original_course_id:
                                enthusiasm_score_ = enthusiasm_dict["enthusiasmScore"]
                        return enthusiasm_score_

                    qualified_peng_profs.sort(reverse=True, key=get_enthusiasm_score)

                    # Remove the researching professors on their research semester
                    for qualified_prof in qualified_peng_profs:
                        if professors[qualified_prof]["facultyType"] == "RESEARCH":
                            if professors[qualified_prof]["preferredNonTeachingSemester"] and semester == \
                                    professors[qualified_prof]["preferredNonTeachingSemester"].lower():
                                qualified_peng_profs.remove(qualified_prof)

                    # Assign the sorted professors as the domain for the course.
                    domains_csp_1[course] = qualified_peng_profs
            else:
                qualified_profs = [k for (k, v) in professors.items()
                                   for course_preferences in v["qualifiedCoursePreferences"]
                                   if course_preferences["courseCode"] == original_course_id and
                                   course_preferences["enthusiasmScore"] != 0]

                if len(qualified_profs) > 0:
                    # Sort values (professors) in descending order of enthusiasm score for the variable (course).
                    def get_enthusiasm_score(prof):
                        enthusiasm_score_ = 0
                        for enthusiasm_dict in professors[prof]["qualifiedCoursePreferences"]:
                            if enthusiasm_dict["courseCode"] == original_course_id:
                                enthusiasm_score_ = enthusiasm_dict["enthusiasmScore"]
                        return enthusiasm_score_

                    qualified_profs.sort(reverse=True, key=get_enthusiasm_score)

                    # Remove the researching professors on their research semester
                    for qualified_prof in qualified_profs:
                        if professors[qualified_prof]["facultyType"] == "RESEARCH":
                            if professors[qualified_prof]["preferredNonTeachingSemester"] and semester == \
                                    professors[qualified_prof]["preferredNonTeachingSemester"].lower():
                                qualified_profs.remove(qualified_prof)

                    # Assign the sorted professors as the domain for the course.
                    domains_csp_1[course] = qualified_profs

    # initialize csp solvers
    course_variables_non_static = []
    course_variables_non_static.extend(list(non_static_courses["fall"].keys()))
    course_variables_non_static.extend(list(non_static_courses["spring"].keys()))
    course_variables_non_static.extend(list(non_static_courses["summer"].keys()))

    # Error case: not enough qualified professors are available for all courses
    if len(domains_csp_1) < len(course_variables_non_static):
        number_of_unqualified = 0
        list_of_domainless = []
        for variable in course_variables_non_static:
            if variable not in domains_csp_1:
                number_of_unqualified += 1
                list_of_domainless.append(variable)
        result_object["schedule"] = None
        if number_of_unqualified <= 1:
            result_object["message"] = f"Error: No qualified professor for {list_of_domainless[0]}."
        else:
            result_object["message"] = f"Error: No qualified professor for {list_of_domainless[0]} and " \
                                       f"{number_of_unqualified - 1} more courses. "
        return

    try:
        csp_1 = CSP(course_variables_non_static, domains_csp_1)

        # add hard constraints
        csp_1.add_constraint(professor_teaching_load(course_variables_non_static, professors))
        csp_1.add_constraint(professor_on_leave(course_variables_non_static, professors))

        # add soft constraints
        csp_1.add_soft_constraint(course_preferences_constraint(course_variables_non_static, professors))

        # set search config values
        config = {
            "mrv": True,
            "degree": False,
            "forward_checking": False,
            "max_steps": 50000
        }

        # Error case: setting up CSP 1 timed out.
        if stop_event.isSet():
            result_object["schedule"] = None
            result_object["message"] = "Error: Timeout due to large professor or course offering input size."
            return

        # Set optimization config values
        config_opt = {
            "max_steps": 1000
        }

        # run csp 1
        start_time_csp_1 = time.time()
        solution_csp_1 = csp_1.backtracking_search(config=config, stop_event=stop_event, result_object=result_object)

        # Error case: CSP 1 did not find a solution in the given time limit.
        if solution_csp_1 is None and stop_event.isSet():
            return

        # Error case: CSP 1 did not find a solution.
        if solution_csp_1 is None:
            log_message("No solution found in CSP 1 (professors to courses)")
            result_object["schedule"] = None
            result_object["message"] = "Error: No possible schedule found for the given constraints while assigning " \
                                       "professors. "
            return

        solution_csp_1 = csp_1.optimize(solution_csp_1, config=config_opt, stop_event=stop_event, result_object=result_object)
        # Error case: CSP 1 did not find a solution in the given time limit.
        if solution_csp_1 is None and stop_event.isSet():
            return

        end_time_csp_1_opt = time.time()

    except Exception as e:
        log_message(str(e))
        # Error case: CSP 1 raised an exception.
        result_object["schedule"] = None
        result_object["message"] = "Error: No schedule found."
        return

    log_message("Successfully solved CSP 1 (assigned all professors to courses)")
    log_message("Runtime of CSP 1: " + str(end_time_csp_1_opt - start_time_csp_1) + " seconds")

    # update the "courses" data structure with the professors assigned
    for semester, all_courses in courses.items():
        for course, values in all_courses.items():
            if course in solution_csp_1.keys():
                values["professor"] = solution_csp_1[course]

    # Error case: CSP 1 timed out at some point.
    if stop_event.isSet():
        result_object["schedule"] = None
        result_object["message"] = "Error: Timeout during professor assignment (likely due to no feasible schedule " \
                                   "existing given the constraints. "
        return

    # csp 2
    course_variables = []
    course_variables.extend(list(courses["fall"].keys()))
    course_variables.extend(list(courses["spring"].keys()))
    course_variables.extend(list(courses["summer"].keys()))

    static_courses = [course for course in course_variables if course not in course_variables_non_static]

    # Create data structure of all possible timeslot configurations
    timeslot_configs = timeslot_determination()

    # Set the domains of each variable.
    timeslot_ids = timeslot_configs.keys()
    domains_csp_2 = {}
    semesters = courses.keys()
    for semester in semesters:
        for course in courses[semester]:
            # Error case: CSP 2 setting of domains timed out.
            if stop_event.isSet():
                result_object["schedule"] = None
                result_object["message"] = "Error: Timeout due to large timeslot or course offering input size."
                return

            timeslot_list = courses[semester][course]["timeSlots"]
            if timeslot_list:

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

    try:
        csp_2 = CSP(course_variables, domains_csp_2)

        static_courses_fall = [course for course in static_courses if "fall" in course]
        static_courses_spring = [course for course in static_courses if "spring" in course]
        static_courses_summer = [course for course in static_courses if "summer" in course]

        # Add constraints: courses in the same academic year must not overlap.
        csp_2 = add_year_timeslot_constraint(csp_2, courses, timeslot_configs, "fall", static_courses_fall)
        csp_2 = add_year_timeslot_constraint(csp_2, courses, timeslot_configs, "spring", static_courses_spring)
        csp_2 = add_year_timeslot_constraint(csp_2, courses, timeslot_configs, "summer", static_courses_summer)

        # Add constraints: courses having the same professor must not overlap.
        all_profs = [k for k in professors.keys()]
        for prof_id in all_profs:
            for semester in ["fall", "spring", "summer"]:
                professor_teaching_courses = [course for course in courses[semester].keys() if
                                              courses[semester][course]["professor"] == prof_id]
                if professor_teaching_courses:
                    # For each list:
                    csp_2.add_constraint(course_timeslot_conflicts(professor_teaching_courses, timeslot_configs, []))

        # Add soft constraints.
        csp_2.add_soft_constraint(
            time_slot_constraint(course_variables_non_static, professors, timeslot_configs, solution_csp_1))

        # set search config values
        config_csp_2 = {
            "mrv": True,
            "degree": False,
            "forward_checking": False,
            "max_steps": 50000
        }

        # Error case: setting up CSP 2 timed out.
        if stop_event.isSet():
            result_object["schedule"] = None
            result_object["message"] = "Error: Timeout due to large timeslot or course offering input size."
            return

        # Set optimization config values
        config_opt = {
            "max_steps": 500
        }

        # run search
        start_time_csp_2 = time.time()
        solution_csp_2 = csp_2.backtracking_search(config=config_csp_2, stop_event=stop_event,
                                                   result_object=result_object)

        # Error case: CSP 2 did not find a solution in the given time limit.
        if solution_csp_2 is None and stop_event.isSet():
            return

        # Error case: CSP 2 did not find a solution.
        if solution_csp_2 is None:
            log_message("No solution found in CSP 2 (timeslots to courses)")
            result_object["schedule"] = None
            result_object["message"] = "Error: No possible schedule found for the given constraints while assigning " \
                                       "timeslots. "
            return

        solution_csp_2 = csp_2.optimize(solution_csp_2, config=config_opt, stop_event=stop_event, result_object=result_object)
        # Error case: CSP 2 did not find a solution in the given time limit.
        if solution_csp_2 is None and stop_event.isSet():
            return

        end_time_csp_2_opt = time.time()

    except Exception as e:
        log_message(str(e))
        # Error case: CSP 2 raised an exception.
        result_object["schedule"] = None
        result_object["message"] = "Error: No schedule found."
        return

    log_message("Successfully solved CSP 2 (assigned all timeslots to courses)")
    log_message("Runtime of CSP 2: " + str(end_time_csp_2_opt - start_time_csp_2) + " seconds")

    # update the "courses" data structure with the timeslots assigned
    for semester, all_courses in courses.items():
        for course, values in all_courses.items():
            if course in solution_csp_2.keys():
                values["timeSlots"] = timeslot_configs[solution_csp_2[course]]

    # Error case: CSP 2 timed out at some point.
    if stop_event.isSet():
        result_object["schedule"] = None
        result_object["message"] = "Error: Timeout during timeslot assignment (likely due to no feasible schedule " \
                                   "existing given the constraints. "
        return

    # format outputs and return generated schedule.
    schedule = transform_output(courses, schedule, professors)
    end_time = time.time()
    log_message("Schedule generated successfully")
    log_message("Total runtime: " + str(end_time - start_time) + " seconds")
    result_object["schedule"] = schedule
    result_object["message"] = "Schedule generated successfully."
    return


def add_year_timeslot_constraint(csp_2, all_courses_input, timeslot_configs, semester, static_courses):
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
    csp_2.add_constraint(course_timeslot_conflicts(first_year_courses, timeslot_configs, static_courses))
    csp_2.add_constraint(course_timeslot_conflicts(second_year_courses, timeslot_configs, static_courses))
    csp_2.add_constraint(course_timeslot_conflicts(third_year_courses, timeslot_configs, static_courses))
    csp_2.add_constraint(course_timeslot_conflicts(fourth_year_courses, timeslot_configs, static_courses))

    return csp_2


if __name__ == '__main__':
    result, error = generate_schedule(None, None, True)
