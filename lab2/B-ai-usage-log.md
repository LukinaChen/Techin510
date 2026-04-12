# Component B: AI Usage Log & Prompt Log

---

## Warm-up: Model Comparison

### Prompt Used (same for both tools)
```
Write a Python function that takes a list of student records (dictionaries with
"name", "program", and "gpa" keys) and returns only the students in a given
program with a GPA above a given threshold. Include error handling.
```

### Tool 1: Claude Code
```python
def filter_students(
    records: list[dict], program: str, gpa_threshold: float
) -> list[dict]:
    if not isinstance(records, list):
        raise TypeError("records must be a list")
    if not (0 <= gpa_threshold <= 4.0):
        raise ValueError("gpa_threshold must be between 0 and 4.0")

    results = []
    for student in records:
        if not isinstance(student, dict):
            continue
        if not all(key in student for key in ("name", "program", "gpa")):
            continue
        if student["program"] == program and student["gpa"] > gpa_threshold:
            results.append(student)
    return results
```

### Tool 2: ChatGPT
```python
def filter_students(records, program, min_gpa):
    if not isinstance(records, list):
        raise TypeError("records must be a list")
    if not isinstance(program, str):
        raise TypeError("program must be a string")
    if not isinstance(min_gpa, (int, float)):
        raise TypeError("min_gpa must be a number")

    filtered = []
    for i, record in enumerate(records):
        try:
            if not isinstance(record, dict):
                raise ValueError(f"Record at index {i} is not a dictionary")
            for key in ["name", "program", "gpa"]:
                if key not in record:
                    raise KeyError(f"Missing key '{key}' in record at index {i}")
            if not isinstance(record["gpa"], (int, float)):
                raise ValueError(f"GPA must be numeric in record at index {i}")
            if record["program"] == program and record["gpa"] > min_gpa:
                filtered.append(record)
        except Exception as e:
            print(f"Skipping invalid record at index {i}: {e}")
    return filtered
```

### Observations (2-3 differences)

1. **Code style**: Claude Code used type hints (`records: list[dict]`) and a concise style — invalid records are silently skipped with `continue`. ChatGPT did not use type hints but provided detailed error messages with index numbers (`f"Record at index {i}"`), making debugging easier.

2. **Error handling**: ChatGPT was more thorough — it validated the `program` parameter type, checked each record's GPA type individually, and wrapped each record in a try/except with `print()` logging. Claude Code only validated `records` type and `gpa_threshold` range, silently skipping bad records without logging.

3. **Explanation quality**: ChatGPT included a usage example with test data (including an invalid GPA case) showing expected output. Claude Code provided a cleaner docstring with Args/Returns/Raises sections but no usage example. ChatGPT's approach is more beginner-friendly; Claude Code's is more professional/library-style.

---

## Level 2: Three Cursor Modes (completed via Claude Code)

### Step 2.2: Composer/Agent — Add a Feature
- **Prompt**: "Add a Petition Statistics page with Plotly charts showing petition count by status and by GIX course"
- **Output**: Added `render_statistics_page()` with metric cards and two Plotly bar charts. Also added login system, file upload per course, and PDF preview for advisor.
- **What it did**: Generated a full statistics dashboard and multi-feature enhancement across the app.

### Step 2.3: Chat — Understand Code
- **Code selected**: PDF display code using `base64` + `iframe` in the reviewer dashboard
- **Question asked**: "Is `st.write(f"**Transcript:** {c['transcript_filename']}")` what displays the file?"
- **Answer**: No. That line only displays a bold text label showing the filename. The actual PDF rendering happens through these steps:
  1. `transcript_file.read_bytes()` — reads the PDF file into binary data
  2. `base64.b64encode(transcript_bytes).decode()` — converts the binary into a base64-encoded string, because HTML cannot embed raw binary data
  3. `st.markdown(f'<iframe src="data:application/pdf;base64,{transcript_b64}" ...></iframe>')` — this is the line that actually renders the PDF inline using an iframe with a data URL
  4. The `else` branch with `st.caption()` is the fallback when the file doesn't exist — it just shows a gray text label
