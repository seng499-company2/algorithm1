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

test_assignment = {
    "CSC111": "2",
    "CSC115": "2",
    "SENG265": "1",
    "CSC225": "2",
    "ENGR110": "100",
    "ENGR130": "101"
}

test_time = {
    "CSC111": 2,
    "CSC115": 2,
    "SENG265": 2,
    "CSC225": 4,
    "ENGR110": "100",
    "ENGR130": "101"
}
test_courses = {
    "CSC111": {
        "pengRequired": True,
        "yearRequired": 1,
        "semester": "fall",
        "professor": "2",
        "timeSlots": []
    },
    "CSC115": {
        "pengRequired": True,
        "yearRequired": 1,
        "semester": "fall",
        "professor": "2",
        "timeSlots": []
    },
    "SENG265": {
        "pengRequired": True,
        "yearRequired": 2,
        "semester": "fall",
        "professor": "1",
        "timeSlots": []
    },
    "CSC225": {
        "pengRequired": False,
        "yearRequired": 2,
        "semester": "fall",
        "professor": "2",
        "timeSlots": [{
            "dayOfWeek": "TUESDAY",
            "timeRange": ["8:30", "9:20"]
        }, {
            "dayOfWeek": "WEDNESDAY",
            "timeRange": ["8:30", "9:20"]
        }, {
            "dayOfWeek": "FRIDAY",
            "timeRange": ["8:30", "9:20"]
        }]
    },
    "ENGR110": {
        "pengRequired": False,
        "yearRequired": 1,
        "semester": "fall",
        "professor": "100",
        "timeSlots": [{
            "dayOfWeek": "TUESDAY",
            "timeRange": ["8:30", "9:20"]
        }, {
            "dayOfWeek": "WEDNESDAY",
            "timeRange": ["8:30", "9:20"]
        }, {
            "dayOfWeek": "FRIDAY",
            "timeRange": ["8:30", "9:20"]
        }]
    },
    "ENGR130": {
        "pengRequired": False,
        "yearRequired": 1,
        "semester": "fall",
        "professor": "101",
        "timeSlots": [{
            "dayOfWeek": "MONDAY",
            "timeRange": ["8:30", "9:50"]
        }, {
            "dayOfWeek": "THURSDAY",
            "timeRange": ["8:30", "9:50"]
        }]
    }
}

