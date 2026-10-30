
from agent.agent import run_agent


print("\n========================================")
print("INTELLIGENT STUDENT SUPPORT AGENT")
print("TRACING AND MEASUREMENT TEST")
print("========================================")


def run_test(test_number, test_name, question, student_id=None):

    print(f"\n{'=' * 45}")
    print(f"TEST {test_number}: {test_name}")
    print("=" * 45)

    print("\nUser Question:", question)

    # Execute agent
    result = run_agent(
        question,
        student_id=student_id
    )

    # Display answer
    print("\n--- AGENT RESPONSE ---")
    print(result.get("answer", "No response generated."))

    # Display tools used
    print("\n--- TOOLS USED ---")

    tools = result.get("tools_used", [])

    if tools:
        for tool in tools:
            print(f"✓ {tool}")
    else:
        print("No tools used.")

    # Display latency
    print("\n--- LATENCY ---")

    latency = result.get("latency_seconds")

    if latency is not None:
        print(f"Execution time: {latency} seconds")
    else:
        print("Latency data unavailable.")

    # Display token usage
    print("\n--- TOKEN USAGE ---")

    usage = result.get("token_usage", {})

    print("Input tokens:", usage.get("input_tokens", "Unavailable"))
    print("Output tokens:", usage.get("output_tokens", "Unavailable"))
    print("Total tokens:", usage.get("total_tokens", "Unavailable"))

    # Display agent steps
    print("\n--- AGENT STEPS ---")
    print("Steps executed:", result.get("steps", "Unavailable"))

    # Display execution trace
    print("\n--- EXECUTION TRACE ---")

    trace = result.get("trace", [])

    if trace:
        for event in trace:
            print(event)
    else:
        print("No detailed execution events recorded yet.")

    print("\nTEST COMPLETED")


# ==========================================
# TEST 1: FEE STATUS
# ==========================================

run_test(
    1,
    "FEE STATUS",
    "What is the current fee status of student STU1001?",
    student_id="STU1001"
)


# ==========================================
# TEST 2: SUPPORT REQUEST
# ==========================================

run_test(
    2,
    "SUPPORT REQUEST",
    "Create a support ticket. The payment portal is not working.",
    student_id="STU1001"
)


# ==========================================
# TEST 3: GENERAL QUESTION
# ==========================================

run_test(
    3,
    "GENERAL QUESTION",
    "What can you help students with?",
    student_id="STU1001"
)


# ==========================================
# TEST 4: PAYMENT POLICY
# ==========================================

run_test(
    4,
    "PAYMENT POLICY",
    "The payment portal failed. Can I pay on the next working day?",
    student_id="STU1001"
)


# ==========================================
# TEST 5: ATTENDANCE POLICY
# ==========================================

run_test(
    5,
    "ATTENDANCE POLICY",
    "What is the exact minimum attendance percentage?",
    student_id="STU1001"
)


print("\n========================================")
print("ALL FIVE TESTS COMPLETED")
print("========================================")
