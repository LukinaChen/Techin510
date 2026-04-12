# Component C: System Architecture & Design

---

## C.1 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        YOUR CODE (you own this)                     │
│                                                                     │
│  ┌──────────┐   ┌──────────────┐   ┌────────────┐   ┌───────────┐ │
│  │ app.py   │   │ petitions    │   │ uploads/   │   │ .streamlit│ │
│  │          │   │ .json        │   │ (PDFs)     │   │ config    │ │
│  │ - Login  │   │              │   │            │   │ .toml     │ │
│  │ - Student│◄─►│ Data storage │   │ File       │   │           │ │
│  │ - Advisor│   │ (read/write) │   │ storage    │   │ Theme     │ │
│  │ - Instr. │   │              │   │            │   │ settings  │ │
│  │ - Stats  │   └──────────────┘   └────────────┘   └───────────┘ │
│  └────┬─────┘                                                       │
│       │                                                             │
└───────┼─────────────────────────────────────────────────────────────┘
        │
 ═══════╪═══════════════════ BOUNDARIES ══════════════════════════════
        │
        ▼
┌───────────────────────────────────────────────────────────────────┐
│                    EXTERNAL LIBRARIES (you call them)             │
│                                                                   │
│  ┌───────────┐   ┌──────────┐   ┌──────────┐   ┌──────────────┐ │
│  │ Streamlit │   │ Plotly   │   │ Pandas   │   │ Python std   │ │
│  │           │   │          │   │          │   │ lib (json,   │ │
│  │ UI render │   │ Charts   │   │ DataFrames│  │ pathlib,     │ │
│  │ Widgets   │   │ Graphs   │   │ Analysis │   │ base64, etc.)│ │
│  │ State mgmt│   │          │   │          │   │              │ │
│  └───────────┘   └──────────┘   └──────────┘   └──────────────┘ │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘

 ═══════════════════════════ BOUNDARIES ══════════════════════════════

┌───────────────────────────────────────────────────────────────────┐
│               AI TOOLS (they propose, you decide)                 │
│                                                                   │
│  ┌─────────────┐          ┌──────────────┐                       │
│  │ Claude Code │          │ Cursor       │                       │
│  │             │          │              │                       │
│  │ Reads:      │          │ Reads:       │                       │
│  │ - CLAUDE.md │          │ - .cursorrules│                      │
│  │ - All files │          │ - All files  │                       │
│  │             │          │              │                       │
│  │ Generates   │          │ Generates    │                       │
│  │ code/answers│          │ code/answers │                       │
│  └─────────────┘          └──────────────┘                       │
│                                                                   │
│  Config boundary: .cursorrules and CLAUDE.md are YOUR             │
│  instructions to THEIR system. You control the input;             │
│  they control the processing.                                     │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘

 ═══════════════════════════ BOUNDARIES ══════════════════════════════

┌───────────────────────────────────────────────────────────────────┐
│            EXTERNAL SERVICES (you push/pull, they host)           │
│                                                                   │
│  ┌──────────────┐          ┌──────────────────┐                  │
│  │ GitHub       │          │ Browser          │                  │
│  │              │          │                  │                  │
│  │ Code hosting │          │ Renders the      │                  │
│  │ Version ctrl │          │ Streamlit app    │                  │
│  │ Collaboration│          │ User interaction │                  │
│  └──────────────┘          └──────────────────┘                  │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Student (browser)
    │
    ▼
[Streamlit UI] ──── st.text_input, st.file_uploader ────►  [app.py logic]
                                                                │
                                                    ┌───────────┼───────────┐
                                                    ▼           ▼           ▼
                                              petitions.json  uploads/   st.session_state
                                                    │                       │
                                                    ▼                       ▼
                                            [Advisor opens]         [Login state,
                                                    │                form state]
                                                    ▼
                                            [Advisor decides]
                                                    │
                                            Approve? ──YES──► [Instructor sees it]
                                                │                      │
                                               NO                     ▼
                                                │              [Instructor decides]
                                                ▼                      │
                                          Status: Rejected    Approve/Reject
                                                               │
                                                               ▼
                                                        Status: Approved
                                                        or Rejected
                                                               │
                                                               ▼
                                                    [Student sees result]
```

---

## C.2 Design Decision Log

### Decision 1: Where should project context live?

| Field | Entry |
|-------|-------|
| **Decision** | Put project context in both `.cursorrules` and `CLAUDE.md`, with each tailored to its respective tool. Specific, one-time instructions go directly in prompts. |
| **Alternatives considered** | (1) Only use `.cursorrules` for everything. (2) Only use prompts, no config files. (3) Put identical content in both files. |
| **Why I chose this** | `.cursorrules` is read by Cursor; `CLAUDE.md` is read by Claude Code. Each tool has different capabilities, so the context should be tailored. Prompts are for task-specific instructions that don't need to persist. Putting coding standards and business logic in config files means I don't have to repeat them in every prompt. |
| **Trade-off** | Maintaining two files means I have to update both when the project changes. If they go out of sync, one tool might generate code that contradicts the other. |
| **When would I choose differently?** | If I were only using one AI tool, I would only maintain one config file. If the project were very small (a single script), I would skip config files entirely and rely on prompts. |

### What happens when config and prompt conflict?

If `.cursorrules` says "use Plotly" but a prompt says "use Matplotlib", the **prompt wins** because it is the most recent, most specific instruction. Config files set defaults; prompts override them for specific tasks.

### What belongs where?

| Information | Where it belongs | Why |
|-------------|-----------------|-----|
| Coding standards (type hints, docstrings) | `.cursorrules` / `CLAUDE.md` | Applies to all code generation, should not be repeated |
| Project structure and tech stack | `.cursorrules` / `CLAUDE.md` | Stable context that rarely changes |
| Business logic (approval flow, roles) | `.cursorrules` / `CLAUDE.md` | Critical rules the AI must always follow |
| "Add a search bar to the advisor page" | Prompt | One-time task, not a persistent rule |
| "Use Matplotlib instead of Plotly for this chart" | Prompt | Exception to the default, task-specific |
| Run commands (`streamlit run app.py`) | `CLAUDE.md` only | Claude Code can run commands; Cursor cannot |

### Cost of maintaining context in multiple places

Maintaining context in both files has a small ongoing cost: when the project evolves (e.g., adding the instructor role), both files need updating. However, the benefit is significant — consistent AI output without repeating instructions. The risk of staleness is real but manageable for a course project of this size.
