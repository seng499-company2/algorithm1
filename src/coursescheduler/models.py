import re
from schema import Schema, Or, And

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

CourseSection = Schema({
    "professor": Or(None, ProfessorSlim),
    "capacity": Or(None, int),
    "timeSlots": And([TimeSlot], lambda x: len(x) in [0, 1, 2, 3])  # And(list, validate_time_slots),
})

CourseOffering = Schema({
    "course": Course,
    "sections": And([CourseSection], lambda x: len(x) in [0, 1, 2]),  # And(list, validate_course_sections),
})

Schedule = Schema({
    "fall": [CourseOffering],
    "spring": [CourseOffering],
    "summer": [CourseOffering],
})


def validate_schedule(schedule, print_output=True):
    Schedule.validate(schedule)
    if print_output:
        print("Schedule adheres to specification")
    return True


def validate_professor(professor, print_output=True):
    Professor.validate(professor)
    if print_output:
        print("Professor adheres to specification")
    return True


def validate_professors(professors, print_output=True):
    for professor in professors:
        validate_professor(professor, print_output=False)
    if print_output:
        print("All professors adhere to specification")
    return True
