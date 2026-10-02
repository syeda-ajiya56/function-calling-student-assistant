# AI Agent Student Assistant

A small educational AI agent built with Python and Google Gemini that demonstrates how an LLM can make decisions, use multiple tools, inspect tool results, and continue working until a task is complete.

The project builds on the previous function-calling exercise by adding an **agent loop**. Instead of stopping after a single tool call, the agent can decide whether another tool is needed and combine results from multiple tools into one final response.

The project uses fictional university data and does not connect to a real student information system or external university database.

---

## 1. Project Overview

This project was created to understand the basic architecture of an AI agent and how it differs from a standard chatbot or a simple function-calling application.

The agent can:

- Answer simple questions without using a tool
- Look up fictional student academic records
- Retrieve fictional course information
- Perform numerical calculations
- Decide which tool or tools are required
- Use multiple tools for a single request
- Inspect tool results and continue the agent loop
- Combine information from multiple tool calls
- Clearly report unavailable information instead of inventing results

The project contains three custom tools:

```text
get_student_result(student_id)
get_course_info(course_name)
calculate_average(value1, value2)
```

---

## 2. What Is an AI Agent?

An AI agent is an application in which an LLM can do more than simply generate a response.

A basic chatbot may follow this pattern:

```text
User
  ↓
LLM
  ↓
Response
```

An AI agent can follow a more dynamic process:

```text
User Task
    ↓
LLM
    ↓
Decide what action is needed
    ↓
Select a tool
    ↓
Execute the tool
    ↓
Inspect the tool result
    ↓
Decide whether another action is needed
    ↓
Another tool / Final response
```

The LLM acts as the decision-making component, while the application controls and executes the available tools.

---

## 3. Chatbot vs AI Agent

### Basic chatbot

A basic chatbot primarily receives a user message and generates a response.

```text
User → LLM → Response
```

### AI agent

An AI agent can determine whether it needs to take an action, select an appropriate tool, use the tool, inspect the result, and continue the process.

```text
User
 ↓
LLM
 ↓
Tool decision
 ↓
Tool execution
 ↓
Tool result
 ↓
LLM reviews result
 ↓
Another action?
 ↙       ↘
Yes       No
 ↓         ↓
Tool      Final answer
```

The important difference in this project is that the agent can perform **multiple tool calls for one user request**.

---

## 4. Learning Goals

This project demonstrates:

- The difference between a chatbot and an AI agent
- The role of an LLM in agent decision-making
- The role of tools in extending an LLM's capabilities
- How an agent decides whether a tool is needed
- How an application executes a selected tool
- How tool results are returned to the LLM
- How the LLM can inspect a tool result
- How the agent can decide whether another tool is required
- How multiple tool results can be combined into a final response
- How an agent handles unavailable information
- Why application code remains responsible for executing tools

---

## 5. Technology Stack

- Python
- Google Gemini API
- `google-genai`
- `python-dotenv`

The application uses Gemini's Interactions API for the model interaction and tool-calling workflow.

---

## 6. Project Structure

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

## 7. Available Tools

The agent has three fictional tools.

### 7.1 `get_student_result(student_id)`

Looks up a fictional student record using a student ID.

Example:

```text
get_student_result("STU-101")
```

Returns information such as:

- Student name
- Program
- Semester
- GPA

---

### 7.2 `get_course_info(course_name)`

Looks up fictional information about a university course.

Example:

```text
get_course_info("Python")
```

Returns:

- Course name
- Course level
- Course description

---

### 7.3 `calculate_average(value1, value2)`

Calculates the average of two numerical values.

Example:

```text
calculate_average(3.72, 4.0)
```

Result:

```text
3.86
```

---

## 8. Fictional Student Data

The application uses a small fictional dataset:

| Student ID | Name | Program | Semester | GPA |
|---|---|---|---:|---:|
| STU-101 | Ayesha Khan | Computer Science | 4 | 3.72 |
| STU-102 | Hamza Khan | Software Engineering | 3 | 3.45 |
| STU-103 | Sara Ahmed | Information Technology | 5 | 3.88 |

These records are fictional and are used only for demonstrating the agent architecture.

