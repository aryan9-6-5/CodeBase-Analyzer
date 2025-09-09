# CodeBase-Analyser

**AI-powered Debugging, Code Health, and Learning Assistant for Python Projects**

**CodeBase-Analyser** is an AI assistant designed to find bugs, explain fixes, and teach programming concepts—specifically tailored for Python developers and learners. It goes beyond traditional code tools by integrating educational insights directly into the debugging and analysis process.

---

## Features

### Debugging Assistant (Error-First Approach)

Upload your Python files and error traceback to receive:

- Root cause analysis
- Suggested fix
- Plain-English explanation of the issue
- Learning tips on how to avoid the error in the future

Highlights exact lines and functions from your code using AST parsing.  
Supports 20+ common Python error patterns (e.g., `IndexError`, `KeyError`, `TypeError`, etc.).

---

### Code Health Scanner

Analyze entire Python project folders to detect:

- Code smells and anti-patterns
- Missing docstrings and poor naming conventions
- Overly complex functions
- Security issues (e.g., hardcoded credentials)

Generates a quality report with prioritized recommendations.  
Built on `pylint` and custom AST rules, all explained in clear, beginner-friendly language.

---

### Interactive Learning Mode

Ask questions about your own codebase, such as:

- "Explain this function like I’m new to Python."
- "Why is this loop inefficient?"
- "How can I improve readability?"

Provides:

- Step-by-step code walkthroughs
- Explanations tailored to your experience level
- Personalized learning paths based on recurring mistakes

---

## Project Architecture

CodeBase-Analyser/
├── app.py # Streamlit UI
├── core/
│ ├── error_analyzer.py # Traceback parsing, error classification
│ ├── code_scanner.py # AST-based project analysis
│ ├── llm_client.py # Gemini/OpenRouter integration
│ ├── patterns.py # Common error patterns & lessons
│ └── utils.py # Utility functions
├── data/
│ ├── error_patterns.json # Error types and explanations
│ └── examples/ # Sample buggy projects
├── tests/ # Unit tests
└── requirements.txt

---

## Tech Stack

- **Frontend:** Streamlit
- **Backend (Optional):** FastAPI
- **LLM Integration:** Gemini Pro, OpenRouter (Claude, LLaMA, etc.)
- **Static Analysis:** Python `ast`, `pylint`, `flake8`
- **Storage:** Local JSON files and caching

---

## Demo Workflow

- **Debugging Mode:** Upload a file and traceback → receive root cause, fix, and explanation
- **Health Check Mode:** Upload project → receive code quality report
- **Learning Chat:** Ask contextual questions about your code → receive tailored responses

---

## Example Outputs

### Error Debugging Example

Error: KeyError: 'user_id'
Location: model.py, line 42, in get_user

Root Cause:
Dictionary accessed with a missing key

Suggested Fix:
Use dict.get('user_id') or check if key exists before accessing

Explanation:
A KeyError occurs when you try to access a dictionary key that does not exist.

Tip:
Always validate external or dynamic data before dictionary access.

---
### Code Health Report Example
Project Health Summary:

5 functions missing docstrings

2 functions overly complex (Cyclomatic Complexity > 10)

3 unused imports detected

1 hardcoded credential found

Learning Tip:
Documenting code improves readability and helps with future debugging and maintenance.

---

## Installation

```bash
git clone https://github.com/yourusername/CodeBase-Analyser.git
cd CodeBase-Analyser
pip install -r requirements.txt
streamlit run app.py
