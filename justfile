SOURCE_PATH := "userpic.py"

upgrade:
    uv lock --upgrade

lint:
    uv run ruff check {{ SOURCE_PATH }}
    uv run python -m mypy --pretty {{ SOURCE_PATH }}

fix:
    uv run ruff format {{ SOURCE_PATH }}
    uv run ruff check --fix --unsafe-fixes {{ SOURCE_PATH }}
