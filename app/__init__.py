"""Flask application factory (scaffold)."""
from flask import Flask

from config import Config


def create_app(config_class: type = Config) -> Flask:
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    app.config.from_object(config_class)

    @app.route("/")
    def index():
        return (
            "Sistem Pemetaan Ketimpangan Digital Jawa Barat — Flask scaffold OK."
        )

    return app
