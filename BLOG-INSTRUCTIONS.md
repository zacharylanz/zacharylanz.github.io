# Blog System Instructions

This website uses a markdown-based blog system that makes it easy to add new articles.

## How to Add a New Blog Post

### Step 1: Create Your Markdown File

1. Create a new markdown file in the `posts/` directory
2. Name it descriptively (e.g., `threat-hunting-techniques.md`)
3. Write your content using standard markdown syntax

**Example markdown file structure:**
```markdown
# Your Article Title

Introduction paragraph here...

## Main Section Heading

Your content here with **bold text** and *italic text*.

### Subsection

- Bullet point 1
- Bullet point 2
- Bullet point 3

## Another Section

More content...
```

### Step 2: Add Metadata to data/blog-posts.json

Open `data/blog-posts.json` and add a new entry to the `posts` array:

```json
{
  "id": "unique-article-id",
  "title": "Your Article Title",
  "subtitle": "Optional subtitle or tagline",
  "category": "Category Name",
  "date": "2026-01-15",
  "readTime": "5 min read",
  "excerpt": "A brief 1-2 sentence description that appears on the blog listing page.",
  "markdownFile": "posts/your-markdown-file.md",
  "tags": ["Tag 1", "Tag 2", "Tag 3"]
}
```

**Field Descriptions:**
- `id`: Unique identifier (use lowercase with hyphens, e.g., "threat-hunting-101")
- `title`: Main article title
- `subtitle`: Optional subtitle (can be omitted)
- `category`: Category badge shown on cards (e.g., "Threat Intelligence", "Career Development", "OSINT")
- `date`: Publication date in YYYY-MM-DD format
- `readTime`: Estimated reading time (e.g., "5 min read")
- `excerpt`: Short description for blog listing page
- `markdownFile`: Path to your markdown file (relative to root, e.g., "posts/filename.md")
- `tags`: Array of topic tags for the article footer

### Step 3: Publish

1. Commit your changes to git:
   ```bash
   git add posts/your-article.md data/blog-posts.json
   git commit -m "Add new blog post: Your Article Title"
   git push
   ```

2. The article will automatically appear on your blog page and be accessible via the dynamic article viewer.

## Markdown Formatting Tips

### Headings
```markdown
# H1 - Article Title (used once at top)
## H2 - Main Sections
### H3 - Subsections
```

### Lists
```markdown
- Unordered list item
- Another item

1. Ordered list item
2. Second item
```

### Emphasis
```markdown
**Bold text**
*Italic text*
***Bold and italic***
```

### Links
```markdown
[Link text](https://example.com)
```

### Code
```markdown
Inline `code` here

```
Code block here
```
```

### Quotes
```markdown
> This is a blockquote
```

### Horizontal Rule
```markdown
---
```

## Styling Features

The blog system automatically applies your site's styling to markdown content:

- **Headings** are styled with the site's color scheme
- **Links** use the accent color
- **Lists** have custom bullet points
- **Code** uses monospace fonts
- **Blockquotes** have left borders
- All content is responsive and mobile-friendly

## Example: Complete data/blog-posts.json Entry

```json
{
  "posts": [
    {
      "id": "getting-started-cti",
      "title": "Getting Started in Cyber Threat Intelligence",
      "subtitle": "A practical guide for aspiring CTI professionals",
      "category": "Career Development",
      "date": "2026-01-08",
      "readTime": "5 min read",
      "excerpt": "Cyber Threat Intelligence has become one of the most critical disciplines in cybersecurity. Here's what you need to know to get started.",
      "markdownFile": "posts/getting-started-cti.md",
      "tags": ["CTI", "Career", "Getting Started"]
    },
    {
      "id": "osint-techniques",
      "title": "Advanced OSINT Techniques for Threat Hunting",
      "subtitle": "Leveraging open-source intelligence for proactive defense",
      "category": "OSINT",
      "date": "2026-01-15",
      "readTime": "8 min read",
      "excerpt": "Learn advanced open-source intelligence techniques to identify and track threat actors before they strike.",
      "markdownFile": "posts/osint-techniques.md",
      "tags": ["OSINT", "Threat Hunting", "Intelligence Collection"]
    }
  ]
}
```

## Technical Details

- **Markdown Parser**: Uses [Marked.js](https://marked.js.org/) for client-side markdown parsing
- **Dynamic Loading**: Articles are loaded via JavaScript when users click on blog cards
- **URL Structure**: Articles are accessed via `article.html?id=your-article-id`
- **SEO**: Page titles and meta descriptions update dynamically based on article metadata

## Troubleshooting

**Article not showing on blog page:**
- Check that `data/blog-posts.json` is valid JSON (use a JSON validator)
- Ensure the markdown file path is correct
- Clear browser cache and reload

**Formatting issues:**
- Verify your markdown syntax
- Check that special characters are properly escaped
- Test your markdown in a markdown preview tool first

**Images in articles:**
- Place images in an `images/` directory
- Reference them in markdown: `![Alt text](images/your-image.jpg)`
- Use relative paths from the root directory
