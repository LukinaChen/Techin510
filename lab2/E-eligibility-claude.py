"""GIX Career Services — Quick Eligibility Checker (Claude Code implementation)."""

from datetime import datetime

import streamlit as st

st.set_page_config(page_title="GIX Eligibility Checker", page_icon="🎓")

st.title("GIX Career Events — Quick Eligibility Checker")
st.write("Check which career events you qualify for based on your program, graduation quarter, and CPT status.")

QUARTERS = [
    "Spring 2025", "Summer 2025", "Autumn 2025", "Winter 2026",
    "Spring 2026", "Summer 2026", "Autumn 2026", "Winter 2027",
    "Spring 2027", "Summer 2027",
]

CURRENT_QUARTER = "Spring 2026"


def quarters_until_graduation(grad_quarter):
    if grad_quarter not in QUARTERS or CURRENT_QUARTER not in QUARTERS:
        return 99
    return QUARTERS.index(grad_quarter) - QUARTERS.index(CURRENT_QUARTER)


program = st.selectbox("Your Program", ["-- Select --", "MSTI", "GIX PMP"])
grad_quarter = st.selectbox("Expected Graduation Quarter", ["-- Select --"] + QUARTERS)
cpt_status = st.radio("CPT Authorization Status", ["Yes", "No", "Pending"], index=None)

if st.button("Check Eligibility", type="primary"):
    if program == "-- Select --" or grad_quarter == "-- Select --" or cpt_status is None:
        st.error("Please fill in all fields.")
    else:
        st.divider()
        st.subheader("Your Eligibility Results")

        quarters_left = quarters_until_graduation(grad_quarter)
        graduating_this_quarter = quarters_left == 0

        # Human review flag
        if cpt_status == "Pending":
            st.warning("Your CPT status is pending. Please contact a career services advisor to confirm your eligibility for CPT-required events.")

        if graduating_this_quarter and cpt_status == "No":
            st.warning("You are graduating this quarter without CPT authorization. Please consult a career advisor for special arrangements.")

        # Event 1: Mock Interviews — within 2 quarters of graduation
        if quarters_left <= 2 and quarters_left >= 0:
            st.success("Mock Interviews — Eligible (graduating within 2 quarters)")
        else:
            st.error("Mock Interviews — Not Eligible (graduation is more than 2 quarters away)")

        # Event 2: Resume Reviews — all students
        st.success("Resume Reviews — Eligible (open to all students)")

        # Event 3: Employer Panels — requires CPT
        if cpt_status == "Yes":
            st.success("Employer Panels — Eligible (CPT authorized)")
        elif cpt_status == "Pending":
            st.info("Employer Panels — Pending Review (awaiting CPT confirmation)")
        else:
            st.error("Employer Panels — Not Eligible (CPT authorization required)")

        # Event 4: Networking Nights — all programs
        st.success("Networking Nights — Eligible (open to all programs)")
