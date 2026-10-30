
from tools.student_tools import get_student_fee_status
from tools.support_tools import create_support_request


# TEST 1: Check student fee status
print("\n--- TEST 1: STUDENT FEE STATUS ---")

fee_result = get_student_fee_status("STU1001")

print(fee_result)


# TEST 2: Create a support request
print("\n--- TEST 2: CREATE SUPPORT REQUEST ---")

ticket_result = create_support_request(
    student_id="STU1001",
    issue_description="Payment portal is not working.",
    category="Payment"
)

print(ticket_result)


# TEST 3: Check a non-existing student
print("\n--- TEST 3: INVALID STUDENT ---")

invalid_result = get_student_fee_status("STU9999")

print(invalid_result)
