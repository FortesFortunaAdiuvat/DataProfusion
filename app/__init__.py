"""Application factory for the economy charts Flask application."""

from __future__ import annotations
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

from app.config.secrets import SecureConfig, get_config
from app.dash.charts import create_dash_app


# Make dash_app available at package level
dash_app = None


def create_app(config_class=SecureConfig) -> Flask:
    """Create and configure a new Flask application."""
    global dash_app

    app = Flask(__name__)
    app.config.from_object(config_class)
    _configure_logging()
    PrometheusMetrics(app)

    # Initialize Dash app
    dash_app = create_dash_app()
    dash_app.init_app(app)

    # Import and initialize routes after dash_app is created
    from app.routes import init_routes

    init_routes(app)

    return app


def _configure_logging() -> None:
    """Configure application logging.

    Uses RotatingFileHandler if a log file is specified in the configuration;
    otherwise logs to standard output.
    """

    config = get_config()
    level_name = config.get_config("logging.level", "INFO").upper()
    log_file = config.get_config("logging.file")

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(getattr(logging, level_name, logging.INFO))

    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=5)
    else:
        handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
