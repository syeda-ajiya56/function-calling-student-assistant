# Function Calling Student Assistant

A small AI assistant that demonstrates **function calling with Gemini**.

The assistant can answer general questions directly, but when a user asks for a specific student's academic result, Gemini can decide to call a custom Python function. The application executes the function, returns the result to Gemini, and Gemini generates the final natural-language response.

The project uses fictional student data and does not connect to a real database or external student-information system.

---

## 1. Project Overview

This project was created to understand how AI systems can move beyond text generation and interact with application-controlled tools.

The assistant provides one custom tool:

```text
get_student_result(student_id)
```

The tool looks up a fictional student record using a student ID.

The assistant supports:

- Looking up a student's GPA
- Returning a student's program and semester
- Answering general questions without using the student-result tool
- Handling nonexistent student IDs without inventing information

---

## 2. Learning Goals

This project demonstrates:

- The difference between normal text generation and tool calling
- What a function/tool is in an AI application
- How an LLM can decide when a tool is needed
- How an application executes a requested function
- How tool results are returned to the model
- How the model uses the tool result to produce a final response
- Why the application remains responsible for executing available tools
- How invalid tool input can be handled safely

---

## 3. Technology Stack

- Python
- Google Gemini API
- `google-genai`
- `python-dotenv`

The project uses Gemini's Interactions API for the AI interaction and function-calling flow.

---

## 4. Project Structure

```text
function-calling-student-assistant/
│
├── assistant.py
├── student_tools.py
├── README.md
├── .gitignore
├── .env
└── .venv/
```

The `.env` file and virtual environment are excluded from Git.

---

## 5. Custom Tool

The project defines a local Python function in `student_tools.py`:

```python
get_student_result(student_id)
```

The function uses a small fictional dataset containing three student records.

### Fictional students

| Student ID | Name | Program | Semester | GPA |
|---|---|---|---:|---:|
| STU-101 | Ayesha Khan | Computer Science | 4 | 3.72 |
| STU-102 | Hamza Ali | Software Engineering | 3 | 3.45 |
| STU-103 | Sara Ahmed | Information Technology | 5 | 3.88 |

These records are fictional and are included only for demonstrating function calling.

---

## 6. How Function Calling Works

The application follows this flow:

```text
User request
     ↓
Gemini receives the request
     ↓
Gemini determines whether the custom tool is needed
     ↓
If needed:
Gemini returns a function call and arguments
     ↓
Python application executes get_student_result()
     ↓
The function result is returned to Gemini
     ↓
Gemini generates the final natural-language response
```

For a question that does not require the student-result tool, Gemini can answer directly without calling the function.

The application controls the available tool and executes the function. Gemini does not receive permission to execute arbitrary Python code.

---

## 7. Tool Definition

The custom function is exposed to Gemini with a description and a parameter:

```text
Tool name:
get_student_result

Parameter:
student_id
```

The tool description tells Gemini that the function should be used when the user asks about a specific student's result, GPA, program, or semester.

---

## 8. Test Results

The assistant was tested with multiple requests.

### Test 1 — Tool Required

Question:

```text
What is the GPA of student STU-101?
```

Gemini selected the custom tool:

```text
Tool called: get_student_result
Tool arguments: {'student_id': 'STU-101'}
```

The application executed the function and returned:

```text
{
    'success': True,
    'student_id': 'STU-101',
    'name': 'Ayesha Khan',
    'program': 'Computer Science',
    'semester': 4,
    'gpa': 3.72
}
```

Final AI response:

```text
The GPA of student STU-101 (Ayesha Khan) is 3.72.
```

This demonstrates the complete tool-calling flow.

---

### Test 2 — Tool Not Required

Question:

```text
What can you help me with?
```

The assistant answered directly.

There was no:

```text
Tool called: get_student_result
```

The AI responded with a general explanation of the tasks it can help with, including student-result lookups, writing, coding, learning, research, brainstorming, and planning.

This demonstrates that the custom function is not automatically called for every request.

---

### Test 3 — Another Tool Request

Question:

```text
What is the GPA of student STU-103?
```

Gemini selected the custom tool:

```text
Tool called: get_student_result
Tool arguments: {'student_id': 'STU-103'}
```

The application returned:

```text
{
    'success': True,
    'student_id': 'STU-103',
    'name': 'Sara Ahmed',
    'program': 'Information Technology',
    'semester': 5,
    'gpa': 3.88
}
```

Final AI response:

```text
The GPA of student STU-103 (Sara Ahmed) is 3.88.
```

