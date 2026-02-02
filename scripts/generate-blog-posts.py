"""
Generate blog-posts.json from YAML front matter in posts/*.md files.

This script scans all markdown files in the posts/ directory, extracts
YAML front matter metadata, and writes a blog-posts.json manifest.

Run manually:   python scripts/generate-blog-posts.py
Or via GitHub Actions on every push that changes posts/*.md
"""

import os
import json
import re
import glob
import sys


def parse_front_matter(filepath):
    """Extract YAML front matter from a markdown file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        return None

    # Find the closing ---
    end = content.find("---", 3)
    if end == -1:
        return None

    raw = content[3:end].strip()
    meta = {}
    current_key = None
    list_values = []

    for line in raw.split("\n"):
        # List item (e.g. "  - Tag One")
        list_match = re.match(r"^\s+-\s+(.+)$", line)
        if list_match and current_key:
            list_values.append(list_match.group(1).strip())
            meta[current_key] = list_values
            continue

        # Key-value pair (e.g. "title: Some Title")
        kv_match = re.match(r"^(\w[\w\s]*?):\s*(.*)$", line)
        if kv_match:
            current_key = kv_match.group(1).strip()
            value = kv_match.group(2).strip()
            if value:
                meta[current_key] = value
                list_values = []
            else:
                # Key with no inline value means a list follows
                list_values = []
            continue

    return meta


def main():
    # Resolve paths relative to repo root
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    posts_dir = os.path.join(repo_root, "posts")
    output_file = os.path.join(repo_root, "blog-posts.json")

    md_files = sorted(glob.glob(os.path.join(posts_dir, "*.md")))

    posts = []
    for filepath in md_files:
        basename = os.path.basename(filepath)

        # Skip template file
        if basename.upper().startswith("TEMPLATE"):
            continue

        meta = parse_front_matter(filepath)
        if meta is None:
            print(f"  Skipping {basename} (no front matter found)")
            continue

        # Derive post ID from filename
        post_id = os.path.splitext(basename)[0]

        post = {
            "id": post_id,
            "title": meta.get("title", ""),
            "subtitle": meta.get("subtitle", ""),
            "category": meta.get("category", ""),
            "date": str(meta.get("date", "")),
            "readTime": meta.get("readTime", ""),
            "excerpt": meta.get("excerpt", ""),
            "markdownFile": f"posts/{basename}",
            "tags": meta.get("tags", []),
        }

        posts.append(post)
        print(f"  Found: {post['title']} ({post['date']})")

    # Sort by date descending (newest first)
    posts.sort(key=lambda p: p["date"], reverse=True)

    manifest = {"posts": posts}

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"\nGenerated blog-posts.json with {len(posts)} post(s)")


if __name__ == "__main__":
    main()
