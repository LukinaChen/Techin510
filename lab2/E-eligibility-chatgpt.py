import streamlit as st
from typing import Dict, List, Tuple

st.set_page_config(page_title="GIX Career Events — Quick Eligibility Checker", page_icon="🎓")


# -----------------------------
# Helpers
# -----------------------------
QUARTER_ORDER = ["Winter", "Spring", "Summer", "Autumn"]


def parse_quarter(quarter_str: str) -> Tuple[int, int]:
    """
    Parse a quarter string like 'Spring 2026' into a sortable tuple.
    Returns (year, quarter_index).

    Raises:
        ValueError: If the format is invalid.
    """
    if not isinstance(quarter_str, str):
        raise TypeError("Quarter must be a string in the format 'Spring 2026'.")

    parts = quarter_str.strip().split()
    if len(parts) != 2:
        raise ValueError("Quarter must be in the format 'Spring 2026'.")

    quarter_name, year_str = parts
    if quarter_name not in QUARTER_ORDER:
        raise ValueError(
            f"Invalid quarter name '{quarter_name}'. Use one of: {', '.join(QUARTER_ORDER)}."
        )

    try:
        year = int(year_str)
    except ValueError as e:
        raise ValueError("Year must be a valid number, e.g. 2026.") from e

    return year, QUARTER_ORDER.index(quarter_name)


def quarter_distance(current_q: str, expected_grad_q: str) -> int:
    """
    Return how many quarters away expected_grad_q is from current_q.
    0 means this quarter, 1 means next quarter, etc.

    Raises:
        ValueError: If either quarter string is invalid.
    """
    current_year, current_idx = parse_quarter(current_q)
    grad_year, grad_idx = parse_quarter(expected_grad_q)

    return (grad_year - current_year) * 4 + (grad_idx - current_idx)


def evaluate_eligibility(
    program: str,
    expected_grad_q: str,
    cpt_status: str,
    current_q: str,
) -> Tuple[List[Dict[str, str]], List[str]]:
    """
    Evaluate eligibility for the four events.

    Business rules:
    - Mock Interviews: eligible if graduating within 2 quarters.
    - Resume Reviews: all students eligible.
    - Employer Panels: requires CPT authorization.
    - Networking Nights: all programs eligible.
    - If CPT is Pending OR student is graduating this quarter with no CPT,
      flag for human review instead of auto-deciding where relevant.

    Returns:
        results: list of event dictionaries with event + status
        warnings: list of human review warnings
    """
    if program not in {"MSTI", "GIX PMP"}:
        raise ValueError("Program must be 'MSTI' or 'GIX PMP'.")

    if cpt_status not in {"Yes", "No", "Pending"}:
        raise ValueError("CPT status must be 'Yes', 'No', or 'Pending'.")

    distance = quarter_distance(current_q, expected_grad_q)
    warnings = []
    results = []

    if distance < 0:
        raise ValueError("Expected graduation quarter cannot be earlier than the current quarter.")

    review_needed = cpt_status == "Pending" or (distance == 0 and cpt_status == "No")

    # Mock Interviews
    if review_needed:
        mock_status = "Human Review Required"
        warnings.append(
            "Mock Interviews requires human review because CPT is pending "
            "or the student is graduating this quarter without CPT authorization."
        )
    else:
        mock_status = "Eligible" if distance <= 2 else "Not Eligible"

    # Resume Reviews
    resume_status = "Eligible"

    # Employer Panels
    if review_needed:
        employer_status = "Human Review Required"
        warnings.append(
            "Employer Panels requires human review because CPT is pending "
            "or the student is graduating this quarter without CPT authorization."
        )
    else:
        employer_status = "Eligible" if cpt_status == "Yes" else "Not Eligible"

    # Networking Nights
    networking_status = "Eligible"

    results.append({"event": "Mock Interviews", "status": mock_status})
    results.append({"event": "Resume Reviews", "status": resume_status})
    results.append({"event": "Employer Panels", "status": employer_status})
    results.append({"event": "Networking Nights", "status": networking_status})

    # Deduplicate warnings
    warnings = list(dict.fromkeys(warnings))
    return results, warnings


def render_status_label(status: str) -> str:
    """
    Return an HTML badge for status.
    """
    color_map = {
        "Eligible": "#d1fae5",
        "Not Eligible": "#fee2e2",
        "Human Review Required": "#fef3c7",
    }
    text_color_map = {
        "Eligible": "#065f46",
        "Not Eligible": "#991b1b",
        "Human Review Required": "#92400e",
    }

    bg = color_map.get(status, "#e5e7eb")
    fg = text_color_map.get(status, "#111827")

    return f"""
        <span style="
            background-color: {bg};
            color: {fg};
            padding: 0.3rem 0.7rem;
            border-radius: 999px;
            font-weight: 600;
            font-size: 0.9rem;
        ">
            {status}
        </span>
    """


# -----------------------------
# App UI
# -----------------------------
st.title("GIX Career Events — Quick Eligibility Checker")
st.write("Enter student details to check event eligibility.")

with st.form("eligibility_form"):
    program = st.selectbox("Program", ["MSTI", "GIX PMP"])
    current_quarter = st.selectbox(
        "Current Quarter",
        [
            "Winter 2026",
            "Spring 2026",
            "Summer 2026",
            "Autumn 2026",
            "Winter 2027",
        ],
        index=1,
    )
    expected_grad_quarter = st.selectbox(
        "Expected Graduation Quarter",
        [
            "Spring 2026",
            "Summer 2026",
            "Autumn 2026",
            "Winter 2027",
            "Spring 2027",
            "Summer 2027",
        ],
        index=1,
    )
    cpt_status = st.selectbox("CPT Authorization Status", ["Yes", "No", "Pending"])

    submitted = st.form_submit_button("Check Eligibility")

if submitted:
    try:
        results, warnings = evaluate_eligibility(
            program=program,
            expected_grad_q=expected_grad_quarter,
            cpt_status=cpt_status,
            current_q=current_quarter,
        )

        if warnings:
            for warning in warnings:
                st.warning(warning)

        st.subheader("Eligibility Results")

        for item in results:
            col1, col2 = st.columns([3, 2])
            with col1:
                st.write(f"**{item['event']}**")
            with col2:
                st.markdown(render_status_label(item["status"]), unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")
