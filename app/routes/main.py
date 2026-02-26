from flask import Blueprint, render_template

from app.services.markdown_parser import parse_markdown_file
from config import Config

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/about")
def about():
    about = parse_markdown_file(Config.ABOUT_FILE)
    return render_template("about.html", about=about)
