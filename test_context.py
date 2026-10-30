
from agent.context_manager import build_context


student_id = "STU1001"


# TEST 1: Academic question
print("\n--- TEST 1: ACADEMIC CONTEXT ---")

context = build_context(
    student_id,
    "Explain deep learning concepts."
)

print(context)


# TEST 2: Programme question
print("\n--- TEST 2: PROGRAMME CONTEXT ---")

context = build_context(
    student_id,
    "Which programme am I studying?"
)

print(context)


# TEST 3: Unrelated question
print("\n--- TEST 3: UNRELATED CONTEXT ---")

context = build_context(
    student_id,
    "What is the weather today?"
)

print(context)
