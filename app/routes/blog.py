import os

from flask import Blueprint, abort, render_template

from app.services.markdown_parser import get_all_posts, parse_markdown_file
from config import Config

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/blog")
def blog_list():
    posts = get_all_posts(Config.BLOG_DIR)
    return render_template("blog/list.html", posts=posts)


@blog_bp.route("/blog/<slug>")
def blog_post(slug):
    file_path = os.path.join(Config.BLOG_DIR, f"{slug}.md")
    if not os.path.exists(file_path):
        abort(404)
    post = parse_markdown_file(file_path)
    return render_template("blog/post.html", post=post)