- **Follow-up insight**: The `data:application/pdf;base64,...` pattern is a way to embed file content directly into HTML without needing a separate file URL. The browser's built-in PDF viewer handles the rendering inside the iframe.

### Step 2.4: Inline Edit — Refactor
- **Prompt**: "Extract the repeated PDF display code into a reusable function"
- **Output**: Created `display_pdf()` helper function, reducing duplicated transcript/syllabus display logic from ~20 lines to 2 function calls.
- **What it did**: Improved code maintainability without changing behavior.

---

## Information Hierarchy Review

### Squint Test — Top 3 Elements
1. Title: "GIX Course Petition Tracker"
2. Section header: "Submit a Course Petition"
3. Course subheaders (Course 1/2/3) and Submit button

### Evaluation
| Question | Answer |
|----------|--------|
| Most important info on the page? | The title and submission form |
| Is it the most visually prominent? | Yes |
| Can a first-time user understand the app? | Yes |
| Are related items grouped together? | Yes |
| Any element that draws attention but is not important? | No |

### Hierarchy Fix
- **Changed title by role**: Students see "GIX Course Petition Form", advisors see "GIX Course Petition Tracker" — clearer purpose for each audience.
- **Bolded all form field labels** (Your Name, UW Email, etc.) using CSS injection — labels were previously normal weight and blended with placeholder text, making the form harder to scan quickly.

---

## Prompt Engineering Log (Level 3)

### Spec (written before prompting)
1. **What should it do?** Advisor can search petitions by student UW NetID and visually distinguish reviewed vs. unreviewed petitions.
2. **What inputs does it take?** A UW NetID typed into a search box on the advisor dashboard.
3. **What should the output look like?** Filtered petition list sorted by time, with a ✓ mark on reviewed petitions, and bold NetID + student name on each card.

### Prompt 1 — Vague
- **Prompt**: "针对advisor的页面需要有个搜索框"
- **Output**: Added a basic `st.text_input("Search")` that filters by student name. No icon, no placeholder, no visual distinction for reviewed items, no empty-state handling.
- **What AI assumed**: Searched by name (not NetID), no styling, label said "Search", triggered on every keystroke.

### Prompt 2 — Specific
- **Prompt**: "搜索框上填学生的UW NetID. 搜索框在Petition Review Dashboard下面，它要有个搜索的标志icon(放大镜），需要与下面的dashboard要有点距离，去掉search的字样。已审核的要在方框的最右边有个打勾的icon（仅黑色线条），没有审核的就没有"
- **Output**: Added 🔍 icon with placeholder text, collapsed label, spacing below search box, ✓ mark on reviewed petitions. Searched by email field. Added empty-state message.
- **What improved**: Search field, placeholder, icon, reviewed indicator, spacing — all matched the spec more closely.

### Prompt 3 — Constrained
- **Prompt**: "搜索框现在只能按回车键才能搜索，要有一个圆角10的长方形的按钮在搜索框的最右边。✓要在每条的最右边，而不是紧紧跟在状态右边。之前的status的字要有，不要删除。每个提交的表单要展示先展示UW NetID然后student，这两个要在折叠的card里加粗，展开里面也都要有。｜左右的间距稍微增加一些。排列顺序按时间"
- **Output**: Added a "Search" button with rounded corners (10px), ✓ pushed to the right with spacing, Status label kept, NetID and student name shown bold in card header and inside expanded view, wider spacing around `|` separators, petitions sorted by submission time (newest first).
- **What improved**: Every visual detail specified was implemented — button style, ✓ positioning, card content order, bold formatting, spacing, sort order.

### Reflection on Progression
1. **Biggest difference**: Vague prompt produced a generic search box with wrong field and no styling. Constrained prompt produced exactly the UI described with correct data, styling, and interaction.
2. **What mattered most**: Behavior details (button vs. enter key) and visual layout (bold, spacing, icon position) had the biggest impact on output quality.
3. **AI assumptions vs. instructions**: In the vague prompt, ~90% of the result was AI assumptions. In the constrained prompt, ~90% came from explicit instructions.

