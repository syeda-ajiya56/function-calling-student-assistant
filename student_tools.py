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


COURSES = {
    "Python": {
        "level": "Beginner",
        "description": "Introduction to Python programming and problem solving.",
    },
    "Java": {
        "level": "Intermediate",
        "description": "Object-oriented programming and Java application development.",
    },
    "Web Development": {
        "level": "Beginner",
        "description": "Introduction to HTML, CSS, JavaScript, and web development.",
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


def get_course_info(course_name: str) -> dict:
    """Return fictional course information."""

    course = COURSES.get(course_name)

    if not course:
        return {
            "success": False,
            "message": f"No course information was found for {course_name}.",
        }

    return {
        "success": True,
        "course": course_name,
        "level": course["level"],
        "description": course["description"],
    }


def calculate_average(value1: float, value2: float) -> dict:
    """Calculate the average of two numbers."""

    average = (value1 + value2) / 2

    return {
        "success": True,
        "value1": value1,
        "value2": value2,
        "average": round(average, 2),
    }


if __name__ == "__main__":
    print(get_student_result("STU-101"))
    print(get_student_result("STU-999"))

    print(get_course_info("Python"))
    print(get_course_info("Unknown"))

    print(calculate_average(3.72, 4.0))