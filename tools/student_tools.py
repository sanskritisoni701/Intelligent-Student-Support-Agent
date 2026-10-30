
import json
from pathlib import Path


# Locate the student database
DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "students.json"
)


def get_student_fee_status(student_id: str):
    """
    Retrieve fee information for a given student ID.
    """

    try:
        # Open and read the JSON database
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Search for the student
        for student in data["students"]:

            if student["student_id"].lower() == student_id.lower():

                # Return only the relevant fee information
                return {
                    "success": True,
                    "student_id": student["student_id"],
                    "name": student["name"],
                    "fee_status": student["fee_status"],
                    "total_fees": student["total_fees"],
                    "paid_amount": student["paid_amount"],
                    "pending_amount": student["pending_amount"],
                    "due_date": student["due_date"]
                }

        # Student ID was not found
        return {
            "success": False,
            "message": "Student record not found."
        }

    except FileNotFoundError:
        return {
            "success": False,
            "message": "Student database is unavailable."
        }

    except (json.JSONDecodeError, KeyError) as error:
        return {
            "success": False,
            "message": f"Student database error: {error}"
        }
