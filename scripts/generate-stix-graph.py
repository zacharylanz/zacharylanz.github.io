"""
Generate data/stix-graph.json from HTML source files + overrides.

Parses experience.html, portfolio.html, and index.html to extract
entities (organizations, certifications, tools, etc.), merges them
with hand-maintained overrides (descriptions, extra nodes, label
overrides), and writes a JSON file consumed by stix-graph.html.

Run manually:   python scripts/generate-stix-graph.py
Or via GitHub Actions on pushes that change source HTML files.
"""

import json
import os
import re
from datetime import datetime, timezone
from html.parser import HTMLParser


# ---------------------------------------------------------------------------
# HTML Parsers (stdlib HTMLParser, SAX-style)
# ---------------------------------------------------------------------------

class ExperienceParser(HTMLParser):
    """Parse experience.html for organizations, education, and teaching."""

    def __init__(self):
        super().__init__()
        self.orgs = []
        self.education = []
        self.teaching = []

        self._in_company = False
        self._in_edu_card = 0        # depth counter
        self._in_edu_h4 = False
        self._in_teach_card = 0      # depth counter
        self._in_teach_h4 = False
        self._in_teach_org = False
        self._current_teach = {}
        self._text = ""

    def handle_starttag(self, tag, attrs):
        classes = dict(attrs).get("class", "")

        if tag == "span" and "company" in classes.split():
            self._in_company = True
            self._text = ""
        elif tag == "div" and "education-card" in classes.split():
            self._in_edu_card = 1
        elif tag == "div" and self._in_edu_card > 0:
            self._in_edu_card += 1
        elif tag == "h4" and self._in_edu_card > 0:
            self._in_edu_h4 = True
            self._text = ""
        elif tag == "div" and "teaching-card" in classes.split():
            self._in_teach_card = 1
            self._current_teach = {}
        elif tag == "div" and self._in_teach_card > 0:
            self._in_teach_card += 1
        elif tag == "h4" and self._in_teach_card > 0:
            self._in_teach_h4 = True
            self._text = ""
        elif tag == "p" and "teach-org" in classes.split() and self._in_teach_card > 0:
            self._in_teach_org = True
            self._text = ""

    def handle_data(self, data):
        if self._in_company or self._in_edu_h4 or self._in_teach_h4 or self._in_teach_org:
            self._text += data

    def handle_endtag(self, tag):
        if tag == "span" and self._in_company:
            text = self._text.strip()
            if text:
                self.orgs.append(text)
            self._in_company = False
        elif tag == "h4" and self._in_edu_h4:
            text = self._text.strip()
            if text:
                self.education.append(text)
            self._in_edu_h4 = False
        elif tag == "div" and self._in_edu_card > 0:
            self._in_edu_card -= 1
        elif tag == "h4" and self._in_teach_h4:
            self._current_teach["title"] = self._text.strip()
            self._in_teach_h4 = False
        elif tag == "p" and self._in_teach_org:
            self._current_teach["org"] = self._text.strip()
            self._in_teach_org = False
        elif tag == "div" and self._in_teach_card > 0:
            self._in_teach_card -= 1
            if self._in_teach_card == 0 and self._current_teach.get("org"):
                self.teaching.append(self._current_teach)


