"""Additional Flask routes.

If you wish to serve traditional Flask-rendered pages (e.g. home page,
authentication, documentation) alongside the Dash dashboards, define them
here and import them in the application factory.  This module is currently
empty and exists as a stub for future development.
"""

from __future__ import annotations

from flask import Blueprint, render_template, redirect, url_for

bp = Blueprint("main", __name__)


def init_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html", active_page="home")

    @app.route("/charts")
    def charts():
        """Render a list of available Dash charts."""
        return render_template("charts.html", active_page="charts")

    @app.route("/news")
    def news():
        return render_template("news.html", active_page="news")

    @app.route("/about")
    def about():
        return render_template("about.html", active_page="about")

    @app.route("/contact")
    def contact():
        return render_template("contact.html", active_page="contact")

    # Note: Dash routes are automatically handled by the Dash app integration
    # The /dash/ route is managed by the Dash application itself
