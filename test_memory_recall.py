
from agent.agent import run_agent

question = """
My student ID is STU1001.

What response preference have I previously
asked you to remember?

Please retrieve my saved memory before answering.
"""

result = run_agent(question)

print("\n--- MEMORY RECALL TEST ---")
print("Agent:", result["answer"])
print("Tools used:", result["tools_used"])
