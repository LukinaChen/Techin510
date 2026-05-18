"""
Skill 1: /setup — Configure your personal profile.
Run: python setup_profile.py
"""
import json
import os

KB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")


def load_kb():
    with open(KB_PATH, "r") as f:
        return json.load(f)


def save_kb(data):
    with open(KB_PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def setup_profile():
    kb = load_kb()

    print("\n=== Personal Knowledge Curator OS — Profile Setup ===\n")

    name = input("What's your name? ").strip()
    career_goals = input("What are your career goals or areas of focus? (e.g., UX design, AI research, product management)\n> ").strip()

    print("\nWhat topics interest you? Enter them one by one. Press Enter on an empty line when done.")
    interests = []
    while True:
        item = input(f"  Interest {len(interests)+1}: ").strip()
        if not item:
            break
        interests.append(item)

    print("\nWhat category names do you prefer? These will be used to organize your materials.")
    print("Examples: Design, Technology, Career, Research, Health, Finance, Personal")
    print("Press Enter on an empty line when done.")
    categories = []
    while True:
        cat = input(f"  Category {len(categories)+1}: ").strip()
        if not cat:
            break
        categories.append(cat)

    if not categories:
        categories = ["Design", "Technology", "Career", "Research", "Personal"]
        print(f"\nNo categories entered. Using defaults: {', '.join(categories)}")

    kb["profile"] = {
        "name": name,
        "interests": interests,
        "career_goals": career_goals,
        "preferred_categories": categories,
    }
    save_kb(kb)

    print(f"\n✓ Profile saved for {name}!")
    print(f"  Interests: {', '.join(interests) if interests else 'none set'}")
    print(f"  Categories: {', '.join(categories)}")
    print("\nNext step: run  python add_material.py \"<URL or text>\"  to start adding materials.")


if __name__ == "__main__":
    setup_profile()