test_professors = {
    "1": {
        "name": "Celina Berg",
        "isPeng": False,
        "facultyType": "TEACHING",
        "qualifiedCoursePreferences": [{
            "courseCode": "CSC111",
            "enthusiasmScore": 78
        }, {
            "courseCode": "CSC115",
            "enthusiasmScore": 20
        }, {
            "courseCode": "ECE255",
            "enthusiasmScore": 0
        }, {
            "courseCode": "CSC230",
            "enthusiasmScore": 20
        }, {
            "courseCode": "ECE260",
            "enthusiasmScore": 0
        }, {
            "courseCode": "SENG265",
            "enthusiasmScore": 0
        }, {
            "courseCode": "CSC225",
            "enthusiasmScore": 20
        }, {
            "courseCode": "ECE310",
            "enthusiasmScore": 0
        }, {
            "courseCode": "SENG275",
            "enthusiasmScore": 20
        }, {
            "courseCode": "SENG310",
            "enthusiasmScore": 78
        }, {
            "courseCode": "ECE458",
            "enthusiasmScore": 0
        }, {
            "courseCode": "CSC361",
            "enthusiasmScore": 0
        }, {
            "courseCode": "CSC226",
            "enthusiasmScore": 20
        }, {
            "courseCode": "ECE360",
            "enthusiasmScore": 0
        }, {
            "courseCode": "SENG321",
            "enthusiasmScore": 0
        }, {
            "courseCode": "SENG371",
            "enthusiasmScore": 0
        }, {
            "courseCode": "ECE355",
            "enthusiasmScore": 0
        }, {
            "courseCode": "CSC355",
            "enthusiasmScore": 0
        }, {
            "courseCode": "CSC320",
            "enthusiasmScore": 0
        }, {
            "courseCode": "CSC360",
            "enthusiasmScore": 0
        }, {
            "courseCode": "CSC370",
            "enthusiasmScore": 20
        }, {
            "courseCode": "SENG350",
            "enthusiasmScore": 20
        }, {
            "courseCode": "SENG360",
            "enthusiasmScore": 0
        }, {
            "courseCode": "SENG426",
            "enthusiasmScore": 0
        }, {
            "courseCode": "SENG440",
            "enthusiasmScore": 0
        }, {
            "courseCode": "SENG499",
            "enthusiasmScore": 0
        }, {
            "courseCode": "ECE455",
            "enthusiasmScore": 0
        }, {
            "courseCode": "CSC460",
            "enthusiasmScore": 0
        }, {
            "courseCode": "SENG401",
            "enthusiasmScore": 0
        }],
        "teachingObligations": 1,
        "preferredTimes": {
            "fall": {
                "monday": [("8:30", "18:30"), ("19:30", "20:30")],
                "tuesday": [("8:30", "18:30")],
                "wednesday": [("8:30", "18:30")],
                "thursday": [("8:30", "18:30")],
                "friday": [("8:30", "18:30")]
            },
            "spring": {
                "monday": None,
                "tuesday": [("8:30", "18:30")],
                "wednesday": [("8:30", "18:30")],
                "thursday": [("8:30", "18:30")],
                "friday": [("8:30", "18:30")]
            },
            "summer": {
                "monday": [("8:30", "18:30")],
                "tuesday": [("8:30", "18:30")],
                "wednesday": [("8:30", "18:30")],
                "thursday": [("8:30", "18:30")],
                "friday": [("8:30", "18:30")]
            }
        },
        "preferredCoursesPerSemester": {
            "fall": 0,
            "spring": 1,
            "summer": 1
        },
        "preferredNonTeachingSemester": "SPRING",
        "preferredCourseDaySpreads": ["TWF", "T", "W", "F"]
    },
    "2": {
        "name": "Bill Bird",
        "isPeng": True,
        "facultyType": "RESEARCH",
        "qualifiedCoursePreferences": [{
            "courseCode": "CSC111",
            "enthusiasmScore": 78
        }, {
            "courseCode": "CSC115",
            "enthusiasmScore": 20
        }, {
            "courseCode": "ECE255",
            "enthusiasmScore": 0
        }, {
            "courseCode": "CSC230",
            "enthusiasmScore": 20
        }, {
            "courseCode": "ECE260",
            "enthusiasmScore": 0
        }, {
            "courseCode": "SENG265",
            "enthusiasmScore": 0
        }, {
            "courseCode": "CSC225",
            "enthusiasmScore": 20
        }, {
            "courseCode": "ECE310",
            "enthusiasmScore": 0
        }, {
            "courseCode": "SENG275",
            "enthusiasmScore": 0
        }, {
            "courseCode": "SENG310",
            "enthusiasmScore": 195
        }, {
            "courseCode": "ECE458",
            "enthusiasmScore": 0
        }, {
            "courseCode": "CSC361",
            "enthusiasmScore": 0
        }, {
            "courseCode": "CSC226",
            "enthusiasmScore": 20
        }, {
            "courseCode": "ECE360",
            "enthusiasmScore": 0
        }, {
            "courseCode": "SENG321",
            "enthusiasmScore": 0
        }, {
            "courseCode": "SENG371",
            "enthusiasmScore": 0
        }, {
            "courseCode": "ECE355",
            "enthusiasmScore": 0
        }, {
            "courseCode": "CSC355",
            "enthusiasmScore": 78
        }, {
            "courseCode": "CSC320",
            "enthusiasmScore": 0
        }, {
            "courseCode": "CSC360",
            "enthusiasmScore": 20
        }, {
            "courseCode": "CSC370",
            "enthusiasmScore": 20
        }, {
            "courseCode": "SENG350",
            "enthusiasmScore": 0
        }, {
            "courseCode": "SENG360",
            "enthusiasmScore": 0
        }, {
            "courseCode": "SENG426",
            "enthusiasmScore": 0
        }, {
            "courseCode": "SENG440",
            "enthusiasmScore": 0
        }, {
            "courseCode": "SENG499",
            "enthusiasmScore": 0
        }, {
            "courseCode": "ECE455",
            "enthusiasmScore": 0
        }, {
            "courseCode": "CSC460",
            "enthusiasmScore": 0
        }, {
            "courseCode": "SENG401",
            "enthusiasmScore": 0
        }],
        "teachingObligations": 1,
        "preferredTimes": {
            "fall": None,
            "spring": None,
            "summer": None
        },
        "preferredCoursesPerSemester": {
            "fall": 0,
            "spring": 1,
            "summer": 0
        },
        "preferredNonTeachingSemester": None,
        "preferredCourseDaySpreads": []
    }
}
