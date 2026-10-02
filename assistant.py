import json
import os

from dotenv import load_dotenv
from google import genai

from student_tools import (
    calculate_average,
    get_course_info,
    get_student_result,
)


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

client = genai.Client(api_key=api_key)


student_result_tool = {
    "type": "function",
    "name": "get_student_result",
    "description": (
        "Get the fictional academic result of a student using their student ID. "
        "Use this tool when the user asks about a specific student's result, "
        "GPA, program, or semester."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "student_id": {
                "type": "string",
                "description": "The student ID, for example STU-101.",
            }
        },
        "required": ["student_id"],
    },
}


course_info_tool = {
    "type": "function",
    "name": "get_course_info",
    "description": (
        "Get fictional information about a university course. "
        "Use this tool when the user asks about a course, its level, "
        "or its description."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "course_name": {
                "type": "string",
                "description": (
                    "The course name, such as Python, Java, "
                    "or Web Development."
                ),
            }
        },
        "required": ["course_name"],
    },
}


calculate_average_tool = {
    "type": "function",
    "name": "calculate_average",
    "description": (
        "Calculate the average of two numerical values. "
        "Use this tool when the user explicitly asks for an average."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "value1": {
                "type": "number",
                "description": "The first numerical value.",
            },
            "value2": {
                "type": "number",
                "description": "The second numerical value.",
            },
        },
        "required": ["value1", "value2"],
    },
}


TOOLS = [
    student_result_tool,
    course_info_tool,
    calculate_average_tool,
]


SYSTEM_INSTRUCTIONS = """
You are a university student assistant.

Your job is to answer student questions using the available tools.

You have access to fictional student records, fictional course information,
and a calculation tool.

Decide which tool is required based on the user's request.

You may use multiple tools when necessary.

After receiving a tool result, inspect the result and decide whether
another tool is required before producing the final answer.

Do not invent student records, course information, or calculation results.

If a tool reports that information is unavailable, clearly tell the user
that the information could not be found.

Only provide information supported by the user's request and tool results.

When the task is complete, provide a concise and clear final answer.
"""


def execute_tool(name: str, arguments: dict) -> dict:
    """Execute the tool selected by the model."""

    if name == "get_student_result":
        return get_student_result(arguments["student_id"])

    if name == "get_course_info":
        return get_course_info(arguments["course_name"])

    if name == "calculate_average":
        return calculate_average(
            arguments["value1"],
            arguments["value2"],
        )

    return {
        "success": False,
        "message": f"Unknown tool: {name}",
    }


def ask_assistant(question: str) -> str:
    """Run the AI agent loop."""

    try:
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=[
                {
                    "type": "text",
                    "text": f"{SYSTEM_INSTRUCTIONS}\n\nUser request:\n{question}",
                }
            ],
            tools=TOOLS,
            generation_config={
                "thinking_level": "low"
            },
            timeout=30_000,
        )
    except Exception as error:
        return f"Gemini request failed: {error}"

    max_steps = 5

    for _ in range(max_steps):
        function_calls = [
            step
            for step in interaction.steps
            if step.type == "function_call"
        ]

        if not function_calls:
            return interaction.output_text

        tool_results = []

        for step in function_calls:
            print(f"\nTool called: {step.name}")
            print(f"Tool arguments: {step.arguments}")

            arguments = step.arguments

            if isinstance(arguments, str):
                arguments = json.loads(arguments)

            result = execute_tool(step.name, arguments)

            print(f"Tool result: {result}")

            tool_results.append(
                {
                    "type": "function_result",
                    "name": step.name,
                    "call_id": step.id,
                    "result": [
                        {
                            "type": "text",
                            "text": json.dumps(result),
                        }
                    ],
                }
            )

        try:
            interaction = client.interactions.create(
                model="gemini-3.8-flash",
                previous_interaction_id=interaction.id,
                tools=TOOLS,
                input=tool_results,
                generation_config={
                    "thinking_level": "low"
                },
                timeout=30_000,
            )
        except Exception as error:
            return f"Gemini follow-up request failed: {error}"

    return (
        "The agent reached its maximum number of steps "
        "before completing the request."
    )


if __name__ == "__main__":
    question = input("\nYou: ")

    answer = ask_assistant(question)

    print("\nAI:", answer)