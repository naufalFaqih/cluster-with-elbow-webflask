"""Flask application factory."""
from pathlib import Path

from flask import Flask, redirect, url_for

from config import Config


def create_app(config_class: type = Config) -> Flask:
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    app.config.from_object(config_class)

    # Ensure upload folder exists
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    # Initialise DB helper
    from app.db import init_app as init_db

    init_db(app)

    # Blueprints
    from app.routes.auth_routes import bp as auth_bp

    app.register_blueprint(auth_bp)

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    return app
