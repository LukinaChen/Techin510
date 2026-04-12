# Project Context

## What This Project Is
A Streamlit web app that allows GIX students to submit course waiver petitions, and enables advisors (Jason) and course instructors to review, approve, or reject those petitions through a two-stage approval workflow.

## Tech Stack
- Python 3.11+
- Streamlit for the web interface
- Plotly for interactive charts
- Pandas for data manipulation
- JSON file for data persistence

## Project Structure
- `app.py` -- Main application entry point (login, student, advisor, instructor views)
- `petitions.json` -- Data storage for petition records
- `uploads/` -- Uploaded PDF files (transcripts, syllabi), organized by petition ID
- `.cursorrules` -- Cursor AI configuration
- `.streamlit/config.toml` -- Streamlit theme (primaryColor: black)
- `requirements.txt` -- Python dependencies

## Development Commands
- Run the app: `streamlit run app.py`
- Install dependencies: `pip install -r requirements.txt`
- Activate venv: `source .venv/bin/activate`

## Coding Standards
- Follow PEP 8 style guidelines
- Use type hints on all function signatures
- Write Google-style docstrings for all functions
- Handle errors gracefully; never let the app crash on user input
- Never hardcode sensitive data (API keys, passwords)

## Business Logic
- Three user roles: student, advisor, instructor
- Approval flow: Student → Advisor → Instructor (two approvals needed)
- Rejection by either reviewer = immediate rejection visible to student
- Students can submit up to 3 external courses per petition
- Each course requires: institution, grade (min 2.7), transcript PDF, syllabus PDF
- Documents must be in official English (university-stamped translation)
- Advisor sees all petitions; Instructor only sees Advisor-Approved ones
- Student sees "Advisor Approved" displayed as "Under Review"

## Important Notes
- This is a course project for TECHIN 510 at UW GIX
- The audience for this app is GIX students and academic advisors (specifically Jason Evans, ASC)
- Demo login credentials: student/111, advisor/111, instructor/111
- When making changes, always verify the app still runs with `streamlit run app.py`
