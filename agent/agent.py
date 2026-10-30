
import os
import json
import time

from dotenv import load_dotenv
from groq import Groq

from tools.student_tools import get_student_fee_status
from tools.support_tools import create_support_request
from tools.policy_tools import search_policy

from memory.memory_manager import (
    save_memory,
    get_memories
)

from agent.context_manager import build_context


# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL")

if not API_KEY:
    raise ValueError("Groq API key not found in .env file.")

if not MODEL:
    raise ValueError("Groq model not configured in .env file.")

client = Groq(api_key=API_KEY)


# ==========================================
# 2. DEFINE AVAILABLE AI TOOLS
# ==========================================

TOOLS = [

    # TOOL 1: Student fee status
    {
        "type": "function",
        "function": {
            "name": "get_student_fee_status",
            "description": (
                "Retrieve the fee status of a student "
                "using their student ID."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "student_id": {
                        "type": "string",
                        "description": "The student's ID."
                    }
                },
                "required": ["student_id"]
            }
        }
    },

    # TOOL 2: Create support request
    {
        "type": "function",
        "function": {
            "name": "create_support_request",
            "description": (
                "Create a support ticket when a student "
                "requests help with an issue."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "student_id": {
                        "type": "string"
                    },
                    "issue_description": {
                        "type": "string"
                    },
                    "category": {
                        "type": "string"
                    }
                },
                "required": [
                    "student_id",
                    "issue_description"
                ]
            }
        }
    },

    # TOOL 3: Search student handbook
    {
        "type": "function",
        "function": {
            "name": "search_policy",
            "description": (
                "Search the student handbook for policy "
                "information about fees, scholarships, "
                "course changes, attendance and support."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Policy-related question."
                    }
                },
                "required": ["question"]
            }
        }
    },

    # TOOL 4: Save student memory
    {
        "type": "function",
        "function": {
            "name": "save_memory",
            "description": (
                "Save useful long-term student information "
                "when the student explicitly asks you to "
                "remember it."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "student_id": {
                        "type": "string"
                    },
                    "category": {
                        "type": "string",
                        "enum": [
                            "programme",
                            "preferred_language",
                            "response_preference",
                            "learning_preference"
                        ]
                    },
                    "value": {
                        "type": "string"
                    }
                },
                "required": [
                    "student_id",
                    "category",
                    "value"
                ]
            }
        }
    },

    # TOOL 5: Retrieve student memory
    {
        "type": "function",
        "function": {
            "name": "get_memories",
            "description": (
                "Retrieve previously saved student "
                "preferences and programme information."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "student_id": {
                        "type": "string"
                    }
                },
                "required": ["student_id"]
            }
        }
    }
]


# ==========================================
# 3. MAP TOOLS TO PYTHON FUNCTIONS
# ==========================================

AVAILABLE_FUNCTIONS = {
    "get_student_fee_status": get_student_fee_status,
    "create_support_request": create_support_request,
    "search_policy": search_policy,
    "save_memory": save_memory,
    "get_memories": get_memories
}


# ==========================================
# 4. MAIN AGENT FUNCTION
# ==========================================

