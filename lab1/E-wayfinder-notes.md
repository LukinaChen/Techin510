# Component E: GIX Campus Wayfinder

## Part 1: I/P/O Diagram
```
+----------------------+    +----------------------+    +----------------------+
|        INPUT         | -> |       PROCESS        | -> |       OUTPUT         |
+----------------------+    +----------------------+    +----------------------+
| - User types keyword |    | - Filter RESOURCES   |    | - Resource cards     |
|   in search bar      |    |   list by category   |    |   showing name,      |
|                      |    | - Filter by search   |    |   category,          |
| - User selects       |    |   keyword (checks    |    |   location, hours,   |
|   category from      |    |   name and           |    |   description,       |
|   sidebar dropdown   |    |   description)       |    |   free to use        |
|   (All, Makerspace,  |    | - If no filters,     |    |                      |
|   Study Space,       |    |   show all 8         |    | - Results count      |
|   Printing,          |    |   resources          |    |   ("X found")        |
|   Storage, Food,     |    |                      |    |                      |
|   Other)             |    |                      |    | - Warning message    |
|                      |    |                      |    |   if no results      |
+----------------------+    +----------------------+    +----------------------+
         ^                                                       |
         +---- Feedback: User refines search or changes --------+
                          category filter
```

### Data Source
RESOURCES = hardcoded list of 8 dictionaries in E-wayfinder.py 

## Part 2: Edge Case Validation

### Edge Case 1: Empty search bar
**What happens:** When the search bar is empty and category 
is "All", all 8 resources are shown.
**Why it matters:** The app should not crash or show 0 results 
when no search term is entered. This is the default state 
every user sees when they first open the app.
**Result:** Pass — all 8 resources display correctly with 
empty search.

### Edge Case 2: Search term with no matches
**What happens:** When user types a keyword that matches 
no resource (e.g. "swimming pool"), the app shows a warning 
message instead of crashing.
**Why it matters:** Users will inevitably search for things 
that don't exist. The app must handle this gracefully instead 
of showing a blank page with no explanation.
**Result:** Pass — warning message "No resources match your 
search" appears correctly.

---

## Part 3: Assert Statement
Located in F-wayfinder.py at the top of the file:
```python
assert all(
    REQUIRED_FIELDS.issubset(r.keys()) for r in RESOURCES
), "Some resources are missing required fields!"
```

This checks that every resource in the list has all 6 required 
fields (name, category, location, hours, description, free).

---

## Part 4: Prompt Log

### Initial Prompt
"Create a new file called wayfinder.py. Build a Streamlit app 
called GIX Campus Wayfinder that helps new GIX students find 
campus resources. Include a data structure with 8 resources, 
a search bar, category filter, resource cards, and an assert 
statement for data integrity."

### Refinement
"Add a search button next to the search bar so users can click 
to search instead of only pressing Enter. The button should have 
a search icon so users immediately know what it does."

**What changed and why:** The initial prompt generated a plain 
text input where users could only search by pressing Enter — 
this is not intuitive for all users. Adding a clickable 🔍 Search 
button makes the interaction clearer and more user-friendly, 
especially for users who are not familiar with pressing Enter 
to submit a search.