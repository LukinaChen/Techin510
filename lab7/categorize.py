"""
Skill 3: /categorize — Use Claude AI to categorize uncategorized materials.
Run: python categorize.py
Requires: ANTHROPIC_API_KEY in environment or .env file
"""
import json
import os
import sys

KB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")


def load_kb():
    with open(KB_PATH, "r") as f:
        return json.load(f)


def save_kb(data):
    with open(KB_PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def categorize_materials():
    try:
        import anthropic
    except ImportError:
        print("anthropic package not found. Run: pip install anthropic")
        sys.exit(1)

    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY not set. Add it to your .env file or environment.")
        sys.exit(1)

    kb = load_kb()
    uncategorized = [m for m in kb["materials"] if not m["categorized"]]

    if not uncategorized:
        print("No uncategorized materials found. Add some with: python add_material.py \"<url>\"")
        return

    profile = kb["profile"]
    categories = profile.get("preferred_categories", [])
    interests = profile.get("interests", [])
    career_goals = profile.get("career_goals", "")

    print(f"\n=== Categorizing {len(uncategorized)} materials ===\n")

    items_text = "\n".join(
        f"{i+1}. Title: {m['title']}\n   Summary: {m['summary'][:200]}"
        for i, m in enumerate(uncategorized)
    )

    prompt = f"""You are a personal knowledge management assistant helping to categorize learning materials.

User profile:
- Career goals: {career_goals}
- Interests: {', '.join(interests)}
- Preferred categories: {', '.join(categories)}

Materials to categorize:
{items_text}

For each material, assign it to one of the preferred categories (or suggest a new one if none fit).
Also generate 2-3 relevant tags.

Respond in this exact JSON format (array of objects):
[
  {{
    "index": 1,
    "category": "category name",
    "tags": ["tag1", "tag2"]
  }}
]

Only return the JSON array, no other text."""

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    response_text = message.content[0].text.strip()

    if response_text.startswith("```"):
        lines = response_text.split("\n")
        response_text = "\n".join(lines[1:-1])

    results = json.loads(response_text)

    for result in results:
        idx = result["index"] - 1
        if 0 <= idx < len(uncategorized):
            material_id = uncategorized[idx]["id"]
            for m in kb["materials"]:
                if m["id"] == material_id:
                    m["category"] = result["category"]
                    m["tags"] = result.get("tags", [])
                    m["categorized"] = True
                    break

    save_kb(kb)

    print(f"{'#':<4} {'Category':<20} {'Tags':<30} {'Title'}")
    print("-" * 80)
    for i, result in enumerate(results):
        title = uncategorized[i]["title"][:35]
        tags = ", ".join(result.get("tags", []))
        print(f"{i+1:<4} {result['category']:<20} {tags:<30} {title}")

    print(f"\n✓ Categorized {len(results)} materials.")
    print("Next: run  python digest.py  for a summary, or  python search.py \"<query>\"  to find something.")


if __name__ == "__main__":
    categorize_materials()
