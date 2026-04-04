# This app is a GIX Student Purchase Request System built with Streamlit.
# It allows GIX students to submit purchase requests by filling in a form
# with fields like item name, price, supplier, and quantity.
# Dorothy (Program Coordinator) can view all submissions on a separate page
# and update the approval status and add rejection notes for each request.
# I manually changed the submission instructions text in render_submit_page()
# to make it clearer for students what to expect after submitting.

"""GIX Student Purchase Request System — Streamlit app."""

import json
from pathlib import Path

import pandas as pd
import streamlit as st

APP_TITLE = "GIX Student Purchase Request System"
DATA_PATH = Path(__file__).resolve().parent / "purchase_requests.json"

STUDENT_FIELDS = [
    "Team Number",
    "CFO Name",
    "Provider / Supplier",
    "Quantity",
    "Name of Item",
    "Price in USD",
    "Link to Purchase",
    "Notes",
]

REQUEST_FIELDS = STUDENT_FIELDS + [
    "Instructor Approval Status",
    "Rejection Note",
]

APPROVAL_OPTIONS = ["Pending", "Approved", "Rejected"]

COORDINATOR_PANEL_CSS = """
<style>
    /* Coordinator panels — indigo-tinted to match theme */
    [class*="st-key-gix_coord_"] {
        background-color: #eef2ff !important;
        padding: 0.85rem 1rem 1rem 1rem;
        border-radius: 8px;
        border: 1px solid #c7d2fe !important;
        margin-bottom: 0.35rem;
    }
</style>
"""

# Theme tokens (match .streamlit/config.toml primary #6366f1)
_THEME_PRIMARY = "#6366f1"
_THEME_PRIMARY_HOVER = "#4f46e5"
_THEME_INPUT_BG = "#eef2ff"

