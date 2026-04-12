# Component A: Staff Interview Notes

## Guest: Jason Evans, Academic Student Counselor (ASC) — Course Petition Syllabus Reviews

---

## Interview Notes

### What Jason Does
Jason reviews course petition documents — transcripts and syllabi — to determine if a student's previous coursework qualifies to waive a UW GIX course.

### Current Workflow
1. **Students submit** via Zoho form: transcript + syllabus (up to 3 external courses to waive 1 GIX course)
2. **Jason does initial review** (basic criteria check):
   - Is the transcript in English? (must be official university translation with stamp, not self-translated or LLM-translated)
   - Can he open the files?
   - Is the correct course submitted? (not a math class for a design class, etc.)
   - Does the student's grade meet the 2.7 minimum GPA requirement?
   - Highlights the relevant course on the transcript
3. **Jason compiles documents** — combines transcript + syllabus into one package per student
4. **Sends to course instructor** for expert review:
   - Instructor compares learning outcomes, deliverables, course level (needs UW 400+ equivalent)
   - 90% of learning outcomes must match the GIX course
   - Instructor gives approval/denial with notes
5. **Jason communicates results** back to students
6. **Edge cases**: one-on-one meetings with student and/or instructor if borderline

### Key Details
- Students can submit up to **3 courses** to waive **1 GIX course**
- **90% match** required on learning outcomes
- Comparison criteria: learning outcomes, deliverables, institution, course level, project vs. exam format
- Comparison method: word by word, keyword matching, understanding regional vocabulary differences
- **Credit limit**: students cannot waive more than allowed credits; must maintain 10 credits minimum per year
- **GIX syllabi change yearly** — need updated syllabus each year for comparison
- Documents kept for **5 cohorts**
- Timeline: ~1 month to review hundreds of syllabi and transcripts (e.g., early Oct to mid-Nov)
- Instructors given ~2 weeks to review; Jason sometimes has to send reminders
- Jason prioritizes by quarter (winter quarter courses first)

### Systems Used
- Zoho form for submissions
- Email for communications
- Spreadsheet for tracking approvals
- Multiple email systems set up for different response types

### LLM Experience
- Tried ChatGPT for syllabus comparison — not helpful
- Too generic, didn't provide detailed analysis of learning outcomes
- Just listed keywords without comparing specifics like projects vs. exams

---

## Emotional Journey

### Frustration Peaks (RED)
- **Emailing students one by one** for follow-ups: wrong format, not in English, self-translated, can't open files, missing documents
- **Students combining transcript and syllabus into one file** or submitting only one document instead of all required documents separately
- **Manually combining documents** — students submit transcript and each syllabus separately, Jason has to compile them all together, very time-consuming
- **Reviewing hundreds of syllabi takes hours and hours** — enormous volume during petition season
- **Mistyped student email addresses** in form submissions, requiring manual lookup

### Delight Moments (GREEN)
- **When students highlight the relevant course on their transcript** — saves Jason significant time
- **Clear-cut cases** where learning outcomes obviously match or obviously don't — quick decisions
- **When official English translations are provided** with university stamp — smooth process

### Uncertainty Zones (YELLOW)
- **Borderline cases** where learning outcomes partially match — requires instructor judgment and sometimes one-on-one meetings
- **Cross-disciplinary comparisons** (e.g., CNC machining vs. 3D printing) — Jason is not a subject matter expert, must rely on instructors
- **Regional vocabulary differences** — same concept, different terms across countries
- **When students submit more petitions than credits allow** — requires individual discussion about which to keep
- **Yearly syllabus changes** at GIX — need to update comparison baseline each year

---

## Problem Statement

"When Jason needs to review course petition syllabi for equivalency, he currently manually compiles documents, compares them word by word, and emails students individually for corrections, which causes hours of repetitive work and communication overhead during a compressed review timeline."

---

## Flowchart

See flowchart below (text-based representation):

```
[Student submits via Zoho form]
        |
        v
[Jason receives submission] --- (FRUSTRATION: mistyped emails, can't open files)
        |
        v
[Check: Documents complete?] --NO--> [Email student individually] --- (FRUSTRATION: one-by-one emails)
        |                                      |
       YES                                     v
        |                              [Student resubmits]
        v                                      |
[Check: Transcript in English?] --NO--> [Email student: need official    
        |                                university translation]        
       YES                               --- (FRUSTRATION: self-translated / LLM translated)
        |
        v
[Check: GPA >= 2.7?] --NO--> [Reject: does not meet minimum] 
        |
       YES
        |
        v
[Check: Credits within limit?] --NO--> [One-on-one meeting with student]
        |                                --- (UNCERTAINTY: which courses to keep?)
       YES
        |
        v
[Jason highlights course on transcript]
--- (DELIGHT: when student pre-highlights it)
        |
        v
[Compile transcript + syllabi into one package] --- (FRUSTRATION: time-consuming manual work)
        |
        v
[Check: Obviously wrong course type?] --YES--> [Reject: e.g., math class for design class]
(e.g., math for design)
        |
       NO / Plausible match
        |
        v
[Send compiled package to course instructor]
        |
        v
[Instructor reviews: 90% learning outcome match?]
--- (UNCERTAINTY: regional vocabulary, cross-discipline nuance)
        |
    /       \
  YES        NO
   |          |
   v          v
[Approved]  [Instructor adds notes on gaps]
   |          |
   |          v
   |    [Borderline?] --YES--> [One-on-one meeting: student + instructor]
   |          |                 --- (UNCERTAINTY: partial match cases)
   |         NO
   |          |
   v          v
[Jason emails result to student]
        |
        v
[Documents archived (kept for 5 cohorts)]
```

Color Code:
- RED = Frustration peaks
- GREEN = Delight moments  
- YELLOW = Uncertainty zones
