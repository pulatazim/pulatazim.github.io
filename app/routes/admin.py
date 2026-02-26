from flask import Blueprint, jsonify, render_template, request

from app.services.github_service import delete_file, write_file
from app.services.markdown_parser import get_all_posts, parse_markdown_file
from app.utils.auth import generate_token, token_required
from config import Config

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/login", methods=["GET"])
def login_page():
    return render_template("admin/login.html")


@admin_bp.route("/admin/login", methods=["POST"])
def login():
    data = request.get_json()
    password = data.get("password")

    if password == Config.ADMIN_PASSWORD:
        token = generate_token()
        return jsonify({"token": token})
    return jsonify({"error": "Parol noto'g'ri"}), 401


@admin_bp.route("/admin/dashboard")
@token_required
def dashboard():
    posts = get_all_posts(Config.BLOG_DIR)
    projects = get_all_posts(Config.PROJECTS_DIR)
    return render_template("admin/dashboard.html", posts=posts, projects=projects)


@admin_bp.route("/admin/new-post")
@token_required
def new_post():
    return render_template("admin/editor.html", post=None)


@admin_bp.route("/admin/edit/<path:file_path>")
@token_required
def edit_post(file_path):
    post = parse_markdown_file(file_path)
    post["file_path"] = file_path
    return render_template("admin/editor.html", post=post)


@admin_bp.route("/admin/save", methods=["POST"])
@token_required
def save_post():
    data = request.get_json()
    file_path = data.get("file_path")
    content = data.get("content")
    message = data.get("message", "content: post yangilandi")

    write_file(file_path, content, message)
    return jsonify({"message": True}), 200


@admin_bp.route("/admin/delete", methods=["POST"])
@token_required
def delete_post():
    data = request.get_json()
    file_path = data.get("file_path")
    message = data.get("message", "content: post o'chirildi")

    delete_file(file_path, message)
    return jsonify({"message": True}), 200
