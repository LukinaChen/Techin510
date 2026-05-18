"""
Skill 2: /add — Add a URL or text to your knowledge base.
Run: python add_material.py "<URL or text>"
"""
import json
import os
import sys
import uuid
from datetime import datetime

KB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")


def load_kb():
    with open(KB_PATH, "r") as f:
        return json.load(f)


def save_kb(data):
    with open(KB_PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def fetch_url_metadata(url):
    """Fetch title and a short description from a URL."""
    try:
        import urllib.request
        from html.parser import HTMLParser

        class MetaParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.title = ""
                self.description = ""
                self._in_title = False

            def handle_starttag(self, tag, attrs):
                attrs_dict = dict(attrs)
                if tag == "title":
                    self._in_title = True
                if tag == "meta":
                    name = attrs_dict.get("name", "").lower()
                    prop = attrs_dict.get("property", "").lower()
                    content = attrs_dict.get("content", "")
                    if name in ("description", "og:description") or prop in ("og:description",):
                        if not self.description:
                            self.description = content
                    if prop == "og:title" and not self.title:
                        self.title = content

            def handle_endtag(self, tag):
                if tag == "title":
                    self._in_title = False

            def handle_data(self, data):
                if self._in_title and not self.title:
                    self.title = data.strip()

        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        parser = MetaParser()
        parser.feed(html[:10000])

        title = parser.title or url
        description = parser.description or "No description available."
        return title[:200], description[:500]

    except Exception as e:
        return url, f"Could not fetch metadata: {e}"


def add_material(content):
    kb = load_kb()

    if not kb["profile"].get("name"):
        print("Profile not set up yet. Please run: python setup_profile.py")
        sys.exit(1)

    is_url = content.startswith("http://") or content.startswith("https://")

    if is_url:
        print(f"Fetching metadata from URL...")
        title, summary = fetch_url_metadata(content)
        material_type = "link"
    else:
        title = content[:80] + ("..." if len(content) > 80 else "")
        summary = content
        material_type = "note"

    material = {
        "id": str(uuid.uuid4())[:8],
        "type": material_type,
        "content": content,
        "title": title,
        "summary": summary,
        "category": None,
        "tags": [],
        "created_at": datetime.now().isoformat(),
        "categorized": False,
    }

    kb["materials"].append(material)
    save_kb(kb)

    uncategorized_count = sum(1 for m in kb["materials"] if not m["categorized"])

    print(f"\n✓ Added: {title}")
    print(f"  Type: {material_type}")
    print(f"  Summary: {summary[:120]}...")
    print(f"  Status: uncategorized")

    if uncategorized_count >= 3:
        print(f"\n  You have {uncategorized_count} uncategorized items.")
        print("  Tip: run  python categorize.py  to organize them.")
    else:
        print(f"\n  Total uncategorized: {uncategorized_count}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add_material.py \"<URL or text>\"")
        sys.exit(1)
    add_material(" ".join(sys.argv[1:]))
