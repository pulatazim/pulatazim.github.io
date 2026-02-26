import os
from datetime import datetime

import markdown
import yaml


def parse_markdown_file(file_path):
    """.md faylni o'qib, frontmatter va HTML qaytaradi."""

    with open(file_path, "r", encoding="utf-8") as file:
        raw = file.read()

    if raw.startswith("---"):
        parts = raw.split("---", 2)
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2].strip()
    else:
        frontmatter = {}
        body = raw.strip()

    # MARKDOWN -> HTML
    html_content = markdown.markdown(body, extensions=["fenced_code", "tables"])

    # frontmatter + HTML ni birlashtiramiz
    result = frontmatter or {}
    result["content"] = html_content
    result["raw"] = raw

    # Sana formatini tekshiramiz
    if "date" in result and isinstance(result["date"], str):
        result["date"] = datetime.strptime(result["date"], "%Y-%m-%d")

    return result


def get_all_posts(folder):
    """Papkadan .md fayllarni o'qib, ro'yxat qaytaradi."""

    posts = []

    for filename in os.listdir(folder):
        if not filename.endswith(".md"):
            continue
        if filename.startswith("."):
            continue

        file_path = os.path.join(folder, filename)
        post = parse_markdown_file(file_path)

        # Slug = file nomi .md siz
        post["slug"] = filename.replace(".md", "")

        # faqat published true bo'lganlar
        if post.get("published", False):
            posts.append(post)

    # Sanaga ko'ra tartiblash
    posts.sort(key=lambda post: post.get("date", datetime.min), reverse=True)
    return posts
