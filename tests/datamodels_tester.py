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
