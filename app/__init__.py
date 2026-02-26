from flask import Flask

from app.routes.admin import admin_bp
from app.routes.blog import blog_bp
from app.routes.main import main_bp
from app.routes.projects import projects_bp
from config import Config


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config)

    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(projects_bp)

    return app
