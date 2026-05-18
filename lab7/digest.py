"""
Skill 5: /digest — Generate a weekly summary of your knowledge base.
Run: python digest.py
"""
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta

KB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")


def load_kb():
    with open(KB_PATH, "r") as f:
        return json.load(f)


def digest(days=7):
    kb = load_kb()
    materials = kb["materials"]
    profile = kb["profile"]

    if not materials:
        print("Knowledge base is empty. Start adding materials with: python add_material.py \"<url>\"")
        return

    cutoff = datetime.now() - timedelta(days=days)
    recent = [
        m for m in materials
        if datetime.fromisoformat(m["created_at"]) >= cutoff
    ]

    print(f"\n=== Weekly Knowledge Digest ===")
    print(f"Period: last {days} days  |  User: {profile.get('name', 'Unknown')}")
    print(f"Total in knowledge base: {len(materials)}  |  Added this week: {len(recent)}")
    print("=" * 50)

    if not recent:
        print("\nNothing added this week.")
        all_categories = defaultdict(list)
        for m in materials:
            cat = m.get("category") or "Uncategorized"
            all_categories[cat].append(m)
        print(f"\nAll-time breakdown ({len(materials)} total):")
        for cat, items in sorted(all_categories.items()):
            print(f"  {cat}: {len(items)} item(s)")
        return

    by_category = defaultdict(list)
    for m in recent:
        cat = m.get("category") or "Uncategorized"
        by_category[cat].append(m)

    for category, items in sorted(by_category.items()):
        print(f"\n[{category}]  ({len(items)} new)")
        for m in items:
            date = m["created_at"][:10]
            tags = ", ".join(m.get("tags", [])) or "—"
            title = m["title"][:70]
            print(f"  • {title}")
            print(f"    Tags: {tags}  |  Added: {date}")

    uncategorized_total = sum(1 for m in materials if not m["categorized"])
    if uncategorized_total:
        print(f"\n  {uncategorized_total} uncategorized item(s) — run  python categorize.py  to organize them.")

    print(f"\nTip: run  python search.py \"<topic>\"  to dive deeper into any of these areas.")


if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    digest(days)