---

## 9. Fictional Course Data

The project contains fictional information for several courses:

| Course | Level | Description |
|---|---|---|
| Python | Beginner | Introduction to Python programming and problem solving. |
| Java | Intermediate | Object-oriented programming and Java application development. |
| Web Development | Beginner | Introduction to HTML, CSS, JavaScript, and web development. |

The agent reports when a requested course is not present in the fictional dataset.

---

## 10. Agent Architecture

The main architecture of the application is:

```text
                    User Request
                         ↓
                  ┌─────────────┐
                  │     LLM     │
                  │  Decision   │
                  └──────┬──────┘
                         ↓
                Is a tool required?
                    ↙          ↘
                  No            Yes
                  ↓              ↓
           Final response   Select tool
                                  ↓
                            Execute tool
                                  ↓
                             Tool result
                                  ↓
                         LLM reviews result
                                  ↓
                     Another tool required?
                         ↙             ↘
                       Yes              No
                        ↓                ↓
                   Next tool       Final response
```

The application therefore combines:

- User input
- Instructions
- LLM
- Tools
- Tool results
- Conversation/interaction state
- Agent loop
- Final response

---

## 11. The Agent Loop

The simplified agent loop implemented by the application is:

```text
1. Receive the user's request
2. Send the request and available tools to Gemini
3. Gemini decides whether a tool is required
4. If no tool is required, return the response
5. If a tool is required, identify the tool and arguments
6. Execute the selected Python function
7. Return the tool result to Gemini
8. Gemini reviews the result
9. Gemini decides whether another tool is needed
10. Repeat if necessary
11. Return the final answer when the task is complete
```

The agent has a maximum number of processing steps to prevent an infinite tool-calling loop.

---

## 12. Single-Tool Example

For this request:

```text
What is the GPA of student STU-101?
```

The agent selected:

```text
get_student_result
```

with:

```text
{'student_id': 'STU-101'}
```

The tool returned:

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

The final AI response was:

```text
The GPA of student STU-101 (Ayesha Khan) is 3.72.
```

This demonstrates a successful tool-selection and tool-execution cycle.

---

## 13. Multi-Tool Agent Example

The most important test was:

```text
What is STU-101's GPA, what level is the Python course, and what is the average of the student's GPA and 4.0?
```

The agent used three tools:

### Step 1 — Student lookup

```text
Tool called: get_student_result
Tool arguments: {'student_id': 'STU-101'}
```

Result:

```text
GPA: 3.72
```

### Step 2 — Course lookup

```text
Tool called: get_course_info
Tool arguments: {'course_name': 'Python'}
```

Result:

```text
Course level: Beginner
```

### Step 3 — Calculation

```text
Tool called: calculate_average
Tool arguments: {'value1': 3.72, 'value2': 4}
```

Result:

```text
Average: 3.86
```

The final response was:

```text
Here are the details based on your request:

* STU-101's GPA: 3.72
* Python Course Level: Beginner
* Average of the GPA (3.72) and 4.0: 3.86
```

This demonstrates the main purpose of the project:

```text
User request
     ↓
get_student_result
     ↓
Tool result
     ↓
get_course_info
     ↓
Tool result
     ↓
calculate_average
     ↓
Tool result
     ↓
Final answer
```

The agent did not require the user to manually request each step. It determined the required tools and combined their results.

---

## 14. Test Results

The completed implementation was tested with several different types of requests.

### Test 1 — Simple Request

Input:

```text
Hello! What can you help me with?
```

Result:

The agent answered directly and explained that it can help with:

- Student academic records
- Course information
- Calculations

No tool was required.

This demonstrates that the agent does not automatically call a tool for every request.

---

### Test 2 — One Tool Required

Input:

```text
What is the GPA of student STU-101?
```

Tool used:

```text
get_student_result
```

Result:

```text
GPA: 3.72
```

Final response:

```text
The GPA of student STU-101 (Ayesha Khan) is 3.72.
```

Status:

```text
PASS
```

---

### Test 3 — Multiple Tools Required

Input:

```text
What is STU-101's GPA, what level is the Python course, and what is the average of the student's GPA and 4.0?
```

