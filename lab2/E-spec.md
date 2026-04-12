# Component E: GIX Career Services — Quick Eligibility Checker

---

## 5-Sentence Specification

1. The Quick Eligibility Checker is a Streamlit web app that determines which GIX career events a student qualifies for based on their program, graduation quarter, and CPT (Curricular Practical Training) authorization status.
2. The student inputs their program (MSTI or GIX PMP), expected graduation quarter (e.g., Spring 2026, Summer 2026), and whether they have CPT authorization (Yes / No / Pending).
3. The app evaluates eligibility for four career events: Mock Interviews, Resume Reviews, Employer Panels, and Networking Nights, each with different qualification criteria.
4. The output displays a clear list of events with "Eligible" or "Not Eligible" labels, color-coded green or red, along with a brief reason for each decision.
5. Edge cases — such as students with pending CPT status or those graduating in the current quarter — are flagged for human review by a career services advisor rather than auto-decided by the tool.

---

## Decision Flowchart

```
[Student enters: Program, Graduation Quarter, CPT Status]
                    |
                    v
        ┌───────────────────────┐
        │ Is Program valid?     │
        │ (MSTI or GIX PMP)     │
        └───────┬───────────────┘
                |
           YES  |  NO → Display error: "Please select a valid program"
                |
                v
        ┌───────────────────────┐
        │ Check CPT Status      │
        └───────┬───────────────┘
                |
        ┌───────┼───────────────┐
        |       |               |
       YES    PENDING           NO
        |       |               |
        |       v               |
        |   ⚠ HUMAN REVIEW     |
        |   "CPT pending —      |
        |    contact advisor"   |
        |                       |
        v                       v
   ┌─────────────┐      ┌──────────────────┐
   │ CPT = Yes   │      │ CPT = No         │
   │             │      │                  │
   │ Check each  │      │ Limited access   │
   │ event:      │      │ to events        │
   └──────┬──────┘      └────────┬─────────┘
          |                      |
          v                      v
  ┌───────────────────────────────────────────────────────────┐
  │                    EVENT ELIGIBILITY                       │
  │                                                           │
  │  1. Mock Interviews                                       │
  │     └─ Graduating within 2 quarters? ──YES──► Eligible    │
  │                                        NO───► Not Eligible│
  │                                                           │
  │  2. Resume Reviews                                        │
  │     └─ All students ─────────────────────────► Eligible   │
  │                                                           │
  │  3. Employer Panels                                       │
  │     └─ Has CPT authorization? ─────────YES──► Eligible    │
  │                                        NO───► Not Eligible│
  │                                                           │
  │  4. Networking Nights                                     │
  │     └─ All programs ─────────────────────────► Eligible   │
  │                                                           │
  │  ⚠ HUMAN REVIEW step:                                    │
  │     └─ Graduating THIS quarter + CPT = No?                │
  │        → Flag: "Consult career advisor for               │
  │          special arrangements"                            │
  │                                                           │
  └───────────────────────────────────────────────────────────┘
                          |
                          v
              [Display results to student]
```

### Decision Branches:
1. **CPT Status**: Yes → full access | No → limited access | Pending → human review
2. **Graduation timing**: Within 2 quarters → eligible for Mock Interviews | Otherwise → not eligible
3. **Graduating this quarter + no CPT**: → flagged for human review (edge case)

### Human Review Annotations:
- **CPT Pending**: Student should contact career services advisor to confirm CPT status before accessing CPT-required events
- **Graduating this quarter with no CPT**: Advisor should determine if special accommodations are needed
