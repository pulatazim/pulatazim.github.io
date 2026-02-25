import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Github
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_REPO = os.getenv("GITHUB_REPO")
    GITHUB_BRANCH = os.getenv("GITHUB_BRANCH")

    # Admin
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", 24))

    # Flask
    DEBUG = os.getenv("DEBUG", "False") == "True"
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # Content papkalari
    BLOG_DIR = "content/blog"
    PROJECTS_DIR = "content/projects"
    ABOUT_FILE = "content/about.md"
