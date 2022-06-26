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


# Note: data does not reflect the real world and is for Testing Constraints Only
temp_courses = {
    "csc110": {
        "pengRequired": False,
        "professor": ""
    },
    "csc111": {
        "pengRequired": False,
        "professor": ""
    },
    "seng265": {
        "pengRequired": False,
        "professor": ""
    },
    "csc225": {
        "pengRequired": False,
        "professor": ""
    },
    "csc226": {
        "pengRequired": False,
        "professor": ""
    },
    "ece260": {
        "pengRequired": True,
        "professor": ""
    },
    "ece310": {
        "pengRequired": True,
        "professor": ""
    },
    "seng475": {
        "pengRequired": True,
        "professor": ""
    }
}

# Note: data does not reflect the real world and is for Testing Constraints Only
temp_profs = {
    "Bird": {
        "Name": "Bird",
        "isPeng": False,
        "qualifiedCoursePreferences": ["csc110", "csc111", "csc225", "csc226"],
        "teachingObligations": 2
    },
    "Zastre": {
        "Name": "Zastre",
        "isPeng": False,
        "qualifiedCoursePreferences": ["csc110", "csc111", "seng265"],
        "teachingObligations": 1
    },
    "Tzanatakis": {
        "Name": "Tzanatakis",
        "isPeng": False,
        "qualifiedCoursePreferences": ["csc225", "csc226"],
        "teachingObligations": 3
    },
    "Adams": {
        "Name": "Adams",
        "isPeng": True,
        "qualifiedCoursePreferences": ["ece260", "seng475"],
        "teachingObligations": 2
    },
    "Gebali": {
        "Name": "Gebali",
        "isPeng": True,
        "qualifiedCoursePreferences": ["ece260", "ece310"],
        "teachingObligations": 1
    }
}
