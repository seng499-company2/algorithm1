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
        "preferredTimes": "dictionary of DayTimes objects",
        "preferredCoursesPerSemester": "dictionary of fall, spring, and summer ints",
        "preferredNonTeachingSemester": "string",
        "preferredCourseDaySpreads": "a course day spread object"
    },
}

# Basic example of the time slot configuration.
# Below is a possible solution change if the time slot dictionary is too slow
# Conflict determination: IF list is same length, only need to compare 1 value
# First check if the day overlaps, then check if time overlaps
# MR and TWF will never need to be compared
timeslots = {
    1: [["TUESDAY", "830", "920"], ["WEDNESDAY", "830", "920"], ["FRIDAY", "830", "920"]],
    2: [["TUESDAY", "900", "950"], ["WEDNESDAY", "900", "950"], ["FRIDAY", "900", "950"]],
    3: [["MONDAY", "900", "1020"], ["THURSDAY", "900", "1020"]],
    4: [["TUESDAY", "900", "1150"]]
}


# conflicts = {
#     1: ABC,
#     2: BC
# }
# set_1.isdisjoint(set_2)
# domain = [1, 2, 3, 4, 5, . . . . . ]

# time_conflicts = {(id1, id2) : bool does_conflict}
