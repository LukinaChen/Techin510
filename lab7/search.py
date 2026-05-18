"""
Skill 4: /search — Search your knowledge base.
Run: python search.py "<query>"
"""
import json
import os
import sys

KB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")


def load_kb():
    with open(KB_PATH, "r") as f:
        return json.load(f)


def search_knowledge(query):
    kb = load_kb()
    materials = kb["materials"]

    if not materials:
        print("Knowledge base is empty. Add materials with: python add_material.py \"<url>\"")
        return

    query_lower = query.lower()
    query_words = query_lower.split()

    scored = []
    for m in materials:
        score = 0
        search_text = " ".join([
            m.get("title", ""),
            m.get("summary", ""),
            m.get("category", "") or "",
            " ".join(m.get("tags", [])),
            m.get("content", ""),
        ]).lower()

        for word in query_words:
            score += search_text.count(word)

        if score > 0:
            scored.append((score, m))

    scored.sort(key=lambda x: x[0], reverse=True)

    print(f"\n=== Search results for: \"{query}\" ===\n")

    if not scored:
        print("No results found.")
        print("Try different keywords, or check what's in your knowledge base with: python digest.py")
        return

    for rank, (score, m) in enumerate(scored[:10], 1):
        date = m["created_at"][:10]
        category = m.get("category") or "uncategorized"
        tags = ", ".join(m.get("tags", [])) or "none"
        title = m["title"]
        summary = m["summary"][:150]
        content_preview = m["content"][:80] if m["type"] == "link" else ""

        print(f"{rank}. {title}")
        print(f"   Category: {category}  |  Tags: {tags}  |  Added: {date}")
        print(f"   {summary}...")
        if content_preview:
            print(f"   URL: {content_preview}")
        print()

    print(f"Found {len(scored)} result(s).")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search.py \"<query>\"")
        sys.exit(1)
    search_knowledge(" ".join(sys.argv[1:]))
