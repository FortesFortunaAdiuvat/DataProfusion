# Contributing to Economy Charts

Thank you for your interest in contributing!  This project aims to build an
educational dashboard for exploring macro‑ and micro‑economic data.  We use
Flask to handle authentication and routing, and embed interactive charts
written with Plotly Dash.  Contributions are welcome in the form of new charts,
bug fixes, documentation improvements, and feature enhancements.

## Development process

1. **Fork the repository or create a feature branch.**  Begin by creating a
   separate branch off `main` to develop your changes.  Use a descriptive
   branch name such as `feat/add-unemployment-chart` or `bugfix/fix-login`.

2. **Set up a virtual environment.**  Ensure you’re using Python 3.13 or
   newer, create a virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the app locally.**  Use `python run.py` to start the development
   server.  Visit `http://127.0.0.1:5000/dash/` to verify your changes before
   committing.

4. **Adding a new Dash chart.**

   * Create a new function in `app/dash/charts.py` (or a new module under
     `app/dash/`) that returns a Plotly figure.  Keep the function pure: it
     should accept data as parameters where possible and avoid side effects.
   * Update the Dash layout in `app/dash/__init__.py` to include your new chart.
     You can add another `dcc.Graph` component or create tabs to separate
     different charts.  If you need callbacks, define them immediately after
     the layout and use unique component IDs.
   * If your chart depends on external data, add a corresponding data loader
     under a new `app/data/` module.  This separation makes it easier to test
     and cache data.

5. **Coding style and linting.**  Follow PEP 8 guidelines for Python code.
   Use meaningful variable names and include docstrings for functions and
   modules.  Before opening a pull request, run linters (e.g. `flake8`) and
   format your code with `black` (optional but recommended).

6. **Testing.**  If you introduce new functionality, provide unit tests
   using [`pytest`](https://docs.pytest.org/) under a `tests/` directory.
   Tests should be deterministic and not rely on external APIs whenever
   possible (mock responses instead).

7. **Commit messages.**  Write clear, concise commit messages describing what
   changed and why.  Follow the conventional format:

   *Short summary (≤ 72 characters)*

   *Long description explaining the change, why it’s needed, and any
   limitations.*

8. **Open a pull request (PR).**  Push your branch to your fork and open a PR
   against `main`.  Describe the changes made, reference any relevant issues
   or discussion, and include screenshots or GIFs of your new charts when
   appropriate.  Make sure your PR is up to date with `main` by rebasing or
   merging before requesting review.

9. **Respond to feedback.**  Maintainers may request changes or ask clarifying
   questions.  Be ready to iterate on your PR until it meets the project’s
   standards.  Once approved, your contribution will be merged into `main`.

## Code of conduct

Contributors are expected to uphold the principles of inclusion and respect.
Be courteous in issue discussions and code reviews.  Harassment, hate
speech, or disrespectful behaviour will not be tolerated.