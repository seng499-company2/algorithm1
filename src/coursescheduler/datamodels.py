import datetime

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

timeslots_codes = {
    "TWF": {
        "id": 1,
        "days": ["Tuesday", "Wednesday", "Friday"],
        "classLength": 50
    },
    "MR": {
        "id": 2,
        "days": ["Monday", "Thursday"],
        "classLength": 80
    },

    "Any": {
        "id": 3,
        "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "classLength": 170
    }
}

# Conflict determination: IF list is same length, only need to compare 1 value
# First check if the day overlaps, then check if time overlaps
# MR and TWF will never need to be compared
timeslots = {
    1: [["TUESDAY", "830", "920"], ["WEDNESDAY", "830", "920"], ["FRIDAY", "830", "920"]],
    2: [["TUESDAY", "900", "950"], ["WEDNESDAY", "900", "950"], ["FRIDAY", "900", "950"]],
    3: [["MONDAY", "900", "1020"], ["THURSDAY", "900", "1020"]],
    4: [["TUESDAY", "900", "1150"]]
}

timeslots = [
    [["TUESDAY", "830", "920"], ["WEDNESDAY", "830", "920"], ["FRIDAY", "830", "920"]],
    [["TUESDAY", "900", "950"], ["WEDNESDAY", "900", "950"], ["FRIDAY", "900", "950"]],
    [["MONDAY", "900", "1020"], ["THURSDAY", "900", "1020"]],
    [["TUESDAY", "900", "1150"]]
]
# conflicts = {
#     1: ABC,
#     2: BC
# }
# set_1.isdisjoint(set_2)
# domain = [1, 2, 3, 4, 5, . . . . . ]

# time_conflicts = {(id1, id2) : bool does_conflict}

# Domain of some variable in CSP 2
timeslots = [
    [()]
]

def timeslot_determination():

    scheduled_start_time = datetime.datetime(100, 1, 1, 8, 30)
    count = 0
    timeslots_dict= {}

    twf_dict = scheduled_times(scheduled_start_time, 50)
    # print(len(twf_dict))
    for start_time,scheduled_end_time in twf_dict.items():
        # print("{} to {}".format(start_time, scheduled_end_time))
        timeslots_dict[count] = [["TUESDAY", start_time, scheduled_end_time],
                                 ["WEDNESDAY", start_time, scheduled_end_time],
                                ["FRIDAY", start_time, scheduled_end_time]]
        count +=1

    # print("THE Monday Thursday Offering")
    scheduled_start_time = datetime.datetime(100, 1, 1, 8, 30)
    mr_dict = scheduled_times(scheduled_start_time, 80)
    # print(len(mr_dict))
    for start_time, scheduled_end_time in mr_dict.items():
        # print("{} to {}".format(start_time.time(), scheduled_end_time.time()))
        timeslots_dict[count] = [["MONDAY", start_time, scheduled_end_time],
                                 ["THURSDAY", start_time, scheduled_end_time]]
        count += 1

    scheduled_start_time = datetime.datetime(100, 1, 1, 13, 00)
    any_dict = scheduled_times(scheduled_start_time, 170)
    for start_time, scheduled_end_time in any_dict.items():
        # print("{} to {}".format(start_time.time(), scheduled_end_time.time()))
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

    print(timeslots_dict)


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

def main():
    timeslot_determination()
    # scheduled_start_time = datetime.datetime(100, 1, 1, 8, 30)
    # timeslot_set = scheduled_times(scheduled_start_time, 50)

    # test = course_timeslot_conflicts(timeslot_set)
    # test.satisfied()



if __name__ == "__main__":
    main()