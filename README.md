# Economy Charts Project

This repository contains a starter project for building a web application that
visualises economic data using **Plotly Dash** embedded inside a **Flask**
application.  It is designed to provide a clean structure for extending the
application with new charts sourced from public datasets such as EDGAR, the
Federal Reserve Economic Data (FRED), or other federal sources.

## Prerequisites

- **Python 3.13** or newer.  Although earlier versions may work, this project
  intentionally targets Python 3.13 to take advantage of the latest language
  features and security updates.
- A recent version of `pip` for installing the Python dependencies.

To ensure you’re using at least Python 3.13, run:

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

4. **Configure API keys (required for data sources).**

   ```bash
   python setup_config.py
   ```
   
   Follow the prompts to enter your API keys for FRED and other data sources.
   See [CONFIG_SETUP.md](CONFIG_SETUP.md) for detailed configuration instructions.

5. **Run the application.**  The development server listens on
   `http://127.0.0.1:5000` by default.  You can change the host or port by
   modifying `run.py`.

   ```bash
   python run.py
   ```

6. **Visit your Dash application.**  Once the server is running, open
   `http://127.0.0.1:5000/dash/` in your browser to see the sample chart.

## Docker

You can build and run the application inside a Docker container.

### Build the image

```bash
docker build -t economy-charts .
```

### Run the container

```bash
docker run -p 8000:8000 economy-charts
```

### Using docker-compose

The repository includes a `docker-compose.yml` that starts the web application
along with a small Redis cache. To build and run all services:

```bash
docker compose up --build
```

## Testing

This project includes a comprehensive test suite to ensure reliability and data quality.

### Quick Test Commands

```bash
# Run fast unit tests (no API calls required)
python run_tests.py unit

# Run integration tests (requires FRED API key)
python run_tests.py integration

# Run all tests
python run_tests.py all
```

### Detailed Testing Instructions

For comprehensive testing documentation, including:
- Test setup and configuration
- API key requirements
- Troubleshooting failed tests
- Writing new tests
- CI/CD integration

See **[tests/TEST_INSTRUCTIONS.md](tests/TEST_INSTRUCTIONS.md)**

### Test Categories

- **Unit Tests** - Fast, isolated tests using mocks (no external dependencies)
- **Integration Tests** - Real API connectivity tests (requires FRED API key)
- **Coverage Reports** - Code coverage analysis and reporting

## Project Structure

The project is organised to separate the Flask application from the Dash
components, making it easier to extend either side independently.

```
economy_charts/
├── app/
│   ├── __init__.py        # Factory function that creates and configures the Flask app
│   ├── routes.py          # (Optional) Flask routes for non‑Dash pages
│   ├── config/
│   │   └── secrets.py     # Secure API key and configuration management
│   ├── data/
│   │   ├── fred_client.py # FRED API client with caching
│   │   └── economic_indicators.py # Economic indicator definitions
│   ├── templates/
│   │   └── layout.html   # Template used for any Flask view (if needed)
│   └── dash/
│       ├── __init__.py    # Function to register Dash on the Flask app
│       └── charts.py     # Functions that create Plotly figures
├── tests/
│   ├── TEST_INSTRUCTIONS.md # Comprehensive testing documentation
│   ├── conftest.py       # Pytest configuration and fixtures
│   ├── test_config.py    # Configuration management tests
│   ├── test_fred_client.py # FRED client unit tests
│   ├── test_fred_integration.py # FRED API integration tests
│   └── test_economic_indicators.py # Economic indicators tests
├── config/
│   └── secrets.json      # API keys and configuration (auto-generated)
├── run.py                 # Entry point that imports the factory and runs the server
├── run_tests.py           # Test runner script
├── setup_config.py       # Interactive API key configuration
├── requirements.txt       # Python dependencies
├── CONFIG_SETUP.md        # Configuration setup instructions
└── README.md              # This file
```

### Explanation of Key Files

* **`app/__init__.py`** – Defines a `create_app()` function that configures
  and returns a Flask application instance.  This factory pattern makes it
  easier to configure the app differently for development, testing or
  production.

* **`app/config/secrets.py`** – Secure configuration management system that
  handles API keys and application settings. Supports environment variables
  and encrypted storage.

* **`app/data/fred_client.py`** – FRED API client with intelligent caching,
  rate limiting, and error handling. Automatically falls back to cached data
  when the API is unavailable.

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

* **`tests/`** – Comprehensive test suite including unit tests, integration
  tests, and testing documentation. See [tests/TEST_INSTRUCTIONS.md](tests/TEST_INSTRUCTIONS.md)
  for detailed information.

## Development Workflow

### Before You Start

1. **Set up your development environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure API keys:**
   ```bash
   python setup_config.py
   ```

3. **Verify your setup:**
   ```bash
   python run_tests.py unit
   python run_tests.py integration  # Requires API key
   ```

### During Development

1. **Run unit tests frequently:**
   ```bash
   python run_tests.py unit
   ```

2. **Test your changes:**
   ```bash
   python run.py
   # Visit http://127.0.0.1:5000/dash/
   ```

3. **Before committing:**
   ```bash
   python run_tests.py all
   ```

## Next Steps: Building Economic Charts

This skeleton project demonstrates how to embed a basic Plotly chart in Dash
within Flask.  To expand it into a useful tool for learning macro‑ and
micro‑economics, consider the following tasks:

1. **Add data retrieval modules.**
   - The `app/data/` directory already includes a robust FRED client
   - Create additional clients for other data sources such as:
     - [**EDGAR**](https://www.sec.gov/edgar.shtml) – corporate financial
       statements and filings.
     - [**BEA**](https://www.bea.gov/) – Bureau of Economic Analysis datasets.
     - [**BLS**](https://www.bls.gov/) – Bureau of Labor Statistics for labour
       market metrics.
     - **Cryptocurrency APIs** – CoinMarketCap, CoinGecko for crypto data
   - When writing data retrieval code, follow the pattern established in
     `fred_client.py` with caching, error handling, and comprehensive testing.

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
   - The project already includes a comprehensive test suite. As you add
     features, write corresponding tests following the patterns in the
     `tests/` directory.
   - Configure linters such as `flake8` and `black` in your development
     environment to maintain a consistent code style.
   - Use the test runner to ensure your changes don't break existing functionality.

## Security and Configuration

- **API keys are secure** - Configuration files are automatically excluded from
  version control and AI assistant context
- **Environment variable support** - API keys can be set via environment variables
  for production deployments
- **Caching system** - Intelligent data caching reduces API calls and improves performance
- **Error handling** - Robust error handling with fallback to cached data when APIs are unavailable

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

With these building blocks in place, you can iteratively add more data
sources, enrich the interactivity of your charts and deliver an educational
tool for exploring the dynamics of the economy.
