import os

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from app.errors import ApiError


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "lab_equipment.db"),
        JSON_SORT_KEYS=False,
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    from . import database

    database.init_app(app)

    from .routes.item_routes import bp as item_blueprint
    from .routes.loan_routes import bp as loan_blueprint

    app.register_blueprint(item_blueprint)
    app.register_blueprint(loan_blueprint)

    @app.errorhandler(ApiError)
    def handle_api_error(error):
        return jsonify({"error": error.message}), error.status_code

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        return jsonify({"error": error.description}), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception("Unhandled exception")
        return jsonify({"error": "Internal server error"}), 500

    return app