class PortfolioParser(HTMLParser):
    """Parse portfolio.html for certs, publications, awards, and frameworks."""

    def __init__(self):
        super().__init__()
        self.certs = []
        self.publications = []
        self.awards = []
        self.frameworks = []

        self._in_cert_card = 0
        self._in_cert_h4 = False
        self._in_pub_card = 0
        self._is_award_card = False
        self._in_pub_h4 = False
        self._in_frameworks_card = 0
        self._in_skill_badge = False
        self._in_skill_card = 0
        self._skill_card_title = ""
        self._text = ""

    def handle_starttag(self, tag, attrs):
        classes = dict(attrs).get("class", "")
        class_list = classes.split()

        if tag == "div" and "cert-card" in class_list:
            self._in_cert_card = 1
        elif tag == "div" and self._in_cert_card > 0:
            self._in_cert_card += 1
        elif tag == "h4" and self._in_cert_card > 0:
            self._in_cert_h4 = True
            self._text = ""
        elif tag == "div" and "publication-card" in class_list:
            self._in_pub_card = 1
            self._is_award_card = "award-card" in class_list
        elif tag == "div" and self._in_pub_card > 0:
            self._in_pub_card += 1
        elif tag == "h4" and self._in_pub_card > 0:
            self._in_pub_h4 = True
            self._text = ""
        elif tag == "div" and "skill-detailed-card" in class_list:
            self._in_skill_card = 1
            self._skill_card_title = ""
        elif tag == "div" and self._in_skill_card > 0:
            self._in_skill_card += 1
        elif tag == "h4" and self._in_skill_card > 0 and not self._skill_card_title:
            self._in_cert_h4 = False  # reuse flag carefully
            self._text = ""
            self._reading_skill_title = True
        elif tag == "span" and "skill-badge" in class_list and self._in_skill_card > 0:
            self._in_skill_badge = True
            self._text = ""

    def handle_data(self, data):
        if self._in_cert_h4 or self._in_pub_h4 or self._in_skill_badge:
            self._text += data
        elif hasattr(self, '_reading_skill_title') and self._reading_skill_title:
            self._text += data

    def handle_endtag(self, tag):
        if tag == "h4" and self._in_cert_h4:
            text = self._text.strip()
            if text:
                self.certs.append(text)
            self._in_cert_h4 = False
        elif tag == "div" and self._in_cert_card > 0:
            self._in_cert_card -= 1
        elif tag == "h4" and self._in_pub_h4:
            text = self._text.strip()
            if text:
                if self._is_award_card:
                    self.awards.append(text)
                else:
                    self.publications.append(text)
            self._in_pub_h4 = False
        elif tag == "div" and self._in_pub_card > 0:
            self._in_pub_card -= 1
        elif tag == "h4" and hasattr(self, '_reading_skill_title') and self._reading_skill_title:
            self._skill_card_title = self._text.strip()
            self._reading_skill_title = False
        elif tag == "span" and self._in_skill_badge:
            text = self._text.strip()
            if text and self._skill_card_title == "Frameworks & Standards":
                self.frameworks.append(text)
            self._in_skill_badge = False
        elif tag == "div" and self._in_skill_card > 0:
            self._in_skill_card -= 1


class IndexParser(HTMLParser):
    """Parse index.html for tools from the about-tools section."""

    def __init__(self):
        super().__init__()
        self.tools = []

        self._in_about_tools = 0
        self._in_skill_badge = False
        self._text = ""

    def handle_starttag(self, tag, attrs):
        classes = dict(attrs).get("class", "")
        class_list = classes.split()

        if tag == "div" and "about-tools" in class_list:
            self._in_about_tools = 1
        elif tag == "div" and self._in_about_tools > 0:
            self._in_about_tools += 1
        elif tag == "span" and "skill-badge" in class_list and self._in_about_tools > 0:
            self._in_skill_badge = True
            self._text = ""

    def handle_data(self, data):
        if self._in_skill_badge:
            self._text += data

    def handle_endtag(self, tag):
        if tag == "span" and self._in_skill_badge:
            text = self._text.strip()
            if text:
                self.tools.append(text)
            self._in_skill_badge = False
        elif tag == "div" and self._in_about_tools > 0:
            self._in_about_tools -= 1


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def slugify(text):
    """Convert text to a URL-friendly slug for node IDs."""
    s = text.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')


def make_node_id(prefix, name, id_map):
    """Get a stable node ID from the id_map, or auto-generate one."""
    if name in id_map:
        return id_map[name]
    return f"{prefix}-{slugify(name)}"


def get_label(node_id, original_name, label_overrides):
    """Get display label: use override if present, otherwise original name."""
    return label_overrides.get(node_id, original_name)


def get_description(node_id, original_name, descriptions):
    """Get description: use override if present, otherwise generate default."""
    if node_id in descriptions:
        return descriptions[node_id]
    return f"{original_name} \u2014 part of the professional CTI toolkit and experience."


