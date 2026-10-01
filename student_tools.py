STUDENT_RESULTS = {
    "STU-101": {
        "name": "Ayesha Khan",
        "program": "Computer Science",
        "semester": 4,
        "gpa": 3.72,
    },
    "STU-102": {
        "name": "Hamza Khan",
        "program": "Software Engineering",
        "semester": 3,
        "gpa": 3.45,
    },
    "STU-103": {
        "name": "Sara Ahmed",
        "program": "Information Technology",
        "semester": 5,
        "gpa": 3.88,
    },
}


def get_student_result(student_id: str) -> dict:
    """Return fictional student result information for a student ID."""

    student = STUDENT_RESULTS.get(student_id)

    if not student:
        return {
            "success": False,
            "message": f"No student record was found for ID {student_id}.",
        }

    return {
        "success": True,
        "student_id": student_id,
        "name": student["name"],
        "program": student["program"],
        "semester": student["semester"],
        "gpa": student["gpa"],
    }

if __name__ == "__main__":
    print(get_student_result("STU-101"))
    print(get_student_result("STU-999"))

    