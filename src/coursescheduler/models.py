import re
from schema import Schema, Or, And, Optional

twentyFourHourTimeRegex = r'^((0?|1)[0-9]|2[0-3]):[0-5][0-9]$'


def validate_time_ranges(time_ranges):
    assert len(time_ranges) == 2
    assert re.match(twentyFourHourTimeRegex, time_ranges[0])
    assert re.match(twentyFourHourTimeRegex, time_ranges[1])
    assert int(time_ranges[0].replace(":", "")) < int(time_ranges[1].replace(":", ""))
    return True


CoursePreference = Schema({
    "courseCode": str,
    "enthusiasmScore": int,
})

TimeRange = Schema(And(Or(list, tuple), validate_time_ranges))

DayTimes = Schema({
    "monday": [TimeRange],
    "tuesday": [TimeRange],
    "wednesday": [TimeRange],
    "thursday": [TimeRange],
    "friday": [TimeRange],
})

Professor = Schema({
    "id": str,
    "name": str,
    "isPeng": bool,
    "facultyType": Or("RESEARCH", "TEACHING"),
    "coursePreferences": [CoursePreference],
    "teachingObligations": int,
    "preferredTimes": {
        "fall": Or(None, DayTimes),
        "spring": Or(None, DayTimes),
        "summer": Or(None, DayTimes),
    },
    "preferredCoursesPerSemester": {
        "fall": And(int, lambda n: n >= 0),
        "spring": And(int, lambda n: n >= 0),
        "summer": And(int, lambda n: n >= 0),
    },
    "preferredNonTeachingSemester": Or("FALL", "SPRING", "SUMMER", None),
    "preferredCourseDaySpreads": ["TWF", "MTh", "M", "T", "W", "Th", "F"],
})

Course = Schema({
    "code": str,
    "title": str,
    "pengRequired": {
        "fall": bool,
        "spring": bool,
        "summer": bool,
    },
    "yearRequired": Or(1, 2, 3, 4),
})

TimeSlot = Schema({
    "dayOfWeek": Or("MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"),
    "timeRange": TimeRange,
})

ProfessorSlim = Schema({
    "id": str,
    "name": str,
})

# len(timeSlots): 0 if unscheduled, 1 if scheduled on M|T|W|Th|F, 2 if scheduled on MTh, or 3 if scheduled on TWF
CourseSection = Schema({
    "professor": Or(None, ProfessorSlim),
    Optional("maxCapacity"): Or(None, int),
    "capacity": Or(None, int),
    "timeSlots": And([TimeSlot], lambda x: len(x) in [0, 1, 2, 3]),
})

CourseOffering = Schema({
    "course": Course,
    "sections": And([CourseSection]),
})

Schedule = Schema({
    "fall": [CourseOffering],
    "spring": [CourseOffering],
    "summer": [CourseOffering],
})


def validate_schedule_structure(schedule, print_output=True):
    Schedule.validate(schedule)
    if print_output:
        print("Schedule adheres to specification")
    return True


def validate_professor_structure(professor, print_output=True):
    Professor.validate(professor)
    if print_output:
        print("Professor adheres to specification")
    return True


def validate_professors_structure(professors, print_output=True):
    for professor in professors:
        validate_professor_structure(professor, print_output=False)
    if print_output:
        print("All professors adhere to specification")
    return True
