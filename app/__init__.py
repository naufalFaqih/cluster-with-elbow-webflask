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

    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    from app.db import init_app as init_db

    init_db(app)

    # Blueprints
    from app.routes.auth_routes import bp as auth_bp
    from app.routes.dashboard_routes import bp as dashboard_bp
    from app.routes.wilayah_routes import bp as wilayah_bp
    from app.routes.data_routes import bp as data_bp
    from app.routes.clustering_routes import bp as clustering_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(wilayah_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(clustering_bp)

    @app.route("/")
    def index():
        return redirect(url_for("dashboard.index"))

    @app.context_processor
    def inject_globals():
        from flask import session

        return {
            "current_user": {
                "id": session.get("user_id"),
                "nama": session.get("user_nama"),
                "username": session.get("user_username"),
                "role": session.get("user_role"),
            }
            if session.get("user_id")
            else None,
        }

    return app