Tools used:

```text
get_student_result
get_course_info
calculate_average
```

Results:

```text
GPA: 3.72
Python level: Beginner
Average: 3.86
```

Final response correctly combined all three results.

Status:

```text
PASS
```

This is the primary demonstration of the agent loop.

---

### Test 4 — Unknown Student

Input:

```text
What is the GPA of student STU-999?
```

Tool called:

```text
get_student_result
```

Tool result:

```text
{
    'success': False,
    'message': 'No student record was found for ID STU-999.'
}
```

Final response:

```text
The student record for ID STU-999 could not be found, so their GPA is unavailable.
```

The agent did not invent a GPA.

Status:

```text
PASS
```

---

### Test 5 — Unknown Course

Input:

```text
Tell me about the Rust course.
```

Tool called:

```text
get_course_info
```

Tool result:

```text
{
    'success': False,
    'message': 'No course information was found for Rust.'
}
```

Final response:

```text
I could not find any information for the Rust course.
```

The agent did not invent course information.

Status:

```text
PASS
```

---

## 15. Test Summary

| Test | Tools Used | Expected Behavior | Result |
|---|---|---|---|
| Simple question | None | Answer directly | ✅ Pass |
| Student GPA | `get_student_result` | Retrieve GPA | ✅ Pass |
| Multi-step request | 3 tools | Combine multiple results | ✅ Pass |
| Unknown student | `get_student_result` | Report unavailable | ✅ Pass |
| Unknown course | `get_course_info` | Report unavailable | ✅ Pass |

---

## 16. Agent Instructions

The agent is given instructions that define its responsibility and behavior.

The instructions tell the model to:

- Act as a university student assistant
- Use available tools when necessary
- Decide which tool is appropriate
- Use multiple tools when required
- Inspect tool results before continuing
- Avoid inventing student information
- Avoid inventing course information
- Report unavailable information clearly
- Provide a final answer when the task is complete

This helps establish the difference between simply exposing tools and actually operating an agent.

---

## 17. Application Responsibility

The LLM does not directly execute arbitrary Python code.

The application controls the available tools.

The process is:

```text
1. Gemini decides that a tool is needed
        ↓
2. Gemini returns the tool name and arguments
        ↓
3. Python receives the tool request
        ↓
4. Python executes the approved function
        ↓
5. Python returns the tool result
        ↓
6. Gemini reviews the result
        ↓
7. Gemini decides whether another tool is required
        ↓
8. Final response
```

This separation is important because the application defines exactly what actions the model is allowed to request.

---

## 18. Error Handling

The application includes exception handling around Gemini API requests.

If the Gemini request fails, the application returns an error message instead of silently failing.

The application also uses a request timeout so that an API request does not wait indefinitely.

The agent loop has a maximum number of processing steps to prevent an infinite loop of tool calls.

---

## 19. Security Considerations

This is an educational project using fictional information.

The application does not connect to:

- A real university database
- A real student information system
- Payment systems
- External business databases

The Gemini API key is stored in `.env` and should not be committed to Git.

The application does not allow Gemini to execute arbitrary Python code. Only the explicitly defined tools are available for the model to request.

---

## 20. Setup

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

### 4. Configure the Gemini API key

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY_HERE
```

Do not commit the `.env` file.

### 5. Run the agent

```powershell
python assistant.py
```

The application will prompt:

```text
You:
```

You can then enter a natural-language request.

---

## 21. Example Requests

### Simple request

```text
Hello! What can you help me with?
```

### One-tool request

```text
What is the GPA of student STU-101?
```

### Multi-tool request

```text
What is STU-101's GPA, what level is the Python course, and what is the average of the student's GPA and 4.0?
```

### Unknown student

```text
What is the GPA of student STU-999?
```

### Unknown course

```text
Tell me about the Rust course.
```

---

## 22. Local Tool Testing

The tools can also be tested independently from the Gemini agent.

For example:

```powershell
python -c "from student_tools import get_student_result; print(get_student_result('STU-999'))"
```

Expected result:

```text
{
    'success': False,
    'message': 'No student record was found for ID STU-999.'
}
```

This demonstrates that the application's tool itself handles unavailable data before the result is returned to the model.

---

## 23. Limitations

This is a small educational demonstration rather than a production AI agent platform.

Current limitations include:

- Student data is fictional
- Course data is fictional
- Data is stored directly in Python
- There is no real database
- There is no authentication or authorization
- There are only three tools
- The tools support a limited set of predefined data
- The agent depends on Gemini API availability
- API usage limits can affect requests
- There is no persistent long-term memory
- There is no external search or real-world data retrieval
- The agent loop is intentionally simple
- The project does not implement production monitoring or observability

---

## 24. What This Project Demonstrates

The project demonstrates the progression from simple LLM interaction to an AI agent.

### Stage 1 — Text generation

```text
User
 ↓
