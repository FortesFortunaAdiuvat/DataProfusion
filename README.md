# Economy Charts Project

This repository contains a starter project for building a web application that
visualises economic data using **Plotly Dash** embedded inside a **Flask**
application.  It is designed to provide a clean structure for extending the
application with new charts sourced from public datasets such as EDGAR, the
Federal Reserve Economic Data (FRED), or other federal sources.

## Prerequisites

- **Python 3.13** or newer.  Although earlier versions may work, this project
  intentionally targets Python 3.13 to take advantage of the latest language
  features and security updates.
- A recent version of `pip` for installing the Python dependencies.

To ensure you’re using at least Python 3.13, run:

```bash
python3 --version
```

If the version is lower than 3.13, consider installing a suitable Python
distribution such as [pyenv](https://github.com/pyenv/pyenv), [Anaconda](https://www.anaconda.com/),
or the official Python installer for your operating system.

## Installation

1. **Clone or download this repository.**
   
   ```bash
   git clone <repository-url>
   cd economy_charts
   ```

2. **Create a virtual environment (optional but recommended).**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install the required Python packages.**  The main dependencies are
   `Flask` and `Dash` (which includes Plotly).  Additional packages can be
   added to `requirements.txt` as the project grows.

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application.**  The development server listens on
   `http://127.0.0.1:5000` by default.  You can change the host or port by
   modifying `run.py`.

   ```bash
   python run.py
   ```

5. **Visit your Dash application.**  Once the server is running, open
   `http://127.0.0.1:5000/dash/` in your browser to see the sample chart.

## Project Structure

The project is organised to separate the Flask application from the Dash
components, making it easier to extend either side independently.

```
economy_charts/
├── app/
│   ├── __init__.py        # Factory function that creates and configures the Flask app
│   ├── routes.py          # (Optional) Flask routes for non‑Dash pages
│   ├── templates/
│   │   └── layout.html   # Template used for any Flask view (if needed)
│   └── dash/
│       ├── __init__.py    # Function to register Dash on the Flask app
│       └── charts.py     # Functions that create Plotly figures
├── run.py                 # Entry point that imports the factory and runs the server
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

### Explanation of Key Files

* **`app/__init__.py`** – Defines a `create_app()` function that configures
  and returns a Flask application instance.  This factory pattern makes it
  easier to configure the app differently for development, testing or
  production.

* **`app/dash/__init__.py`** – Contains the `register_dashapps()` function
  which creates and mounts one or more Dash applications on the Flask server.
  Each Dash instance can live at its own URL prefix (e.g. `/dash/`).

* **`app/dash/charts.py`** – Centralises chart creation.  As you add new
  economic charts, define them here or in submodules so they can be imported
  into your Dash layouts.

* **`run.py`** – A simple runner that invokes `create_app()` and starts the
  Flask development server.  This script is meant for local development.  For
  deployment behind a production web server (e.g. gunicorn or uwsgi), you
  should expose the Flask app directly via the factory.

## Next Steps: Building Economic Charts

This skeleton project demonstrates how to embed a basic Plotly chart in Dash
within Flask.  To expand it into a useful tool for learning macro‑ and
micro‑economics, consider the following tasks:

1. **Add data retrieval modules.**
   - Create a directory (e.g. `app/data/`) where you write functions to
     download, cache and parse data from public sources such as:
     - [**EDGAR**](https://www.sec.gov/edgar.shtml) – corporate financial
       statements and filings.
     - [**FRED**](https://fred.stlouisfed.org) – economic time series like GDP,
       unemployment, interest rates, etc.
     - [**BEA**](https://www.bea.gov/) – Bureau of Economic Analysis datasets.
     - [**BLS**](https://www.bls.gov/) – Bureau of Labor Statistics for labour
       market metrics.
   - When writing data retrieval code, respect API rate limits and build
     helper functions to clean and structure the data for charting.

2. **Design Dash layouts for new charts.**
   - Within `app/dash/__init__.py`, you can mount additional Dash apps at
     different URL prefixes (e.g. `/gdp/`, `/unemployment/`) or use tabs
     inside one Dash app.
   - Use the functions in `app/dash/charts.py` to supply Plotly figures
     representing these datasets.  Plotly’s interactive features (zooming,
     tooltips, filtering) make it well suited for economic visualisation.

3. **Implement authentication and user management.**
   - Since this project uses Flask, you can integrate typical Flask utilities
     such as sessions, user login, and role‑based access control (e.g.
     `Flask‑Login`).  Add a `login` route in `app/routes.py` and protect
     certain Dash endpoints behind authentication decorators.

4. **Styling and UI refinement.**
   - Consider using a front‑end framework such as Bootstrap or Bulma
     (integrated via `dash_bootstrap_components`) to give the site a cohesive
     look and feel.
   - Create custom Jinja templates in `app/templates/` for non‑Dash pages
     (e.g. a home page, about page, contact page).

5. **Testing and code quality.**
   - As the code base grows, write unit tests using `pytest` to ensure your
     data loading and chart functions behave correctly.
   - Configure linters such as `flake8` and `black` in your development
     environment to maintain a consistent code style.

With these building blocks in place, you can iteratively add more data
sources, enrich the interactivity of your charts and deliver an educational
tool for exploring the dynamics of the economy.