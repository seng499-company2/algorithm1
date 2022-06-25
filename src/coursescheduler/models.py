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
        "coursePreferences": "list of coursePreference objects",
        "teachingObligations": "int",
        "qualifiedCourses": "list",
        "preferredTimes": "dictionary of DayTimes objects",
        "preferredCoursesPerSemester": "dictionary of fall, spring, and summer ints",
        "preferredNonTeachingSemester": "string",
        "preferredCourseDaySpreads": "a course day spread object"
    },
}

timeslots = {
#     TODO
}

# Note: data does not reflect the real world and is for Testing Constraints Only
temp_courses = {
    "csc110": {
        "pengRequired": False,
        "professor": "Bird",
        "courseDay": ["monday", "tuesday", "wednesday"]
    },
    "csc111": {
        "pengRequired": False,
        "professor": "Bird"
    },
    "seng265": {
        "pengRequired": False,
        "professor": "Zastre"
    },
    "csc225": {
        "pengRequired": False,
        "professor": "Zastre"
    },
    "csc226": {
        "pengRequired": False,
        "professor": "Zastre"
    },
    "ece260": {
        "pengRequired": True,
        "professor": "Zastre"
    },
    "ece310": {
        "pengRequired": True,
        "professor": "Zastre"
    },
    "seng475": {
        "pengRequired": True,
        "professor": "Zastre"
    }
}

# Note: data does not reflect the real world and is for Testing Constraints Only
temp_profs = {
    "Bird": {
        "Name": "Bird",
        "isPeng": False,
        "qualifiedCourses": ["csc110", "csc111", "csc225", "csc226"],
        "teachingObligations": 2,
        "assigned_Courses": 3
    },
    "Zastre": {
        "Name": "Zastre",
        "isPeng": False,
        "qualifiedCourses": ["csc110", "csc111", "seng265"],
        "teachingObligations": 1
    },
    "Tzanatakis": {
        "Name": "Tzanatakis",
        "isPeng": False,
        "qualifiedCourses": ["csc225", "csc226"],
        "teachingObligations": 3
    },
    "Adams": {
        "Name": "Adams",
        "isPeng": True,
        "qualifiedCourses": ["ece260", "seng475"],
        "teachingObligations": 2
    },
    "Gebali": {
        "Name": "Gebali",
        "isPeng": True,
        "qualifiedCourses": ["ece260", "ece310"],
        "teachingObligations": 1
    }
}
