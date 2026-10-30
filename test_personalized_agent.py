
from agent.agent import run_agent


student_id = "STU1001"

question = (
    "Explain supervised learning "
    "and give me a simple example."
)

result = run_agent(
    question,
    student_id=student_id
)

print("\n--- PERSONALIZED AGENT TEST ---")

print("Agent:", result["answer"])

print("Tools used:", result["tools_used"])
