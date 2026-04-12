# GIX Course Petition Tracker

A Streamlit web app for GIX students to submit course waiver petitions and for advisors/instructors to review them through a two-stage approval workflow.

## Features

- **Student Portal**: Submit course waiver petitions with transcript and syllabus uploads (up to 3 courses per petition)
- **Advisor Dashboard**: Review petitions, view uploaded documents inline, approve or reject with notes
- **Instructor Dashboard**: Final approval on advisor-approved petitions
- **Statistics**: Interactive Plotly charts showing petition counts by status and course
- **Visual Status Tracking**: Color-coded cards (white = unread, yellow = viewed, gray = decided) and colored status labels

## Tech Stack

- Python 3.11+
- Streamlit
- Plotly
- Pandas

## How to Run

```bash
# 1. Clone the repository
git clone <repo-url>
cd lab2

# 2. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate.bat  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open at http://localhost:8501

## Demo Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Student | student | 111 |
| Advisor | advisor | 111 |
| Instructor | instructor | 111 |

## Project Structure

```
lab2/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── petitions.json              # Data storage (auto-generated)
├── uploads/                    # Uploaded PDF files (auto-generated)
├── .cursorrules                # Cursor AI configuration
├── CLAUDE.md                   # Claude Code AI configuration
├── .streamlit/config.toml      # Streamlit theme config
├── A-interview-notes.md        # Component A: Interview notes
├── B-ai-usage-log.md           # Component B: AI usage log & prompt log
├── C-architecture.md           # Component C: Architecture & design decisions
├── D-testing.md                # Component D: Testing & validation
├── E-spec.md                   # Component E: Eligibility checker spec & flowchart
├── E-eligibility-claude.py     # Component E: Claude Code implementation
├── E-eligibility-chatgpt.py    # Component E: ChatGPT implementation
├── E-comparison.md             # Component E: Comparison & testing
└── README.md                   # This file
```
