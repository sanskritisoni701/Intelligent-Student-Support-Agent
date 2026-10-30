
import json
import uuid
from pathlib import Path
from datetime import datetime, timezone


# Location where support tickets will be stored
TICKET_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "support_tickets.json"
)


def create_support_request(
    student_id: str,
    issue_description: str,
    category: str = "General"
):
    """
    Create and save a student support ticket.
    """

    try:
        # Validate inputs
        if not student_id.strip():
            return {
                "success": False,
                "message": "Student ID is required."
            }

        if not issue_description.strip():
            return {
                "success": False,
                "message": "Issue description is required."
            }

        # Create a unique ticket
        ticket = {
            "ticket_id": "TKT-" + uuid.uuid4().hex[:8].upper(),
            "student_id": student_id.strip(),
            "category": category.strip(),
            "description": issue_description.strip(),
            "status": "Open",
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        # Read existing tickets
        if TICKET_FILE.exists():
            with open(TICKET_FILE, "r", encoding="utf-8") as file:
                tickets = json.load(file)
        else:
            tickets = []

        # Add new ticket
        tickets.append(ticket)

        # Save updated tickets
        with open(TICKET_FILE, "w", encoding="utf-8") as file:
            json.dump(tickets, file, indent=4)

        return {
            "success": True,
            "message": "Support request created successfully.",
            "ticket": ticket
        }

    except (OSError, json.JSONDecodeError) as error:
        return {
            "success": False,
            "message": f"Unable to create support request: {error}"
        }
