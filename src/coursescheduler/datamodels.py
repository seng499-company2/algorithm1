# This function transforms the input data into data which is optimal for use in the algorithm.
def tranform_input(schedule_input, professors_input):
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
                courses[semester][course["code"] + "_" + str(index)] = {
                    # Appending number to handle multi-section courses
                    "pengRequired": course["pengRequired"][semester],
                    "yearRequired": course["yearRequired"],
                    "semester": semester,
                    "professor": section["professor"]["id"] if section["professor"] is not None else None,
                    "timeSlots": section["timeslots"] if section["timeslots"] is not None else [],
                    # "academicYear": course["academicYear"] # Unsure of redundancy with yearRequired
                }

    professors = {}
    for professor in professors_input:
        professors[professor["id"]] = {
            "name": professor["name"],
            "isPeng": professor["isPeng"],
            "facultyType": professor["facultyType"],
            "qualifiedCoursePreferences": professor["coursePreferences"],
            "teachingObligations": professor["teachingObligations"],
            "preferredTimes": professor["preferredTimes"],
            "preferredCoursesPerSemester": professor["preferredCoursesPerSemester"],
            "preferredNonTeachingSemester": professor["preferredNonTeachingSemester"],
            "preferredCourseDaySpreads": professor["preferredCourseDaySpreads"]
        }
    return courses, professors
