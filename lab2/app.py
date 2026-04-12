"""GIX Course Petition Tracker — Streamlit app.

A tool for GIX students to submit course waiver petitions
and for advisors (Jason) and instructors to review and track them.

Approval flow:
  Student submits → Advisor reviews → if Advisor approves → Instructor reviews → final decision
  If either Advisor or Instructor rejects → student sees Rejected immediately.
"""

import base64
import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="GIX Course Petition Tracker", page_icon="📋", layout="wide")

st.markdown("""
<style>
    /* Bold all form field labels */
    .stTextInput label, .stSelectbox label, .stRadio label,
    .stNumberInput label, .stFileUploader label, .stTextArea label {
        font-weight: 700 !important;
    }
    /* Rounded buttons */
    div[data-testid="stButton"] button {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

DATA_PATH = Path(__file__).resolve().parent / "petitions.json"
UPLOADS_DIR = Path(__file__).resolve().parent / "uploads"

GIX_COURSES = [
    "TECHIN 509 - Prototyping Studio",
    "TECHIN 510 - Programming for Digital and Physical UI",
    "TECHIN 511 - Signals and Sensors",
    "TECHIN 512 - Design Thinking",
    "TECHIN 513 - Managing Tech Projects",
    "TECHIN 514 - Hardware/Software Lab",
    "TECHIN 515 - Data Science",
    "TECHIN 516 - Connected Devices",
]

PROGRAMS = ["MSTI", "GIX PMP", "Other"]

USERS = {
    "student": {"password": "111", "role": "student"},
    "advisor": {"password": "111", "role": "advisor"},
    "instructor": {"password": "111", "role": "instructor"},
}

# Status constants
STATUS_SUBMITTED = "Submitted"
STATUS_ADVISOR_APPROVED = "Advisor Approved"
STATUS_APPROVED = "Approved"
STATUS_REJECTED = "Rejected"


def load_petitions() -> list[dict]:
    if DATA_PATH.exists():
        return json.loads(DATA_PATH.read_text())
    return []


def save_petitions(petitions: list[dict]) -> None:
    DATA_PATH.write_text(json.dumps(petitions, indent=2, default=str))


# --- Status helpers ---

def status_color_tag(status: str) -> str:
    """Return an HTML span with colored status text."""
    colors = {
        STATUS_SUBMITTED: "#888888",
        STATUS_ADVISOR_APPROVED: "#1a73e8",
        STATUS_APPROVED: "#2e7d32",
        STATUS_REJECTED: "#c62828",
    }
    color = colors.get(status, "#888888")
    return f'<span style="color:{color}; font-weight:600;">{status}</span>'


def card_bg_color(petition: dict, role: str) -> str:
    """Return background color based on viewing state for this role."""
    viewed_key = f"viewed_by_{role}"
    decided = petition["status"] in [STATUS_ADVISOR_APPROVED, STATUS_APPROVED, STATUS_REJECTED]

    if decided:
        return "#f5f5f5"  # light gray — decided
    elif petition.get(viewed_key):
        return "#fffde7"  # light yellow — viewed but not decided
    else:
        return "#ffffff"  # white — new/unread


def mark_as_viewed(petitions: list[dict], petition_id: int, role: str) -> None:
    """Mark a petition as viewed by this role."""
    for p in petitions:
        if p["id"] == petition_id and not p.get(f"viewed_by_{role}"):
            p[f"viewed_by_{role}"] = True
            save_petitions(petitions)
            break


# --- Login / Logout ---

def render_login() -> None:
    if not st.session_state.get("show_login"):
        st.write("")
        st.write("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.caption("Demo credentials — Student: student / 111 | Advisor: advisor / 111 | Instructor: instructor / 111")
            role = st.radio("Log in as", ["Student", "Advisor", "Instructor"], index=None)
            if role:
                st.session_state["login_role"] = role.lower()
                st.session_state["show_login"] = True
                st.rerun()
    else:
        role = st.session_state.get("login_role", "student")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.subheader(f"Log In — {role.capitalize()}")
            if role == "student":
                username = st.text_input("UW NetID", autocomplete="off")
            else:
                username = st.text_input("Username", autocomplete="off")
            password = st.text_input("Password", type="password", autocomplete="new-password")
            login_col, back_col = st.columns(2)
            with login_col:
                if st.button("Log in", type="primary", use_container_width=True):
                    user = USERS.get(role)
                    if user and password == user["password"]:
                        st.session_state["logged_in"] = True
                        st.session_state["role"] = role
                        st.session_state["username"] = username
                        st.session_state["show_login"] = False
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
            with back_col:
                if st.button("Back", use_container_width=True):
                    st.session_state["show_login"] = False
                    st.rerun()


def render_logout() -> None:
    col1, col2, col3 = st.columns([5, 2, 1])
    with col2:
        role_label = st.session_state["role"].capitalize()
        st.caption(f"Logged in as **{role_label}**")
    with col3:
        if st.button("Log out"):
            st.session_state["logged_in"] = False
            st.session_state["role"] = None
            st.session_state["username"] = None
            st.rerun()


# --- Student pages ---

def render_student_page() -> None:
    st.header("Submit a Course Petition")
    st.write("Submit your course waiver request. You may submit up to 3 previous courses to waive 1 GIX course.")
    st.caption("Each course requires the institution name, a transcript file, and a syllabus file.")

    if "num_courses" not in st.session_state:
        st.session_state["num_courses"] = 1

    student_name = st.text_input("Your Name")
    student_email = st.text_input("Your UW Email")
    program = st.selectbox("Program", PROGRAMS)
    gix_course = st.selectbox("GIX Course to Waive", GIX_COURSES)
    is_english = st.radio("Is your transcript/syllabus in official English?", ["Yes", "No"], index=None)

    st.divider()
    courses = []
    for n in range(st.session_state["num_courses"]):
        if n == 0:
            st.subheader(f"Course {n + 1}")
        else:
            title_col, delete_col = st.columns([9, 1])
            with title_col:
                st.subheader(f"Course {n + 1}")
            with delete_col:
                if st.button("🗑️", key=f"delete_{n}", help=f"Remove Course {n + 1}"):
                    st.session_state["num_courses"] -= 1
                    st.rerun()
        institution = st.text_input(f"Institution Where You Took Course {n + 1}", key=f"inst_{n}")
        grade = st.number_input(f"Grade Received for Course {n + 1} (on 4.0 scale)", min_value=0.0, max_value=4.0, step=0.1, key=f"grade_{n}")
        transcript = st.file_uploader(f"Transcript for Course {n + 1} (PDF)", type=["pdf"], key=f"transcript_{n}")
        syllabus = st.file_uploader(f"Syllabus for Course {n + 1} (PDF)", type=["pdf"], key=f"syllabus_{n}")
        course_notes = st.text_area(f"Additional Notes for Course {n + 1} (optional)", key=f"course_notes_{n}")
        courses.append({"institution": institution, "grade": grade, "transcript": transcript, "syllabus": syllabus, "notes": course_notes})
        st.divider()

    if st.session_state["num_courses"] < 3:
        if st.button("➕ Add Another Course"):
            st.session_state["num_courses"] += 1
            st.rerun()

    st.divider()
    if st.button("Submit Petition", type="primary", use_container_width=True):
        errors = []
        if not student_name:
            errors.append("Please fill in your name.")
        if not student_email:
            errors.append("Please fill in your UW email.")
        if is_english is None:
            errors.append("Please select whether your documents are in official English.")
        elif is_english == "No":
            errors.append("Only official English documents are accepted. Please obtain an official translation from your university.")

        for n, c in enumerate(courses):
            if not c["institution"]:
                errors.append(f"Please fill in the institution for Course {n + 1}.")
            if c["grade"] < 2.7:
                errors.append(f"Course {n + 1}: A minimum GPA of 2.7 is required.")
            if not c["transcript"]:
                errors.append(f"Please upload a transcript for Course {n + 1}.")
            if not c["syllabus"]:
                errors.append(f"Please upload a syllabus for Course {n + 1}.")

        if errors:
            for e in errors:
                st.error(e)
            return

        petition_id = len(load_petitions()) + 1
        petition_dir = UPLOADS_DIR / str(petition_id)
        petition_dir.mkdir(parents=True, exist_ok=True)

        course_entries = []
        for n in range(st.session_state["num_courses"]):
            transcript_path = petition_dir / f"course{n+1}_transcript_{courses[n]['transcript'].name}"
            syllabus_path = petition_dir / f"course{n+1}_syllabus_{courses[n]['syllabus'].name}"
            transcript_path.write_bytes(courses[n]["transcript"].getvalue())
            syllabus_path.write_bytes(courses[n]["syllabus"].getvalue())
            course_entries.append({
                "institution": courses[n]["institution"],
                "grade": courses[n]["grade"],
                "transcript_filename": courses[n]["transcript"].name,
                "transcript_path": str(transcript_path),
                "syllabus_filename": courses[n]["syllabus"].name,
                "syllabus_path": str(syllabus_path),
                "notes": courses[n]["notes"],
            })

        petition = {
            "id": petition_id,
            "student_name": student_name,
            "student_email": student_email,
            "program": program,
            "gix_course": gix_course,
            "is_english": is_english,
            "courses": course_entries,
            "status": STATUS_SUBMITTED,
            "advisor_notes": "",
            "instructor_notes": "",
            "viewed_by_advisor": False,
            "viewed_by_instructor": False,
            "submitted_at": datetime.now().isoformat(),
        }

        petitions = load_petitions()
        petitions.append(petition)
        save_petitions(petitions)

        keys_to_clear = [k for k in st.session_state if k.startswith(("inst_", "grade_", "transcript_", "syllabus_", "course_notes_"))]
        for k in keys_to_clear:
            del st.session_state[k]
        st.session_state["num_courses"] = 1
        st.session_state["submitted_success"] = True
        st.rerun()


def render_success_page() -> None:
    st.write("")
    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.success("Petition submitted successfully!")
        st.write("Your petition has been received and is now under review.")
        if st.button("Submit Another Petition", type="primary", use_container_width=True):
            st.session_state["submitted_success"] = False
            st.rerun()


def render_student_page_wrapper() -> None:
    if st.session_state.get("submitted_success"):
        render_success_page()
    else:
        render_student_page()


def render_student_history() -> None:
    st.header("My Petitions")
    petitions = load_petitions()
    my_petitions = [p for p in petitions if p.get("student_name")]

    if not my_petitions:
        st.info("You have not submitted any petitions yet.")
        return

    for p in my_petitions:
        # Student sees simplified status
        display_status = p["status"]
        if display_status == STATUS_ADVISOR_APPROVED:
            display_status = "Under Review"  # student doesn't need to know internal flow

        status_html = status_color_tag(display_status)
        st.markdown(f"**#{p['id']} — {p['gix_course']}** &nbsp; | &nbsp; Status: {status_html}", unsafe_allow_html=True)
        with st.expander("View Details"):
            st.write(f"**Status:** {display_status}")
            for i, c in enumerate(p.get("courses", []), 1):
                st.write(f"**Course {i}:** {c['institution']} | Grade: {c.get('grade', 'N/A')} | Transcript: {c['transcript_filename']}, Syllabus: {c['syllabus_filename']}")
            if p.get("advisor_notes"):
                st.write(f"**Advisor Notes:** {p['advisor_notes']}")
            if p.get("instructor_notes"):
                st.write(f"**Instructor Notes:** {p['instructor_notes']}")


# --- Shared reviewer components ---

def display_pdf(label: str, file_path: str | None, filename: str, key: str) -> None:
    pdf_file = Path(file_path) if file_path else None
    if pdf_file and pdf_file.is_file():
        st.write(f"**{label}:** {filename}")
        pdf_bytes = pdf_file.read_bytes()
        st.download_button(f"Download {label}", data=pdf_bytes, file_name=filename, mime="application/pdf", key=key)
        pdf_b64 = base64.b64encode(pdf_bytes).decode()
        st.markdown(f'<iframe src="data:application/pdf;base64,{pdf_b64}" width="100%" height="500" type="application/pdf"></iframe>', unsafe_allow_html=True)
    else:
        st.caption(f"{label}: {filename or 'N/A'}")


def render_review_dashboard(role: str) -> None:
    """Shared review dashboard for advisor and instructor."""
    st.header("Petition Review Dashboard")
    all_petitions = load_petitions()

    if not all_petitions:
        st.info("No petitions submitted yet.")
        return

    # Filter: advisor sees all; instructor only sees "Advisor Approved"
    if role == "instructor":
        petitions = [p for p in all_petitions if p["status"] in [STATUS_ADVISOR_APPROVED, STATUS_APPROVED]]
    else:
        petitions = list(all_petitions)

    # Search
    search_col, btn_col = st.columns([9, 1])
    with search_col:
        search_query = st.text_input("🔍", placeholder="Search by UW NetID", label_visibility="collapsed", key=f"search_input_{role}")
    with btn_col:
        search_clicked = st.button("Search", type="primary", use_container_width=True, key=f"search_btn_{role}")

    search_key = f"search_term_{role}"
    if search_key not in st.session_state:
        st.session_state[search_key] = ""
    if search_clicked:
        st.session_state[search_key] = search_query
    search = st.session_state[search_key]

    st.write("")

    if search:
        petitions = [p for p in petitions if search.lower() in p.get("student_email", "").lower()]

    # Sort by time, newest first
    petitions = sorted(petitions, key=lambda x: x.get("submitted_at", ""), reverse=True)

    if not petitions:
        st.info("No petitions found.")
        return

    for i, p in enumerate(petitions):
        # Determine card state
        bg_color = card_bg_color(p, role)
        netid = p.get("student_email", "N/A")
        name = p.get("student_name", "N/A")
        status_html = status_color_tag(p["status"])

        # Card header with background color
        st.markdown(
            f'<div style="background-color:{bg_color}; padding:12px 16px; border-radius:8px; margin-bottom:4px;">'
            f'<strong>{netid}</strong> &nbsp; | &nbsp; <strong>{name}</strong> &nbsp; | &nbsp; {p["gix_course"]} &nbsp; | &nbsp; Status: {status_html}'
            f'</div>',
            unsafe_allow_html=True,
        )

        with st.expander("View & Review"):
            # Mark as viewed
            mark_as_viewed(all_petitions, p["id"], role)

            st.write(f"**UW NetID:** {p['student_email']}")
            st.write(f"**Student:** {p['student_name']}")
            st.write(f"**Program:** {p['program']}")
            st.write(f"**GIX Course:** {p['gix_course']}")
            st.write(f"**English Documents:** {p['is_english']}")
            st.write(f"**Submitted:** {p['submitted_at']}")

            st.divider()
            for j, c in enumerate(p.get("courses", []), 1):
                st.subheader(f"Course {j}")
                st.write(f"**Institution:** {c['institution']}")
                st.write(f"**Grade:** {c.get('grade', 'N/A')}")
                if c.get("notes"):
                    st.write(f"**Student Notes:** {c['notes']}")
                display_pdf("Transcript", c.get("transcript_path"), c.get("transcript_filename", "N/A"), key=f"dl_transcript_{role}_{i}_{j}")
                display_pdf("Syllabus", c.get("syllabus_path"), c.get("syllabus_filename", "N/A"), key=f"dl_syllabus_{role}_{i}_{j}")

            # Show existing notes from other reviewer
            if role == "instructor" and p.get("advisor_notes"):
                st.divider()
                st.write(f"**Advisor Notes:** {p['advisor_notes']}")

            if role == "advisor" and p.get("instructor_notes"):
                st.divider()
                st.write(f"**Instructor Notes:** {p['instructor_notes']}")

            # Decision section
            st.divider()
            st.subheader("Decision")

            notes_key = f"{role}_notes"

            if role == "advisor":
                # Advisor can approve (sends to instructor) or reject
                can_decide = p["status"] == STATUS_SUBMITTED
                if not can_decide:
                    st.info(f"This petition has already been processed. Current status: {p['status']}")
                else:
                    decision = st.radio(
                        "Your decision",
                        ["Approve (send to Instructor)", "Reject"],
                        index=None,
                        key=f"decision_advisor_{i}",
                    )
                    reviewer_notes = st.text_area("Advisor Notes", value=p.get("advisor_notes", ""), key=f"notes_advisor_{i}")

                    if st.button("Save Decision", key=f"save_advisor_{i}", type="primary"):
                        # Find the petition in all_petitions by id
                        for ap in all_petitions:
                            if ap["id"] == p["id"]:
                                ap["advisor_notes"] = reviewer_notes
                                if decision == "Approve (send to Instructor)":
                                    ap["status"] = STATUS_ADVISOR_APPROVED
                                elif decision == "Reject":
                                    ap["status"] = STATUS_REJECTED
                                break
                        save_petitions(all_petitions)
                        st.success("Decision saved!")
                        st.rerun()

            elif role == "instructor":
                # Instructor makes final decision on advisor-approved petitions
                can_decide = p["status"] == STATUS_ADVISOR_APPROVED
                if not can_decide:
                    st.info(f"This petition has already been decided. Current status: {p['status']}")
                else:
                    decision = st.radio(
                        "Your decision (final)",
                        ["Approve", "Reject"],
                        index=None,
                        key=f"decision_instructor_{i}",
                    )
                    reviewer_notes = st.text_area("Instructor Notes", value=p.get("instructor_notes", ""), key=f"notes_instructor_{i}")

                    if st.button("Save Decision", key=f"save_instructor_{i}", type="primary"):
                        for ap in all_petitions:
                            if ap["id"] == p["id"]:
                                ap["instructor_notes"] = reviewer_notes
                                if decision == "Approve":
                                    ap["status"] = STATUS_APPROVED
                                elif decision == "Reject":
                                    ap["status"] = STATUS_REJECTED
                                break
                        save_petitions(all_petitions)
                        st.success("Decision saved!")
                        st.rerun()


# --- Statistics ---

def render_statistics_page() -> None:
    st.header("Petition Statistics")
    petitions = load_petitions()

    if not petitions:
        st.info("No data yet.")
        return

    df = pd.DataFrame(petitions)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Petitions", len(df))
    col2.metric("Approved", len(df[df["status"] == STATUS_APPROVED]))
    col3.metric("Rejected", len(df[df["status"] == STATUS_REJECTED]))
    col4.metric("Pending", len(df[df["status"].isin([STATUS_SUBMITTED, STATUS_ADVISOR_APPROVED])]))

    st.subheader("Petitions by Status")
    status_counts = df["status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    fig_status = px.bar(
        status_counts, x="Status", y="Count",
        title="Petition Count by Status",
        color="Status",
        color_discrete_sequence=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
    )
    st.plotly_chart(fig_status, use_container_width=True)

    st.subheader("Petitions by GIX Course")
    course_counts = df["gix_course"].value_counts().reset_index()
    course_counts.columns = ["Course", "Count"]
    fig_course = px.bar(
        course_counts, x="Count", y="Course",
        title="Petition Count by GIX Course",
        orientation="h",
        color_discrete_sequence=["#1f77b4"],
    )
    fig_course.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_course, use_container_width=True)


# --- Main App ---
if not st.session_state.get("logged_in"):
    st.title("GIX Course Petition Tracker")
    render_login()
else:
    role = st.session_state["role"]
    if role == "student":
        st.title("GIX Course Petition Form")
    else:
        st.title("GIX Course Petition Tracker")
    render_logout()

    if role == "student":
        tab1, tab2 = st.tabs(["Submit Petition", "My Petitions"])
        with tab1:
            render_student_page_wrapper()
        with tab2:
            render_student_history()

    elif role == "advisor":
        tab1, tab2 = st.tabs(["Review Dashboard", "Statistics"])
        with tab1:
            render_review_dashboard("advisor")
        with tab2:
            render_statistics_page()

    elif role == "instructor":
        tab1, tab2 = st.tabs(["Review Dashboard", "Statistics"])
        with tab1:
            render_review_dashboard("instructor")
        with tab2:
            render_statistics_page()
