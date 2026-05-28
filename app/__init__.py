"""Flask application factory."""
from pathlib import Path

from flask import Flask

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

    # Initialise DB helper (auto-init SQLite if needed)
    from app.db import init_app as init_db

    init_db(app)

    @app.route("/")
    def index():
        return (
            "Sistem Pemetaan Ketimpangan Digital Jawa Barat — DB connection ready."
        )

    return app
