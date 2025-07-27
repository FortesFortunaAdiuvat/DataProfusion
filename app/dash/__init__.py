"""Functions for mounting Dash applications onto the Flask server.

Dash apps are created and registered here.  Keeping this logic separate
facilitates modularity: multiple Dash apps can coexist under different
URL prefixes, each with its own layout and callbacks.
"""

from __future__ import annotations

import dash
from dash import Dash, html, dcc

from flask import Flask

from .charts import sample_chart


def register_dashapps(app: Flask) -> None:
    """Create and register one or more Dash applications on the given Flask app.

    This function attaches the Dash app(s) to specific URL prefixes and
    configures them to use the Flask server for handling requests.

    Parameters
    ----------
    app : Flask
        The Flask application instance on which to mount Dash.
    """
    # Example: register a single Dash app at '/dash/'
    mount_path = "/dash/"
    dash_app = Dash(
        __name__,
        server=app,
        url_base_pathname=mount_path,
        title="Economic Charts",
        suppress_callback_exceptions=True,
    )

    # Use a simple external stylesheet provided by Dash for baseline styling.
    dash_app._external_stylesheets = [
        "https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
    ]

    # Build a basic layout containing a header and a Plotly graph created in
    # charts.py.  For larger apps you might use Dash components such as Tabs
    # or separate pages.
    dash_app.layout = html.Div(
        [
            html.H2("Economic Indicators Dashboard"),
            dcc.Graph(
                id="sample-graph",
                figure=sample_chart(),
            ),
        ],
        style={"margin": "40px"},
    )

    # Set the external stylesheets properly
    dash_app.config.external_stylesheets = dash_app._external_stylesheets
    
    # Register a Flask route that redirects to the Dash app
    # This creates the 'dash_dashboard' endpoint that can be used with url_for()
    @app.route('/dashboard/')
    def dash_dashboard():
        """Redirect to the Dash application."""
        from flask import redirect
        return redirect(mount_path)