---

## 9. Invalid Input Test

The project was also tested with a nonexistent student ID.

Question:

```text
What is the GPA of student STU-999?
```

Gemini called the tool:

```text
Tool called: get_student_result
Tool arguments: {'student_id': 'STU-999'}
```

The Python function returned:

```text
{
    'success': False,
    'message': 'No student record was found for ID STU-999.'
}
```

The final AI response was:

```text
No student record was found for student ID STU-999.
Please verify the student ID and try again.
```

The system did not invent a GPA or student record.

This demonstrates that the tool result is treated as the source of truth for student records.

---

## 10. Error and Rate-Limit Handling

During development, the Gemini Free Tier rate limit was reached.

The API returned a rate-limit error indicating:

```text
Rate limit exceeded for model gemini-3.8-flash
```

The assistant was updated with exception handling and a request timeout so that API failures do not leave the application waiting indefinitely.

The current application reports Gemini request failures instead of silently failing.

The Gemini API's availability and limits depend on the selected model and account tier.

---

## 11. Application Responsibility

An important part of function calling is that the model does not directly execute arbitrary application code.

In this project:

1. Gemini can request the specific tool that the application exposes.
2. The Python application receives the requested function and arguments.
3. The application executes `get_student_result()`.
4. The application sends the function result back to Gemini.
5. Gemini generates the final response.

The available function is therefore controlled by the application.

---

## 12. Security Considerations

The project uses only fictional student information.

The application does not connect to:

- A real university database
- A real student information system
- A payment system
- An external business database

The Gemini API key is stored in `.env` and is excluded from Git using `.gitignore`.

The application also does not allow Gemini to execute arbitrary Python code. Only the explicitly defined `get_student_result` tool can be invoked.

---

## 13. Setup

### 1. Clone the repository

```bash
git clone https://github.com/syeda-ajiya56/function-calling-student-assistant.git
cd function-calling-student-assistant
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install google-genai python-dotenv
```

### 4. Configure the API key

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY_HERE
```

Do not commit the `.env` file.

### 5. Run the assistant

```powershell
python assistant.py
```

Then enter a natural-language request such as:

```text
What is the GPA of student STU-101?
```

---

## 14. Local Tool Testing

The student-result function can also be tested without calling Gemini.

For example:

```powershell
python -c "from student_tools import get_student_result; print(get_student_result('STU-999'))"
```

The invalid ID returns:

```text
{'success': False, 'message': 'No student record was found for ID STU-999.'}
```

This confirms that the local tool handles invalid student IDs independently of the AI model.

---

## 15. Limitations

This is a small educational demonstration rather than a production student-information system.

Current limitations include:

- Student data is fictional and stored directly in Python.
- There is no real database.
- There is only one custom tool.
- The tool supports student-result lookup only.
- The assistant depends on Gemini API availability.
- Gemini Free Tier usage limits can prevent additional API requests.
- The system does not implement authentication or authorization.
- The student ID lookup is based on the predefined fictional records.

---

## 16. What This Project Demonstrates

The project demonstrates the difference between:

### Text generation

The model receives a question and generates an answer directly.

Example:

```text
What can you help me with?
```

No custom tool is required.

### Tool calling

The model determines that external application data is needed.

Example:

```text
What is the GPA of student STU-101?
```

Gemini requests:

```text
get_student_result("STU-101")
```

The application executes the function and returns the result.

Gemini then uses that result to produce the final answer.

---

## 17. Key Learning

The main lesson from this project is that an LLM can decide when a tool is useful, but the application remains responsible for defining and executing the available functions.

The model can request:

```text
get_student_result(student_id)
```

but the Python application controls what that function actually does and what information it returns.

This creates a clear separation between:

```text
AI reasoning
     ↓
Tool request
     ↓
Application-controlled execution
     ↓
Tool result
     ↓
AI response
```

---

## 18. Repository

GitHub repository:

https://github.com/syeda-ajiya56/function-calling-student-assistant

---

## 19. Assignment Requirements Checklist

- [x] Create a local custom function
- [x] Use fictional data
- [x] Connect the function to an LLM
- [x] Allow the model to determine when the function is needed
- [x] Execute the function in the application
- [x] Return the function result to the model
- [x] Generate a final natural-language response
- [x] Test a request requiring the tool
- [x] Test a request that does not require the tool
- [x] Test multiple tool requests
- [x] Test invalid input
- [x] Prevent invented results for an unknown student
- [x] Document the function-calling workflow
- [x] Document limitations and security considerations
