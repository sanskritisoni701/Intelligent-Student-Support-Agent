
from tools.policy_tools import search_policy


# TEST 1: Fee payment question
print("\n--- TEST 1: FEE PAYMENT ---")

result = search_policy(
    "What should I do if the payment portal fails?"
)

print(result)


# TEST 2: Scholarship question
print("\n--- TEST 2: SCHOLARSHIP ---")

result = search_policy(
    "How can I apply for a scholarship?"
)

print(result)


# TEST 3: Missing information
print("\n--- TEST 3: ATTENDANCE ---")

result = search_policy(
    "What is the exact minimum attendance percentage?"
)

print(result)
