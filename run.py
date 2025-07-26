"""Entry point for running the economy charts application.

This module imports the Flask app factory and launches the development
server.  It is kept intentionally simple so that you can instead point
production servers (e.g. gunicorn) directly at the factory function.
"""

from app import create_app


def main() -> None:
    """Create and run the Flask application."""
    app = create_app()
    # In development, enable debug mode to auto‑reload on code changes.
    app.run(host="127.0.0.1", port=5000, debug=True)


if __name__ == "__main__":
    main()