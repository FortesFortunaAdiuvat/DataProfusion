"""Application factory for the economy charts Flask application."""

from __future__ import annotations
from flask import Flask
from app.config.secrets import SecureConfig
from app.dash.charts import create_dash_app


# Make dash_app available at package level
dash_app = None


def create_app(config_class=SecureConfig) -> Flask:
    """Create and configure a new Flask application."""
    global dash_app

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Dash app
    dash_app = create_dash_app()
    dash_app.init_app(app)

    # Import and initialize routes after dash_app is created
    from app.routes import init_routes

    init_routes(app)

    return app
