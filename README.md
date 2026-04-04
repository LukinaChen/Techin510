# TECHIN 510 - Lab 1: GIX Student Purchase Request System

## Project Overview
A Streamlit web application that helps GIX students submit 
purchase requests and allows Dorothy (Program Coordinator) 
to review and manage them.

## Features
- Students can submit purchase requests with all required fields
- Dorothy can view all submissions on a coordinator dashboard
- Dorothy can update approval status and add rejection notes
- Clean, accessible UI with custom theme

## How to Run

### Prerequisites
- Python 3.11+
- Git

### Setup Instructions

1. Clone the repository:
   git clone https://github.com/LukinaChen/Techin510.git
   cd Techin510

2. Create and activate virtual environment:
   python3 -m venv .venv
   source .venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run the app:
   python3 -m streamlit run app.py

5. Open your browser at:
   http://localhost:8501