# Visible borders + fill for form fields; Submit button matches primary.
# Use str.format (not f-string): CSS uses many `{`/`}` which f-strings treat as Python code.
FORM_FIELD_CSS = """
<style>
    :root {{
        --gix-input-border: {primary};
        --gix-input-bg: {input_bg};
        --gix-input-radius: 8px;
        --gix-primary: {primary};
        --gix-primary-hover: {primary_hover};
        --gix-control-min-height: 48px;
    }}
    /* Forms / vertical blocks: default overflow clips taller custom inputs */
    div[data-testid="stForm"],
    div[data-testid="stForm"] > div,
    div[data-testid="stForm"] [data-testid="stVerticalBlock"] {{
        overflow: visible !important;
        max-height: none !important;
    }}
    /* Full-width widgets (number_input steppers no longer squeeze the value cell) */
    div[data-testid="stForm"],
    div[data-testid="stTextInput"],
    div[data-testid="stNumberInput"],
    div[data-testid="stTextArea"],
    div[data-testid="stSelectbox"] {{
        width: 100% !important;
        max-width: 100% !important;
    }}
    div[data-testid="stTextInput"] > div,
    div[data-testid="stNumberInput"] > div,
    div[data-testid="stTextArea"] > div,
    div[data-testid="stSelectbox"] > div {{
        width: 100% !important;
        max-width: 100% !important;
        overflow: visible !important;
        max-height: none !important;
    }}
    /* Number input: grow wrappers so bordered row is not cut off at the bottom */
    div[data-testid="stNumberInput"],
    div[data-testid="stNumberInput"] > div {{
        overflow: visible !important;
        max-height: none !important;
        min-height: var(--gix-control-min-height) !important;
        height: auto !important;
    }}
    div[data-testid="stNumberInput"] [data-baseweb="input"] {{
        flex: 1 1 0% !important;
        min-width: 0 !important;
        min-height: var(--gix-control-min-height) !important;
        height: auto !important;
        overflow: visible !important;
        max-height: none !important;
        align-items: stretch !important;
    }}
    div[data-testid="stTextInput"] [data-baseweb="input"],
    div[data-testid="stSelectbox"] [data-baseweb="select"] {{
        width: 100% !important;
        min-width: 0 !important;
    }}
    div[data-testid="stTextInput"] div[data-baseweb="input"] > div {{
        border: 1px solid var(--gix-input-border) !important;
        border-radius: var(--gix-input-radius) !important;
        background-color: var(--gix-input-bg) !important;
        width: 100% !important;
        min-height: var(--gix-control-min-height) !important;
        box-sizing: border-box !important;
        align-items: center !important;
    }}
    div[data-testid="stTextInput"] input {{
        background-color: transparent !important;
        width: 100% !important;
        min-height: 42px !important;
        padding: 10px 14px !important;
        box-sizing: border-box !important;
        font-size: 1rem !important;
    }}
    div[data-testid="stNumberInput"] div[data-baseweb="input"] > div {{
        border: 1px solid var(--gix-input-border) !important;
        border-radius: var(--gix-input-radius) !important;
        background-color: var(--gix-input-bg) !important;
        width: 100% !important;
        min-width: 0 !important;
        min-height: var(--gix-control-min-height) !important;
        height: auto !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        overflow: visible !important;
        flex: 1 1 auto !important;
    }}
    div[data-testid="stNumberInput"] input {{
        background-color: transparent !important;
        width: 100% !important;
        min-width: 0 !important;
        min-height: 40px !important;
        padding: 8px 12px !important;
        box-sizing: border-box !important;
        font-size: 1rem !important;
        line-height: 1.35 !important;
    }}
    /* Hide "Press Enter to submit form" on number inputs (form uses enter_to_submit=False; backup) */
    div[data-testid="stNumberInput"] [data-testid="InputInstructions"] {{
        display: none !important;
    }}
    div[data-testid="stTextArea"] [data-baseweb="textarea"] {{
        width: 100% !important;
        min-width: 0 !important;
    }}
    div[data-testid="stTextArea"] div[data-baseweb="textarea"] > div {{
        border: 1px solid var(--gix-input-border) !important;
        border-radius: var(--gix-input-radius) !important;
        background-color: var(--gix-input-bg) !important;
        width: 100% !important;
        min-height: 140px !important;
        box-sizing: border-box !important;
    }}
    div[data-testid="stTextArea"] textarea {{
        background-color: transparent !important;
        width: 100% !important;
        min-height: 120px !important;
        padding: 12px 14px !important;
        box-sizing: border-box !important;
        font-size: 1rem !important;
        line-height: 1.5 !important;
    }}
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
        border: 1px solid var(--gix-input-border) !important;
        border-radius: var(--gix-input-radius) !important;
        background-color: var(--gix-input-bg) !important;
        width: 100% !important;
        min-height: var(--gix-control-min-height) !important;
        box-sizing: border-box !important;
        align-items: center !important;
    }}
    /* Bold widget labels (Streamlit wraps label text in child elements) */
    div[data-testid="stTextInput"] label,
    div[data-testid="stTextInput"] label *,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stNumberInput"] label *,
    div[data-testid="stTextArea"] label,
    div[data-testid="stTextArea"] label *,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stSelectbox"] label * {{
        font-weight: 700 !important;
    }}
    div[data-testid="stFormSubmitButton"] button {{
        background-color: var(--gix-primary) !important;
        border-color: var(--gix-primary) !important;
        color: #ffffff !important;
    }}
    div[data-testid="stFormSubmitButton"] button:hover {{
        background-color: var(--gix-primary-hover) !important;
        border-color: var(--gix-primary-hover) !important;
    }}
</style>
""".format(
    primary=_THEME_PRIMARY,
    input_bg=_THEME_INPUT_BG,
    primary_hover=_THEME_PRIMARY_HOVER,
)


def load_requests() -> list[dict]:
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def save_requests(rows: list[dict]) -> None:
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)


def normalize_request(row: dict) -> dict:
    out = dict(row)
    status = out.get("Instructor Approval Status")
    if status not in APPROVAL_OPTIONS:
        out["Instructor Approval Status"] = "Pending"
    note = out.get("Rejection Note")
    out["Rejection Note"] = "" if note is None else str(note)
    return out


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, layout="wide")

    st.markdown(FORM_FIELD_CSS, unsafe_allow_html=True)

    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Submit Request", "View All Requests"],
        label_visibility="collapsed",
    )

    st.title(f"**{APP_TITLE}**")

    if page == "Submit Request":
        render_submit_page()
    else:
        render_view_page()


