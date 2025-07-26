"""Application factory for the economy charts Flask application.

By using a factory function we can create multiple instances of the app with
different configurations (e.g. for testing versus production).  It also
decouples the creation of the Dash apps from the Flask app, making the
structure modular and easier to extend.
"""

from __future__ import annotations

import os
from flask import Flask, redirect, url_for

from .dash import register_dashapps


def create_app() -> Flask:
    """Create and configure a new Flask application.

    Returns
    -------
    Flask
        A configured Flask application instance.
    """
    app = Flask(__name__, instance_relative_config=False)

    # Set a secret key for session management.  In production you should
    # override this via an environment variable or configuration file.
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-me")

    # Register Dash applications on this Flask server.
    register_dashapps(app)

    @app.route("/")
    def index():
        """Redirect the root URL to the Dash application."""
        # You can change '/dash/' to any path where your main Dash app lives.
        return redirect(url_for("dash_dashboard"))

    # Additional Flask routes can be defined here or imported from .routes

    return app