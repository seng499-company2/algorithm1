# This file contains a set of example data models to be used within the algorithm.
# This file will eventually convert the input data into the structures below.

# A dictionary of courses where the course codes are the keys and the values are the attributes of each course
courses = {
    "course code1": {
        "pengRequired": "boolean",
        "yearRequired": "int",
        "semester": "string",
        "professor": "professor object",
        "timeSlots": "list of timeSlot objects",
        "academicYear": "int"
    },
    "course code2": {
        "pengRequired": "boolean",
        "yearRequired": "int",
        "semester": "string",
        "professor": "professor object",
        "timeSlots": "list of timeSlot objects",
        "academicYear": "int"
    },
}

# A dictionary of professors where the professor ids are the keys and the values are the attributes of each professor
professors = {
    "id": {
        "name": "string",
        "isPeng": "boolean",
        "facultyType": "string",
        "qualifiedCoursePreferences": "list of coursePreference objects",
        "teachingObligations": "int",
        "preferredTimes": "dictionary of DayTimes objects",
        "preferredCoursesPerSemester": "dictionary of fall, spring, and summer ints",
        "preferredNonTeachingSemester": "string",
        "preferredCourseDaySpreads": "a course day spread object"
    },
}
# TWF (Tues, Wed, Fri) - 50 mins
# MR (Mon, Thurs) - 80 mins
# Any day - 180 mins
# TODO: Create the timeslot dictionary
timeslots = {
}

# timeslots = {
#     days = TWF
# }
#
# timeslot_configuration = {
#     id = 1
#     timeslots = [timeslot1, timeslot2, . . . ]
# }
#
# timeslot = {
#     day = "Mon"
#     start = 830
#     end = 920
# }

# time_conflicts = {id : [ids of conflicting configurations]}
