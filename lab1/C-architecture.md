## Component C: System Architecture & Design 
```
+----------------------+    +----------------------+    +----------------------+
|        INPUT         | -> |       PROCESS        | -> |       OUTPUT         |
+----------------------+    +----------------------+    +----------------------+
| - Team Number        |    | - Python collects    |    | - Success message    |
| - CFO Name           |    |   and validates data |    |   shown to student   |
| - Supplier           |    | - Saved to JSON file |    | - Table of requests  |
| - Quantity           |    | - Reads JSON on load |    |   shown to Dorothy   |
| - Item Name          |    | - Overwrites JSON    |    | - Editable Approval  |
| - Price in USD       |    |   when Dorothy edits |    |   Status & Note      |
| - Link to Purchase   |    |                      |    | - Toast notification |
| - Notes              |    |                      |    |   when saved         |
| - Submit button      |    |                      |    |                      |
| - Dorothy: Approval  |    |                      |    |                      |
| - Dorothy: Note      |    |                      |    |                      |
+----------------------+    +----------------------+    +----------------------+
         ^                                                       |
         +------ Feedback: Dorothy updates, student resubmits --+
```

## Design Decision Log

| Field | Your Entry |
|-------|------------|
| **Decision** | Put everything in one file (app.py) |
| **Alternatives considered** | Split into multiple files: data.py for JSON logic, ui.py for pages, main.py as entry point |
| **Why you chose this** | Cursor generated a single file by default. With ~385 lines it is still manageable for a first version |
| **Trade-off** | If 5 more features are added, the file could grow to 600+ lines and become very hard to navigate and debug |
| **When would you choose differently?** | If the app grows significantly or needs multiple people working on different parts at the same time |
