# Repository Guidelines

## Project Structure & Module Organization
- Core C++ binding lives in `src/main.cpp`; the Python package is in `src/tessbind/` with the built extension `_core` and helpers like `manager.py` and `utils.py`.
- Third-party sources are vendored under `extern/` (zlib, libpng, leptonica, tesseract) and compiled during builds; avoid manual edits there.
- Python packaging metadata sits in `pyproject.toml` and `setup.py`; distribution artifacts land in `dist/`.
- Tests live in `tests/` with fixtures such as `hello.png`; helper scripts for setup/cleanup are in `scripts/`.

-## Build, Test, and Development Commands
- Use `mise install` to set up the `.venv` defined in `.mise.toml`; activate it (`source .venv/bin/activate`) before builds.
- `uv sync --extra test`: create/update the virtualenv and install dev deps; triggers `build_dependencies.sh` to compile vendored libs, so ensure `cmake` and a compiler are available.
- `uv run python -m build`: produce sdist/wheel in `dist/`.
- `uv run pytest -m "not slow"`: run the default suite; add `-m slow` when you explicitly want long-running loops.
- `mise run update-extern`: update all `extern/` submodules to their latest tracked upstream revisions.
- Set `TESSDATA_PREFIX` if Tesseract data files are not auto-discovered; Linux CI uses `/usr/share/tesseract-ocr/5/tessdata`.

## Coding Style & Naming Conventions
- Target Python 3.12+; prefer type hints everywhere (`from __future__ import annotations` is required by import sorting).
- Ruff enforces lint rules and import order; run `ruff check .` before sending a PR.
- Static checks with `mypy src tests` (strict mode enabled for `tessbind.*`); keep functions typed and avoid implicit `Any`.
- Use descriptive lowercase_with_underscores for Python symbols; C++ identifiers should mirror existing pybind11 style.

## Testing Guidelines
- Place new tests under `tests/` and mark long-running cases with `@pytest.mark.slow`.
- Use the provided `hello.png` or small fixtures; clean up any temp files created by new tests.
- Aim for coverage of both the Python API and the pybind11 surface; prefer arranging and asserting around small, deterministic inputs.

## Commit & Pull Request Guidelines
- Commit messages follow short, imperative summaries (e.g., `add macos brew hint`, `fix tessdata lookup`); keep them under ~72 chars.
- For PRs, include a brief problem statement, the approach, and any manual checks (build/test commands) you ran; link issues when applicable.
- Update docs or tests alongside code changes; mention any required system deps or environment variables in the PR description.
