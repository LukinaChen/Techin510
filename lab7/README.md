# Lab 7: Personal Knowledge Curator — Agentic OS

## What is the purpose of this Agentic OS?

**Personal Knowledge Curator** is an AI-powered knowledge management system built as an Agentic OS. Its purpose is to solve a universal problem for students and knowledge workers:

> You collect lots of great articles, links, and notes — but they pile up in a disorganized mess, and when you actually need something, you can't find it.

This OS acts as an intelligent personal librarian: you throw materials at it (URLs, notes, lecture summaries), and it automatically organizes them based on *your* interests and career goals using Claude AI. Later, when you need something, you can search and retrieve it instantly.

---

## How does this Agentic OS address my need?

As a UW MSTI student, I regularly encounter:
- Interesting articles I want to save but never revisit
- Lecture notes scattered across different tools
- Resources I can't find when writing papers or preparing for interviews

This OS addresses these needs through 5 chained skills:

| Pain Point | Skill That Solves It |
|---|---|
| Hard to capture materials quickly | `/add` — one command to save any URL or text |
| Don't know how to categorize | `/categorize` — Claude AI auto-assigns categories based on your profile |
| Forget what you've collected | `/digest` — weekly summary grouped by topic |
| Can't find something specific | `/search` — full-text search across all materials |
| Categories don't match my life | `/setup` — personalized categories from your own career goals |

---

## Skills Enabled in this Agentic OS

### Skill 1: `/setup` — Profile Configuration
**File:** `setup_profile.py`

Asks you for your name, career goals, interests, and preferred category names. Saves this profile to `knowledge_base.json`. All subsequent AI categorization is personalized to this profile.

### Skill 2: `/add` — Add a Material
**File:** `add_material.py`

Accepts a URL or plain text. For URLs, it automatically fetches the page title and meta description. Stores the item as `uncategorized` until `/categorize` is run.

```bash
python add_material.py "https://nngroup.com/articles/mental-models/"
python add_material.py "Note from today: design systems need tokens for scalability"
```

### Skill 3: `/categorize` — AI-Powered Batch Categorization
**File:** `categorize.py`

Reads all uncategorized items and sends them to Claude (claude-opus-4-7) along with your profile. Claude assigns each item to the best-matching category and generates tags. This is the core AI skill that makes the system intelligent.

```bash
python categorize.py
```

### Skill 4: `/search` — Search Knowledge Base
**File:** `search.py`

Full-text search across titles, summaries, categories, tags, and content. Returns ranked results. No AI needed — fast local search.

```bash
python search.py "design systems"
python search.py "machine learning interview"
```

### Skill 5: `/digest` — Weekly Review
**File:** `digest.py`

Generates a digest of everything added in the last 7 days (configurable), grouped by category. Helps you remember what you learned and spot gaps.

```bash
python digest.py       # last 7 days
python digest.py 14    # last 14 days
```

---

## How Skills Collaborate and Chain for Complex Tasks

### Chain 1: First-Time Setup
```
/setup → /add → /categorize
```
You first configure your profile with your interests, then add materials, then run AI categorization. The profile from `/setup` directly powers the AI in `/categorize` — without it, categorization is generic; with it, it's personalized.

### Chain 2: Daily Capture Workflow
```
/add → /add → /add → /categorize
```
Throughout the day, quickly add anything interesting. At the end of the day, run one `/categorize` to batch-organize everything. This is more efficient than categorizing one item at a time.

### Chain 3: Weekly Learning Review
```
/digest → /search
```
On Sunday, run `/digest` to see what you collected all week. When a category looks interesting, run `/search` to deep-dive into specific items from that topic.

### Chain 4: Full Weekly Loop
```
Mon–Fri: /add (capture as you browse)
Friday:  /categorize (organize the week)
Sunday:  /digest (review and reflect)
Anytime: /search (retrieve on demand)
```

These four skills form a **feedback loop**: the more you add, the more organized your knowledge becomes, and the more valuable `/search` and `/digest` become over time.

---

## How to Start the Project

### Prerequisites
- Python 3.8+
- An Anthropic API key (get one at [console.anthropic.com](https://console.anthropic.com))

### Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up your API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 3. Configure your personal profile
python setup_profile.py

# 4. Add some materials
python add_material.py "https://www.nngroup.com/articles/mental-models/"
python add_material.py "Interesting note: AI agents need memory to be useful"

# 5. Categorize with AI
python categorize.py

# 6. Search your knowledge base
python search.py "mental models"

# 7. Generate your weekly digest
python digest.py
```

### Project Structure

```
lab7/
├── CLAUDE.md           # Agentic OS configuration — defines agent identity and skills
├── README.md           # This file
├── knowledge_base.json # Your personal knowledge store (auto-created/updated)
├── setup_profile.py    # Skill 1: Configure your profile
├── add_material.py     # Skill 2: Add a URL or note
├── categorize.py       # Skill 3: AI batch categorization
├── search.py           # Skill 4: Search your knowledge base
├── digest.py           # Skill 5: Weekly review digest
├── requirements.txt    # Python dependencies
└── .env.example        # API key template
```