def run_agent(user_question, student_id=None):

    # STEP 0: INITIALIZE MEASUREMENTS

    start_time = time.perf_counter()

    total_input_tokens = 0
    total_output_tokens = 0

    execution_trace = []
    tools_used = []

    # STEP 0.1: TRACE RECORDING FUNCTION

    def add_trace(event, **details):

        execution_trace.append({
            "event": event,
            "elapsed_seconds": round(
                time.perf_counter() - start_time, 3
            ),
            **details
        })

    add_trace(
        "user_query_received",
        question=user_question
    )

    # STEP 1: BUILD RELEVANT STUDENT CONTEXT

    context = "No student-specific context provided."

    if student_id:

        context = build_context(
            student_id,
            user_question
        )

    add_trace(
        "context_selected",
        student_id_provided=bool(student_id),
        context_available=(
            context != "No student-specific context provided."
        ),
        context_length=len(context)
    )

    # STEP 2: DEFINE AGENT INSTRUCTIONS

    system_prompt = """
    You are an Intelligent Student Support Agent.

    Help students with academic, administrative,
    financial and technical queries.

    TOOL SELECTION RULES:

    1. Use get_student_fee_status for personal fee
       balance, payment history and fee status.

    2. Use search_policy for general college policies,
       deadlines, scholarships, course changes,
       attendance and payment-related problems.

    3. A student ID is not required for general
       policy retrieval.

    4. Use create_support_request when a student
       explicitly asks to create a support ticket.

    RESPONSE RULES:

    5. Never invent student records or fee information.

    6. Ask for a student ID if a personal fee query
       requires one and it is missing.

    7. Answer policy questions only using retrieved
       handbook evidence.

    8. Never invent policy rules, deadlines or percentages.

    9. Never claim that a support ticket was created
       unless the tool confirms success.

    10. Answer clearly and in simple language.

    MEMORY RULES:

    11. When a student explicitly asks you to remember
        useful long-term information, use save_memory.

    12. Only save approved memory categories.

    13. Never store passwords, OTPs, sensitive personal
        information or temporary issues.

    14. When a student asks what you remember about
        them, use get_memories.

    15. Never guess or invent remembered information.

    16. If no relevant memory exists, say so.

    17. Never retrieve or disclose another student's memory.

    18. If the student ID is missing, ask for it before
        saving or retrieving personal memory.

    CONTEXT RULES:

    19. Use the selected student context when relevant.

    20. Do not invent information that is absent
        from the selected context.
    """

    # STEP 3: ADD SELECTED CONTEXT TO SYSTEM PROMPT

    system_prompt += (
        "\n\nSELECTED STUDENT CONTEXT:\n" + context
    )

    # Provide active student ID to the agent

    if student_id:

        system_prompt += (
            f"\n\nACTIVE STUDENT ID: {student_id}\n"
            "Use this student ID for personal student "
            "queries. Do not ask the student to provide "
            "it again when it is already available."
        )

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_question
        }
    ]

    # ==========================================
    # STEP 4: START AGENT LOOP
    # ==========================================

    for step in range(5):

        # STEP 4.1: SEND REQUEST TO GROQ

        add_trace(
            "llm_request",
            iteration=step + 1,
            message_count=len(messages)
        )

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0
        )

        # STEP 4.2: RECORD TOKEN USAGE

        usage = response.usage

        if usage:

            total_input_tokens += usage.prompt_tokens or 0
            total_output_tokens += usage.completion_tokens or 0

        assistant_message = response.choices[0].message

        # STEP 4.3: RECORD MODEL DECISION

        add_trace(
            "llm_response",
            iteration=step + 1,
            tool_requested=bool(assistant_message.tool_calls),
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0
        )

        # ==========================================
        # STEP 5: CHECK FOR FINAL ANSWER
        # ==========================================

        if not assistant_message.tool_calls:

            add_trace(
                "final_answer_generated",
                answer_generated=bool(assistant_message.content)
            )

            latency = time.perf_counter() - start_time

            return {
                "answer": assistant_message.content,
                "tools_used": tools_used,
                "steps": step + 1,

                "latency_seconds": round(latency, 3),

                "token_usage": {
                    "input_tokens": total_input_tokens,
                    "output_tokens": total_output_tokens,
                    "total_tokens": (
                        total_input_tokens + total_output_tokens
                    )
                },

                "trace": execution_trace
            }

        # ==========================================
        # STEP 6: ADD TOOL REQUEST TO CONVERSATION
        # ==========================================

        messages.append(
            assistant_message.model_dump(exclude_none=True)
        )

        # ==========================================
        # STEP 7: EXECUTE REQUESTED TOOLS
        # ==========================================

        for tool_call in assistant_message.tool_calls:

            function_name = tool_call.function.name

            add_trace(
                "tool_call",
                tool_name=function_name
            )

            try:

                arguments = json.loads(
                    tool_call.function.arguments
                )

                # STEP 7.1: INJECT STUDENT ID

                if (
                    student_id
                    and function_name in [
                        "get_student_fee_status",
                        "create_support_request",
                        "save_memory",
                        "get_memories"
                    ]
                ):

                    arguments.setdefault(
                        "student_id",
                        student_id
                    )

                # STEP 7.2: CHECK TOOL AVAILABILITY

                if function_name not in AVAILABLE_FUNCTIONS:

                    result = {
                        "success": False,
                        "message": "Tool is not available."
                    }

                else:

                    function_to_call = AVAILABLE_FUNCTIONS[
                        function_name
                    ]

                    # STEP 7.3: EXECUTE PYTHON FUNCTION

                    result = function_to_call(**arguments)

                tools_used.append(function_name)

                # STEP 7.4: RECORD TOOL RESULT

                tool_success = (
                    result.get("success")
                    if isinstance(result, dict)
                    else None
                )

                result_preview = json.dumps(
                    result,
                    default=str
                )[:1200]

                add_trace(
                    "tool_result",
                    tool_name=function_name,
                    success=tool_success,
                    result_keys=(
                        list(result.keys())
                        if isinstance(result, dict)
                        else []
                    ),
                    result_preview=result_preview
                )

            except Exception as error:

                result = {
                    "success": False,
                    "message": f"Tool execution failed: {str(error)}"
                }

                add_trace(
                    "tool_error",
                    tool_name=function_name,
                    error=str(error)
                )

            # ==========================================
            # STEP 8: RETURN TOOL OUTPUT TO LLM
            # ==========================================

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": json.dumps(
                    result,
                    default=str
                )
            })

    # ==========================================
    # STEP 9: MAXIMUM ITERATIONS REACHED
    # ==========================================

    latency = time.perf_counter() - start_time

    add_trace(
        "maximum_iterations_reached",
        max_iterations=5
    )

    return {
        "answer": (
            "I could not complete your request "
            "within the allowed steps."
        ),

        "tools_used": tools_used,
        "steps": 5,

        "latency_seconds": round(latency, 3),

        "token_usage": {
            "input_tokens": total_input_tokens,
            "output_tokens": total_output_tokens,
            "total_tokens": (
                total_input_tokens + total_output_tokens
            )
        },

        "trace": execution_trace
    }
