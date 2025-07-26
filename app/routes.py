"""Additional Flask routes.

If you wish to serve traditional Flask-rendered pages (e.g. home page,
authentication, documentation) alongside the Dash dashboards, define them
here and import them in the application factory.  This module is currently
empty and exists as a stub for future development.
"""

from __future__ import annotations

from flask import Blueprint, render_template

bp = Blueprint("main", __name__)


@bp.route("/about")
def about():
    """Render a simple about page with information about the project."""
    # In practice you would create a 'about.html' template under
    # `app/templates/` and render it here.  For now this is a placeholder.
    return "<h1>About</h1><p>This will be a static about page.</p>"