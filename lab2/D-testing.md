# Component D: Testing & Validation

---

## Prompt Regression Test Results

### Smoke Test

For each prompt output (with config), the following was verified:
- [x] It runs without errors
- [x] Core behavior works (statistics display, PDF rendering, JSON loading)
- [x] Invalid input is handled without crashing (empty data, corrupted JSON)

### Recording Template

| # | Prompt Used | Without Config (Before) | With Config (After) | What Changed | Better/Worse/Same |
|---|-------------|------------------------|--------------------|--------------|--------------------|
| 1 | "Add a statistics section to the reviewer dashboard" | Used Matplotlib, no type hints, no docstring | Used Plotly, Google-style docstring, added type hints, used project color palette | Switched to Plotly and added type hints per .cursorrules | Better |
| 2 | "Explain the display_pdf function step by step" | Generic explanation, no project context | Referenced advisor dashboard, uploads/ directory, and project conventions | Used project context from CLAUDE.md | Better |
| 3 | "Add error handling so the app doesn't crash if petitions.json is corrupted" | Bare except clause, no user message | Specific exception types, added st.warning() message and docstring | Followed Streamlit conventions from config | Better |

---

## Quality Gate Checklist

- [x] **Smoke test completed**: For each prompt output, confirmed (1) it runs, (2) core behavior works once, and (3) invalid input is handled without crashing
- [x] **3 prompts tested**: Recording template has 3 complete rows with before/after observations
- [x] **Differences are specific**: Each "What Changed" entry describes concrete, observable changes (e.g., "switched from Matplotlib to Plotly", "added type hints", "used specific exception types")
- [x] **Config files restored**: `.cursorrules` and `CLAUDE.md` files are back in place and verified working
- [x] **Honest assessment**: All 3 prompts showed improvement with config files — no "Same" results, which is accurate because the config files contain substantial project-specific conventions
- [x] **Prompts are documented**: Exact prompt text is recorded for reproducibility

---

## Testing Concept: Regression Testing

### What is a regression test?
A regression test re-runs existing tests after a change to ensure the change did not break previously working functionality. A "regression" is when something that worked before stops working due to a new change.

### How this applies to AI tools
- Configuration files (`.cursorrules`, `CLAUDE.md`) are inputs to AI tools, just like code is input to a compiler
- Changing these files can improve or regress the AI's output quality
- This exercise is a manual regression test: we ran the same prompts before and after adding config files to check whether the change was beneficial
- In professional settings, this would be automated — teams run the same prompts against different model versions or configurations and compare outputs systematically
