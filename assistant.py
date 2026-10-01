import json
import os

from dotenv import load_dotenv
from google import genai

from student_tools import get_student_result


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


def ask_assistant(question: str):
    tools = [student_result_tool]

    try:
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=question,
            tools=tools,
            generation_config={
                "thinking_level": "low"
            },
            timeout=30_000,
        )
    except Exception as error:
        return f"Gemini request failed: {error}"

    for step in interaction.steps:
        if step.type == "function_call":
            print(f"\nTool called: {step.name}")
            print(f"Tool arguments: {step.arguments}")

            if step.name == "get_student_result":
                arguments = step.arguments

                if isinstance(arguments, str):
                    arguments = json.loads(arguments)

                result = get_student_result(arguments["student_id"])

                print(f"Tool result: {result}")

                try:
                    follow_up = client.interactions.create(
                        model="gemini-3.8-flash",
                        previous_interaction_id=interaction.id,
                        tools=tools,
                        input=[
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
                        ],
                        generation_config={
                            "thinking_level": "low"
                        },
                        timeout=30_000,
                    )
                except Exception as error:
                    return f"Gemini follow-up request failed: {error}"

                return follow_up.output_text

    return interaction.output_text


if __name__ == "__main__":
    question = input("\nYou: ")

    answer = ask_assistant(question)

    print("\nAI:", answer)