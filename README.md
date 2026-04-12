# zacharylanz.github.io

Personal portfolio!

**Live site:** [www.lanzsec.com](https://www.lanzsec.com)

## Structure

- `index.html` — Home page with about section, Diamond Model, and contact
- `experience.html` — Professional experience timeline
- `portfolio.html` — Certifications, publications, and achievements
- `resources.html` — Curated CTI tools, reports, and learning resources
- `blog.html` / `article.html` — Blog listing and article reader
- `stix-graph.html` — Interactive STIX-style network visualization
- `posts/` — Blog post markdown files
- `data/blog-posts.json` — Blog manifest (auto-generated from front matter)
- `scripts/generate-blog-posts.py` — Generates blog manifest from `posts/*.md`
- `.dev/` — Developer reference files (blog template, instructions)

## Adding Blog Posts

1. Create a markdown file in `posts/` with YAML front matter (see `.dev/TEMPLATE.md`)
2. Commit and push — the GitHub Action auto-generates `data/blog-posts.json`

## Tech Stack

Static HTML/CSS/JS hosted on GitHub Pages. No build step required.
