
from memory.memory_manager import (
    save_memory,
    get_memories
)


student_id = "STU1001"


# TEST 1: Save programme information
print("\n--- TEST 1: SAVE MEMORY ---")

result = save_memory(
    student_id,
    "programme",
    "PGDM in Big Data Analytics"
)

print(result)


# TEST 2: Save language preference
print("\n--- TEST 2: SAVE PREFERENCE ---")

result = save_memory(
    student_id,
    "preferred_language",
    "English"
)

print(result)


# TEST 3: Retrieve saved information
print("\n--- TEST 3: RETRIEVE MEMORY ---")

memories = get_memories(student_id)

print(memories)


# TEST 4: Try storing an unapproved category
print("\n--- TEST 4: MEMORY FILTER ---")

result = save_memory(
    student_id,
    "password",
    "sample-password"
)

print(result)
