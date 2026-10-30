
from agent.agent import run_agent

question = """
My student ID is STU1001.
Please remember that I prefer explanations
in simple English.
"""

result = run_agent(question)

print("\n--- MEMORY SAVE TEST ---")
print("Agent:", result["answer"])
print("Tools used:", result["tools_used"])