def render_submit_page() -> None:
    st.header("**Submit Request**")
    st.subheader("**Student purchase form**")
    st.write(
        "Please fill in all fields carefully. Dorothy (Program Coordinator) will review "
        "your submission on **View All Requests** and update the approval status."
    )

    with st.form("purchase_request_form", clear_on_submit=True, enter_to_submit=False):
        team_number = st.text_input("**Team Number**", width="stretch")
        cfo_name = st.text_input("**CFO Name**", width="stretch")
        provider = st.text_input("**Provider / Supplier**", width="stretch")
        quantity = st.number_input("**Quantity**", min_value=0, value=1, step=1, width="stretch")
        item_name = st.text_input("**Name of Item**", width="stretch")
        price_usd = st.number_input(
            "**Price in USD**",
            min_value=0.0,
            value=0.0,
            step=0.01,
            format="%.2f",
            width="stretch",
        )
        purchase_link = st.text_input("**Link to Purchase**", width="stretch")
        notes = st.text_area("**Notes**", height=160, width="stretch")

        submitted = st.form_submit_button("Submit")

    if submitted:
        entry = {
            "Team Number": team_number.strip(),
            "CFO Name": cfo_name.strip(),
            "Provider / Supplier": provider.strip(),
            "Quantity": int(quantity),
            "Name of Item": item_name.strip(),
            "Price in USD": float(price_usd),
            "Link to Purchase": purchase_link.strip(),
            "Notes": notes.strip(),
            "Instructor Approval Status": "Pending",
            "Rejection Note": "",
        }
        rows = load_requests()
        rows.append(entry)
        save_requests(rows)
        st.success("Your purchase request was saved successfully.")


def render_view_page() -> None:
    st.header("**View All Requests**")
    st.subheader("**Coordinator dashboard**")
    st.markdown(COORDINATOR_PANEL_CSS, unsafe_allow_html=True)
    st.write(
        "Student data is read-only. **Instructor Approval Status** and **Rejection Note** "
        "sit in the highlighted panel on the right; changes are saved as soon as you update them."
    )

    rows = [normalize_request(r) for r in load_requests()]

    if not rows:
        st.info("No requests yet. Submissions will appear here after students use **Submit Request**.")
        return

    changed = False
    new_rows: list[dict] = []

    for i, row in enumerate(rows):
        st.divider()
        st.caption(f"Request **#{i + 1}**")
        data_col, edit_col = st.columns([2.4, 1], gap="medium")

        with data_col:
            st.markdown("##### **Student submission**")
            student_row = {k: row[k] for k in STUDENT_FIELDS}
            st.dataframe(
                pd.DataFrame([student_row]),
                hide_index=True,
                use_container_width=True,
            )

        with edit_col:
            with st.container(key=f"gix_coord_{i}", border=True):
                st.markdown("##### **Coordinator**")
                st.caption("Editable fields")
                idx = (
                    APPROVAL_OPTIONS.index(row["Instructor Approval Status"])
                    if row["Instructor Approval Status"] in APPROVAL_OPTIONS
                    else 0
                )
                st.selectbox(
                    "**Instructor Approval Status**",
                    options=APPROVAL_OPTIONS,
                    index=idx,
                    key=f"approval_{i}",
                    width="stretch",
                )
                st.text_area(
                    "**Rejection note**",
                    value=row["Rejection Note"],
                    height=160,
                    key=f"reject_note_{i}",
                    width="stretch",
                    help="Optional. Use when status is Rejected (or anytime you want to leave context).",
                )

        st_s = st.session_state[f"approval_{i}"]
        st_n = st.session_state[f"reject_note_{i}"]
        if not isinstance(st_n, str):
            st_n = str(st_n) if st_n is not None else ""

        old_s = row["Instructor Approval Status"]
        old_n = row["Rejection Note"]
        if st_s != old_s or st_n != old_n:
            changed = True

        updated = dict(row)
        updated["Instructor Approval Status"] = st_s
        updated["Rejection Note"] = st_n
        new_rows.append(updated)

    if changed:
        save_requests(new_rows)
        st.toast("Coordinator updates saved.", icon="✅")


if __name__ == "__main__":
    main()