LLM
 ↓
Response
```

The model answers directly.

### Stage 2 — Function calling

```text
User
 ↓
LLM
 ↓
Tool selection
 ↓
Tool execution
 ↓
Tool result
 ↓
LLM
 ↓
Response
```

The model can request application-controlled functionality.

### Stage 3 — Agent loop

```text
User
 ↓
LLM
 ↓
Tool 1
 ↓
Result
 ↓
LLM
 ↓
Tool 2
 ↓
Result
 ↓
LLM
 ↓
Tool 3
 ↓
Result
 ↓
Final response
```

The model can continue taking actions until the requested task is complete.

The multi-tool test in this project demonstrates Stage 3.

---

## 25. Key Learning

The main lesson from this project is that an AI agent combines:

```text
LLM
+
Instructions
+
Tools
+
Tool results
+
Interaction state
+
Agent loop
```

The LLM provides the decision-making capability, while the application provides controlled actions through tools.

The model can decide:

```text
"I need student information."
```

The application then executes:

```text
get_student_result(...)
```

The model receives the result and can decide:

```text
"I also need course information."
```

The application executes:

```text
get_course_info(...)
```

The process continues until the agent has enough information to produce the final response.

This demonstrates why an AI agent is more than a chatbot that simply generates text.

---

## 26. Agent Loop in This Project

The complete flow can be summarized as:

```text
             USER TASK
                 ↓
          Gemini / LLM
                 ↓
        Understand the task
                 ↓
       Decide required action
                 ↓
          Select a tool
                 ↓
       Python executes tool
                 ↓
          Tool result
                 ↓
          Back to Gemini
                 ↓
       Inspect the result
                 ↓
     Another tool required?
          ↙           ↘
        YES            NO
         ↓              ↓
   Select next tool   Final answer
         ↓
    Execute tool
         ↓
     Tool result
         ↓
     Back to Gemini
```

This is the core architecture implemented by the project.

---

## 27. Repository

GitHub repository:

https://github.com/syeda-ajiya56/function-calling-student-assistant

---

## 28. Assignment Requirements Checklist

- [x] Learn what an AI agent is
- [x] Understand the role of the LLM
- [x] Understand the role of tools
- [x] Understand the agent loop
- [x] Build a small AI agent
- [x] Use at least two tools
- [x] Add clear agent instructions
- [x] Allow the agent to decide which tools are required
- [x] Execute tools through the Python application
- [x] Return tool results to the LLM
- [x] Support a request requiring one tool
- [x] Support a request requiring multiple tools
- [x] Combine multiple tool results into one answer
- [x] Test a simple request
- [x] Test an unsuccessful student lookup
- [x] Test an unsuccessful course lookup
- [x] Prevent invented information
- [x] Document the agent architecture
- [x] Document the agent loop
- [x] Document test results
- [x] Document limitations
- [x] Document security considerations

---

## 29. Conclusion

This project demonstrates a small but complete AI agent architecture.

The key difference from the previous function-calling implementation is that the application now supports an **agent loop**. Gemini can decide which tools are needed, receive their results, decide whether additional actions are required, and finally combine the collected information into a single response.

The multi-tool test successfully demonstrated this behavior using:

```text
get_student_result
get_course_info
calculate_average
```

The project therefore provides a practical foundation for understanding how AI agents can connect LLMs with application-controlled tools and multi-step workflows.