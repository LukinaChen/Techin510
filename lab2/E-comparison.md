# Component E: Comparison & Testing

---

## Comparison Table

| Dimension | Claude Code | ChatGPT |
|-----------|------------|---------|
| **Code length** | ~60 lines, compact | ~180 lines, modular |
| **Architecture** | Single inline script, logic mixed with UI | Separated into helper functions (`parse_quarter`, `quarter_distance`, `evaluate_eligibility`, `render_status_label`) |
| **Type hints** | None | Full type hints on all functions with Tuple, List, Dict |
| **Docstrings** | None | Google-style docstrings with Args/Returns/Raises |
| **Error handling** | Basic — checks if fields are filled, shows `st.error()` | Comprehensive — validates program, CPT status, graduation quarter order; raises ValueError with descriptive messages; wraps in try/except |
| **UI framework** | No form — uses individual widgets + button | Uses `st.form()` with `st.form_submit_button()` |
| **Result display** | Uses `st.success()`, `st.error()`, `st.info()` — built-in Streamlit colors | Custom HTML badges with `render_status_label()` — styled spans with rounded pill shape and custom colors |
| **Human review handling** | Separate warning messages for CPT Pending and graduating-this-quarter edge cases | Flags "Human Review Required" as a third status category with yellow badge; consolidates warnings |
| **Quarter calculation** | Hardcoded list of quarters, index-based distance | Parsed quarter strings into (year, index) tuples, arithmetic-based distance — more flexible |
| **Input validation** | Checks for "-- Select --" placeholder | Validates via ValueError exceptions with specific error messages |

---

## Smoke Test

| Test | Claude Code | ChatGPT |
|------|------------|---------|
| App starts without error | Yes | Yes |
| Core path works (valid input → results displayed) | Yes | Yes |
| Invalid input does not crash | Yes — shows "Please fill in all fields" | Yes — shows error message from exception |

---

## Input Testing

### Valid Input
- **Input**: Program = MSTI, Graduation = Summer 2026, CPT = Yes
- **Claude Code result**: Mock Interviews: Eligible, Resume Reviews: Eligible, Employer Panels: Eligible, Networking Nights: Eligible
- **ChatGPT result**: Same — all four events show Eligible with green badges

### Invalid Input
- **Input**: Program = MSTI, Graduation = Spring 2026 (this quarter), CPT = No
- **Claude Code result**: Warning "You are graduating this quarter without CPT authorization. Please consult a career advisor." Mock Interviews: Eligible, Employer Panels: Not Eligible
- **ChatGPT result**: Warning messages for Mock Interviews and Employer Panels. Both show "Human Review Required" with yellow badge instead of auto-deciding

### Key Difference on Edge Case
ChatGPT's approach is more conservative — it refuses to auto-decide for edge cases and always flags them for human review. Claude Code still shows Eligible/Not Eligible for individual events but adds a warning banner. ChatGPT's approach better matches the spec requirement that edge cases "are flagged for human review rather than auto-decided."

---

## .cursorrules Impact

The existing `.cursorrules` file was already active for the Claude Code implementation. Key effects observed:
- Used Streamlit conventions (`st.set_page_config()` at top, `st.error()`/`st.warning()` for user messages)
- Used project color palette indirectly (Streamlit built-in colors)
- The .cursorrules did not significantly change the ChatGPT output since ChatGPT does not read local config files — it followed its own conventions (type hints, docstrings, modular functions) by default
