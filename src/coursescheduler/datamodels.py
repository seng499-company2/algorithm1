import datetime


# This function transforms the input data into data which is optimal for use in the algorithm.
def transform_input(schedule_input, professors_input):
    courses = {
        "fall": {},
        "spring": {},
        "summer": {}
    }
    for semester, offering_list in schedule_input.items():
        for offering in offering_list:
            course = offering["course"]
            sections = offering["sections"]
            for index, section in enumerate(sections):
                if section["professor"] is None and len(section["timeSlots"]) <= 0:
                    courses[semester][course["code"] + "_" + semester] = {
                        # Appending number to handle multi-section courses
                        "pengRequired": course["pengRequired"][semester],
                        "yearRequired": course["yearRequired"],
                        "semester": semester,
                        "professor": section["professor"]["id"] if section["professor"] is not None else None,
                        "timeSlots": section["timeSlots"] if section["timeSlots"] is not None else [],
                        # "academicYear": course["academicYear"] # Unsure of redundancy with yearRequired
                    }
                else:
                    courses[semester][course["code"] + "_" + semester + "_" + str(index)] = {
                        # Appending number to handle multi-section courses
                        "pengRequired": course["pengRequired"][semester],
                        "yearRequired": course["yearRequired"],
                        "semester": semester,
                        "professor": section["professor"]["id"] if section["professor"] is not None else None,
                        "timeSlots": section["timeSlots"] if section["timeSlots"] is not None else [],
                        # "academicYear": course["academicYear"] # Unsure of redundancy with yearRequired
                    }

    professors = {}
    for professor in professors_input:
        sorted_course_prefs = sorted(professor["coursePreferences"], key=lambda d: d['enthusiasmScore'], reverse=True)
        professors[professor["id"]] = {
            "name": professor["name"],
            "isPeng": professor["isPeng"],
            "facultyType": professor["facultyType"],
            "qualifiedCoursePreferences": sorted_course_prefs,
            "teachingObligations": professor["teachingObligations"],
            "preferredTimes": professor["preferredTimes"],
            "preferredCoursesPerSemester": professor["preferredCoursesPerSemester"],
            "preferredNonTeachingSemester": professor["preferredNonTeachingSemester"],
            "preferredCourseDaySpreads": professor["preferredCourseDaySpreads"]
        }
    return courses, professors


# Fill in the schedule object with the output data from the algorithm
def transform_output(alg_output, schedule_input, professors):
    # Loop through the input object and fill in the missing data
    for semester, offering_list in schedule_input.items():
        for offering in offering_list:
            course = offering["course"]
            sections = offering["sections"]
            for index, section in enumerate(sections):
                if section["professor"] is None and len(section["timeSlots"]) <= 0:
                    output_section_data = alg_output[semester][course["code"] + "_" + semester]
                else:
                    output_section_data = alg_output[semester][course["code"] + "_" + semester + "_" + str(index)]

                # If the input professor is None then we create an empty object to be filled in
                if section["professor"] is None:
                    section["professor"] = {
                        "id": None,
                        "name": None
                    }

                # If the professor isn't assigned in the input then we fetch the output assignment and fill it in
                if section["professor"]["id"] is None:
                    section["professor"]["id"] = output_section_data["professor"]

                # If the professor isn't assigned in the input then we fetch the output assignment and fill it in
                if section["professor"]["name"] is None:
                    section["professor"]["name"] = professors[output_section_data["professor"]]["name"]

                # If the timeslot isn't assigned in the input then we fetch the output assignment and fill it in
                if len(section["timeSlots"]) == 0:
                    alg_output_timeslots = output_section_data["timeSlots"]

                    output_timeslots = []
                    for timeslot in alg_output_timeslots:
                        output_timeslot = {
                            "dayOfWeek": timeslot[0].upper(),
                            "timeRange": (timeslot[1].strftime("%H:%M"), timeslot[2].strftime("%H:%M"))
                        }
                        output_timeslots.append(output_timeslot)

                    section["timeSlots"] = output_timeslots

    # Return the filled in schedule object
    return schedule_input


# This function returns a dictionary containing a time slot ID and time slot configuration
def timeslot_determination():
    count = 0
    timeslots_dict = {}
    timeslots_dict_twf = {}
    timeslots_dict_mr = {}

    scheduled_start_time = datetime.datetime(100, 1, 1, 8, 30)
    twf_dict = scheduled_times(scheduled_start_time, 50)
    for start_time, scheduled_end_time in twf_dict.items():  # 830-320 330-920
        timeslots_dict_twf[count] = [["TUESDAY", start_time, scheduled_end_time],
                                     ["WEDNESDAY", start_time, scheduled_end_time],
                                     ["FRIDAY", start_time, scheduled_end_time]]
        count += 1

    scheduled_start_time = datetime.datetime(100, 1, 1, 8, 30)
    mr_dict = scheduled_times(scheduled_start_time, 80)

    for start_time, scheduled_end_time in mr_dict.items():
        timeslots_dict_mr[count] = [["MONDAY", start_time, scheduled_end_time],
                                    ["THURSDAY", start_time, scheduled_end_time]]
        count += 1

    # In timeslots_dict, alternate between TWF and MR configurations.
    # Then the search will naturally distribute classes between all days of the week,
    # since timeslots are considered in the order they appear in the dictionary.
    for i in range(len(timeslots_dict_twf) - 1):
        timeslots_dict[i] = timeslots_dict_twf[i]
        timeslots_dict[i + len(timeslots_dict_twf)] = timeslots_dict_mr[i + len(timeslots_dict_twf)]
    timeslots_dict[len(timeslots_dict_twf) - 1] = timeslots_dict_twf[len(timeslots_dict_twf) - 1]

    scheduled_start_time = datetime.datetime(100, 1, 1, 13, 00)
    any_dict = scheduled_times(scheduled_start_time, 170)
    for start_time, scheduled_end_time in any_dict.items():
        timeslots_dict[count] = [["MONDAY", start_time, scheduled_end_time]]
        count += 1
        timeslots_dict[count] = [["TUESDAY", start_time, scheduled_end_time]]
        count += 1
        timeslots_dict[count] = [["WEDNESDAY", start_time, scheduled_end_time]]
        count += 1
        timeslots_dict[count] = [["THURSDAY", start_time, scheduled_end_time]]
        count += 1
        timeslots_dict[count] = [["FRIDAY", start_time, scheduled_end_time]]
        count += 1

    return timeslots_dict


# Helper function for timeslot_determination
def scheduled_times(start_time, class_length):
    end_time = start_time + datetime.timedelta(minutes=class_length)
    timeslot_dict = {start_time: end_time}
    timeslot_array = {(start_time, end_time)}

    while end_time.time() < datetime.time(21, 50):
        if start_time.time() == datetime.time(19, 00) and class_length == 170:
            break
        start_time += datetime.timedelta(minutes=30)
        end_time = start_time + datetime.timedelta(minutes=class_length)

        timeslot_dict[start_time] = end_time
        timeslot_array.add((start_time, end_time))

    return timeslot_dict
