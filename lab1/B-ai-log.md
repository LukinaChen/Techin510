## Warm-up: Tool Awareness Comparison

**App idea:** A simple purchase request form for GIX students 
with fields for item name, price, and supplier.

**Plain English description:**
"Build a simple Streamlit app for GIX students to submit 
purchase requests with fields for item name, price, and supplier."

**Claude (chatbot) result:**
Claude generated code as a text block in the chat window. 
I would need to manually create a new file, copy-paste the code, 
and save it myself. The code worked but required extra steps 
to actually use it.

**Cursor result:**
Cursor directly created app.py in my project folder, wrote 
the code into the file, and even ran a verification command. 
No copy-pasting needed — the file was ready to run immediately.

**Comparison:**
Cursor feels more "buildable" because it acts directly on 
the project files. A chatbot gives you code as text, which 
is useful for understanding but requires manual steps to deploy. 
Cursor skips those steps and behaves more like a coding assistant 
than a text generator.

---

# Component B: AI Usage Log

## Interaction 1 — Build the base app
**Prompt:** Build a Streamlit app called "GIX Student Purchase 
Request System" that helps GIX students submit purchase requests 
and allows Dorothy (Program Coordinator) to track them. The app 
should have two pages: Submit Request (a form with all required 
fields) and View All Requests (a table showing all submissions).

**What AI produced:** Created app.py with two-page navigation 
using st.sidebar, a complete submission form with all 9 fields, 
and a dataframe view of all requests. Data is saved to 
purchase_requests.json.

**Did it work first try?** Yes, app ran successfully on first try.

---

## Interaction 2 — Fix Approval Status ownership
**Prompt:** Update the app so that on the Submit Request page, 
remove the Instructor Approval Status field. All new submissions 
automatically get status "Pending". On the View All Requests page, 
add a dropdown next to each request that lets Dorothy change the 
approval status.

**What AI produced:** Removed the field from the student form, 
set default status to "Pending", added editable dropdown on the 
coordinator view.

**Did it work first try?** Yes.

---

## Interaction 3 — Add Rejection Note and visual distinction
**Prompt:** Add a Rejection Note text field next to the approval 
status for each request. Make Dorothy's editable fields visually 
distinct with a light blue background so she can clearly see 
which fields she can edit.

**What AI produced:** Added a blue-background "Coordinator" panel 
on the right side of each request with editable Approval Status 
dropdown and Rejection Note text area, clearly separated from the 
read-only student submission table on the left.

**Did it work first try?** Yes.

---

## Interaction 4 — Style with Themes (Level 5)
**Prompt:** Create a .streamlit/config.toml file with a 
professional indigo theme, white background, and sans-serif font.

**What AI produced:** Created .streamlit/config.toml with custom 
colors. Had to fix a NameError (border syntax error in app.py) 
and a layout issue with the Price in USD field.

**Did it work first try?** No. Got a NameError on line 68 of 
app.py. Fixed by pasting the error back to Cursor. Also had to 
fix input field width display issue.

---

## Interaction 5 — Manual Code Edit (Level 4)
**Prompt:** No AI used. Manually edited the submission 
instructions text in render_submit_page().

**What I changed:** Changed "Fill in the details below" to 
"Please fill in all fields carefully" to make instructions 
clearer for students.

**Did it work?** Yes, app ran successfully after the change.

---

## Level 4: Code Understanding

**Function I studied:** render_submit_page()

**My understanding in my own words:**
The render_submit_page() function draws all the form inputs on 
the page and waits for the user to click Submit. Only when 
submitted is True does it save the data to the JSON file.

---

## Accessibility Baseline Check

**Color Contrast:** PASS
- Text color: rgb(49, 51, 63)
- Background color: rgb(255, 255, 255)
- Contrast ratio exceeds 4.5:1 standard (WCAG AA)
- Using Streamlit default theme, no custom colors needed

**Semantic Headings:** PASS
- st.title() used once for main page title
- st.header() used for major sections
- st.subheader() used for subsections
- Heading order is correct, no levels skipped

---

## Reflection

**1. What surprised you about AI-assisted coding?**
I was surprised by how quickly Cursor completed the entire app. 
It not only generated the code but directly created and edited 
the files in my project folder, which felt very different from 
just getting a text response from a chatbot.

**2. What did the AI get wrong?**
Sometimes the visual layout was slightly off — for example, 
input fields were not displaying at full width, and the initial 
color theme looked unprofessional. Some features also didn't 
match real user habits, like having the approval status on the 
student form instead of the coordinator dashboard.

**3. Could you explain your code?**
For most parts, yes. After studying render_submit_page(), I 
understood how Streamlit draws form inputs and only saves data 
when the Submit button is clicked. There are still some advanced 
parts I would need more time to fully understand.

**4. What did you learn from the interview?**
Understanding the user's needs is crucial — it directly shaped 
what features to build and what to prioritize. Without talking 
to Dorothy, I might have built a generic form that missed key 
details like the instructor approval workflow and the volume 
of requests she handles each month.