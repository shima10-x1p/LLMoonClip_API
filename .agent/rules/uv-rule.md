---
trigger: always_on
---

# Custom Instructions: Prefer `uv` for Python Projects

## 1. Global Policy for Python Work

* Always assume Python projects should be managed with **`uv`** (by Astral) unless the repository clearly uses another tool (e.g. Poetry, pip-tools) and changing it would break compatibility.
* Prefer **`pyproject.toml`** managed by `uv` over `requirements.txt` or `setup.py` for new projects.
* When suggesting commands in the terminal, **default to `uv` commands** instead of `pip`, `poetry`, or `pipenv`.
* Avoid creating or editing virtual environments directly with `python -m venv` or `conda` unless the user explicitly asks.

## 2. Project Initialization & Environments

* For a **new Python project**, propose the following steps:

  1. Initialize the project:

     * `uv init` (library) or `uv init --package` (application) depending on context.
  2. Ensure a `pyproject.toml` exists and is the **single source of truth** for dependencies and metadata.
  3. Use `uv`'s built-in environment handling instead of manual venv management.
* When explaining or generating instructions, prefer patterns like:

  * `uv run python main.py`
  * `uv run fastapi dev main:app` (or similar, depending on framework)

## 3. Dependency Management Rules

* Use `uv` for all dependency operations by default:

  * Add runtime dependency: `uv add <package>`
  * Add dev dependency: `uv add --dev <package>`
  * Remove dependency: `uv remove <package>`
  * Sync lockfile / environment: `uv sync`
* Reflect dependency changes **only** in `pyproject.toml` and `uv.lock`. Do not add or maintain `requirements.txt` unless the repository already uses it and compatibility is necessary.
* When upgrading packages, suggest:

  * `uv add --upgrade <package>` or
  * `uv sync --upgrade` for broader updates (if appropriate).

## 4. Running Commands & Scripts

* When proposing shell commands for running scripts, tests, or tooling, wrap them with `uv run` unless there is a strong reason not to.
* Examples:

  * Run a module or script:

    * `uv run python -m app.main`
    * `uv run python scripts/something.py`
  * Run FastAPI (or other ASGI app):

    * `uv run uvicorn app.main:app --reload`
  * Run tests:

    * `uv run pytest`
  * Run formatters / linters:

    * `uv run ruff check .`
    * `uv run black .` (if black is used)

## 5. Testing, Linting, and Tooling

* Assume test and quality tools are installed as **dev dependencies** via `uv`:

  * `uv add --dev pytest`
  * `uv add --dev ruff`
  * `uv add --dev mypy` (if type checking is requested)
* When generating CI config (GitHub Actions, etc.), prefer using `uv` for install + run steps, e.g.:

  * `pip install uv` (if needed in CI image)
  * `uv sync`
  * `uv run pytest`

## 6. Repository Detection & Fallback Rules

* If a repository already contains `pyproject.toml` and `uv.lock`, **assume `uv` is the canonical tool**.
* If the repo contains `poetry.lock`, `Pipfile`, or `requirements.txt` but **no** `uv.lock`, then:

  * Do **not** auto-migrate to `uv` unless the user explicitly requests it.
  * Respect existing tools but may *optionally* suggest a migration path using `uv` in comments or documentation.
* Never mix multiple dependency managers in the same project unless explicitly requested by the user.

## 7. Instructions for GitHub Copilot

When acting as GitHub Copilot (chat or inline):

* Prefer to:

  * Suggest `uv` commands when the user asks "how do I install / run / test" in Python projects, unless the project clearly uses another tool.
  * Use `uv run` prefixed commands in generated README snippets, developer docs, and task descriptions.
* Avoid to:

  * Suggest plain `pip install ...` or `python -m venv .venv` unless the repository already uses that pattern or the user asks for it.

### Example phrasing for Copilot suggestions

* "You can install the dependencies with `uv sync` and then run the app via `uv run uvicorn app.main:app --reload`."
* "Add `uv`-managed dev dependencies via `uv add --dev pytest ruff` and then run tests with `uv run pytest`."

## 8. Instructions for Antigravity (AI IDE)

When acting inside Antigravity as an AI assistant or Agent:

* For **Python projects**:

  * Plan and generate project scaffolding using `uv` for dependency and environment management.
  * When creating tasks, include explicit `uv` commands in the task descriptions.
  * When generating shell scripts (e.g. `bootstrap.sh`, `dev.sh`), base them on `uv`, e.g.:

    * `uv sync`
    * `uv run pytest`
    * `uv run fastapi dev main:app`
* Coordinate changes:

  * Whenever you add new imports that require external packages, also propose the corresponding `uv add ...` command and `pyproject.toml` updates.

### Example high-level instruction for Antigravity

* "For any Python project in this workspace, manage dependencies and virtual environments with `uv`. Use `pyproject.toml` and `uv.lock` as the single source of truth, and prefer `uv run ...` commands when running tools, tests, or applications. Do not introduce `pip`, `poetry`, or `conda` unless they are already clearly used by the repository or the user explicitly requests them."

## 9. Style & Documentation

* In documentation, code comments, and generated READMEs:

  * Show `uv`-based workflows as the primary example.
  * If you mention alternative tools (pip/poetry), note them briefly as secondary options.
* Prefer concise, reproducible command sequences like:

  1. `uv sync`
  2. `uv run pytest`
  3. `uv run uvicorn app.main:app --reload`

---

These rules are meant to bias all Python-related assistance towards a **`uv`-first workflow**, while still respecting existing project tooling when it is clearly established.
