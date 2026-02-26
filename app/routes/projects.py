import os

from flask import Blueprint, abort, render_template

from app.services.markdown_parser import get_all_posts, parse_markdown_file
from config import Config

projects_bp = Blueprint("projects", __name__)


@projects_bp.route("/projects")
def projects_list():
    projects = get_all_posts(Config.PROJECTS_DIR)
    return render_template("projects/list.html", projects=projects)


@projects_bp.route("/projects/<slug>")
def project(slug):
    file_path = os.path.join(Config.PROJECTS_DIR, f"{slug}.md")
    if not os.path.exists(file_path):
        abort(404)
    project = parse_markdown_file(file_path)
    return render_template("projects/project.html", project=project)