def parse_html_file(filepath, parser_class):
    """Read an HTML file and parse it with the given parser."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    parser = parser_class()
    parser.feed(content)
    return parser


# ---------------------------------------------------------------------------
# Main generation logic
# ---------------------------------------------------------------------------

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    overrides_path = os.path.join(repo_root, "data", "stix-graph-overrides.json")
    output_path = os.path.join(repo_root, "data", "stix-graph.json")

    # Load overrides
    with open(overrides_path, "r", encoding="utf-8") as f:
        overrides = json.load(f)

    id_map = overrides.get("id_map", {})
    label_overrides = overrides.get("label_overrides", {})
    descriptions = overrides.get("descriptions", {})
    skip_from_tools = set(overrides.get("skip_from_tools", []))
    extra_nodes = overrides.get("extra_nodes", {})
    categories = overrides.get("categories", {})
    identity = overrides.get("identity", {})

    # ---- Parse HTML files ----
    exp_path = os.path.join(repo_root, "experience.html")
    port_path = os.path.join(repo_root, "portfolio.html")
    idx_path = os.path.join(repo_root, "index.html")

    exp = parse_html_file(exp_path, ExperienceParser)
    port = parse_html_file(port_path, PortfolioParser)
    idx = parse_html_file(idx_path, IndexParser)

    print(f"  Parsed experience.html: {len(exp.orgs)} orgs, {len(exp.education)} edu, {len(exp.teaching)} teaching")
    print(f"  Parsed portfolio.html: {len(port.certs)} certs, {len(port.publications)} pubs, {len(port.awards)} awards, {len(port.frameworks)} frameworks")
    print(f"  Parsed index.html: {len(idx.tools)} tools")

    # ---- Build category children ----
    output_categories = {}

    # Organizations (timeline + teaching)
    org_children = []
    seen_ids = set()

    for name in exp.orgs:
        node_id = make_node_id("org", name, id_map)
        if node_id not in seen_ids:
            seen_ids.add(node_id)
            org_children.append({
                "id": node_id,
                "label": get_label(node_id, name, label_overrides),
                "description": get_description(node_id, name, descriptions)
            })

    for teach in exp.teaching:
        org_name = teach.get("org", "")
        node_id = make_node_id("org", org_name, id_map)
        if node_id not in seen_ids:
            seen_ids.add(node_id)
            org_children.append({
                "id": node_id,
                "label": get_label(node_id, org_name, label_overrides),
                "description": get_description(node_id, org_name, descriptions)
            })

    if "cat-org" in categories:
        cat = categories["cat-org"]
        output_categories["cat-org"] = {
            "label": cat["label"],
            "group": cat["group"],
            "edge_label": cat["edge_label"],
            "description": cat.get("description", ""),
            "children": org_children
        }

    # Tools (filtered: skip items that are frameworks)
    tool_children = []
    seen_ids.clear()

    for name in idx.tools:
        if name in skip_from_tools:
            continue
        node_id = make_node_id("tool", name, id_map)
        if node_id not in seen_ids:
            seen_ids.add(node_id)
            tool_children.append({
                "id": node_id,
                "label": get_label(node_id, name, label_overrides),
                "description": get_description(node_id, name, descriptions)
            })

    if "cat-tool" in categories:
        cat = categories["cat-tool"]
        output_categories["cat-tool"] = {
            "label": cat["label"],
            "group": cat["group"],
            "edge_label": cat["edge_label"],
            "description": cat.get("description", ""),
            "children": tool_children
        }

    # Certifications
    cert_children = []
    seen_ids.clear()

    for name in port.certs:
        node_id = make_node_id("cert", name, id_map)
        if node_id not in seen_ids:
            seen_ids.add(node_id)
            cert_children.append({
                "id": node_id,
                "label": get_label(node_id, name, label_overrides),
                "description": get_description(node_id, name, descriptions)
            })

    if "cat-cert" in categories:
        cat = categories["cat-cert"]
        output_categories["cat-cert"] = {
            "label": cat["label"],
            "group": cat["group"],
            "edge_label": cat["edge_label"],
            "description": cat.get("description", ""),
            "children": cert_children
        }

    # Frameworks (deduplicates via id_map, e.g., ICD203 + ICD206 → fw-icd203)
    fw_children = []
    seen_ids.clear()

    for name in port.frameworks:
        node_id = make_node_id("fw", name, id_map)
        if node_id not in seen_ids:
            seen_ids.add(node_id)
            fw_children.append({
                "id": node_id,
                "label": get_label(node_id, name, label_overrides),
                "description": get_description(node_id, name, descriptions)
            })

    if "cat-framework" in categories:
        cat = categories["cat-framework"]
        output_categories["cat-framework"] = {
            "label": cat["label"],
            "group": cat["group"],
            "edge_label": cat["edge_label"],
            "description": cat.get("description", ""),
            "children": fw_children
        }

    # Publications
    pub_children = []
    seen_ids.clear()

    for name in port.publications:
        node_id = make_node_id("pub", name, id_map)
        if node_id not in seen_ids:
            seen_ids.add(node_id)
            pub_children.append({
                "id": node_id,
                "label": get_label(node_id, name, label_overrides),
                "description": get_description(node_id, name, descriptions)
            })

    if "cat-pub" in categories:
        cat = categories["cat-pub"]
        output_categories["cat-pub"] = {
            "label": cat["label"],
            "group": cat["group"],
            "edge_label": cat["edge_label"],
            "description": cat.get("description", ""),
            "children": pub_children
        }

    # Awards
    award_children = []
    seen_ids.clear()

    for name in port.awards:
        node_id = make_node_id("award", name, id_map)
        if node_id not in seen_ids:
            seen_ids.add(node_id)
            award_children.append({
                "id": node_id,
                "label": get_label(node_id, name, label_overrides),
                "description": get_description(node_id, name, descriptions)
            })

    if "cat-award" in categories:
        cat = categories["cat-award"]
        output_categories["cat-award"] = {
            "label": cat["label"],
            "group": cat["group"],
            "edge_label": cat["edge_label"],
            "description": cat.get("description", ""),
            "children": award_children
        }

    # Education
    edu_children = []
    seen_ids.clear()

    for name in exp.education:
        node_id = make_node_id("edu", name, id_map)
        if node_id not in seen_ids:
            seen_ids.add(node_id)
            edu_children.append({
                "id": node_id,
                "label": get_label(node_id, name, label_overrides),
                "description": get_description(node_id, name, descriptions)
            })

    if "cat-edu" in categories:
        cat = categories["cat-edu"]
        output_categories["cat-edu"] = {
            "label": cat["label"],
            "group": cat["group"],
            "edge_label": cat["edge_label"],
            "description": cat.get("description", ""),
            "children": edu_children
        }

    # Skills (fully curated from extra_nodes)
    if "cat-skill" in categories:
        cat = categories["cat-skill"]
        skill_children = []
        for node in extra_nodes.get("cat-skill", []):
            skill_children.append({
                "id": node["id"],
                "label": node["label"],
                "description": node.get("description", "")
            })
        output_categories["cat-skill"] = {
            "label": cat["label"],
            "group": cat["group"],
            "edge_label": cat["edge_label"],
            "description": cat.get("description", ""),
            "children": skill_children
        }

    # Also append extra_nodes for any other category
    for cat_id, extra_list in extra_nodes.items():
        if cat_id == "cat-skill":
            continue  # already handled above
        if cat_id in output_categories:
            existing_ids = {c["id"] for c in output_categories[cat_id]["children"]}
            for node in extra_list:
                if node["id"] not in existing_ids:
                    output_categories[cat_id]["children"].append({
                        "id": node["id"],
                        "label": node["label"],
                        "description": node.get("description", "")
                    })

    # ---- Build output ----
    # Maintain a stable category ordering
    category_order = [
        "cat-org", "cat-skill", "cat-tool", "cat-cert",
        "cat-framework", "cat-pub", "cat-edu", "cat-award"
    ]

    ordered_categories = {}
    for cat_id in category_order:
        if cat_id in output_categories:
            ordered_categories[cat_id] = output_categories[cat_id]
    # Add any categories not in the predefined order
    for cat_id in output_categories:
        if cat_id not in ordered_categories:
            ordered_categories[cat_id] = output_categories[cat_id]

    output = {
        "identity": {
            "label": identity.get("label", "Zachary Lanz"),
            "description": identity.get("description", "")
        },
        "categories": ordered_categories,
        "generated": datetime.now(timezone.utc).isoformat()
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        f.write("\n")

    total_children = sum(len(c["children"]) for c in ordered_categories.values())
    print(f"\nGenerated stix-graph.json: {len(ordered_categories)} categories, {total_children} child nodes")


if __name__ == "__main__":
    main()
