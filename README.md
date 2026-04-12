# TECHIN 510 - Programming for Digital and Physical User Interfaces

## Labs

### Lab 1: GIX Student Purchase Request System
A Streamlit web application that helps GIX students submit purchase requests and allows Dorothy (Program Coordinator) to review and manage them.

### Lab 2: GIX Course Petition Tracker
A Streamlit web app for GIX students to submit course waiver petitions and for advisors/instructors to review them through a two-stage approval workflow.

## How to Run

### Prerequisites
- Python 3.11+
- Git

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/LukinaChen/Techin510.git
   cd Techin510
   ```

2. Create and activate virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app (lab1 or lab2):
   ```bash
   cd lab1
   streamlit run app.py

   # or
   cd lab2
   streamlit run app.py
   ```

5. Open your browser at: http://localhost:8501
