```
install:
    uv sync --group dev
    uv run pre-commit install

dev:
    uv run fastapi dev app/main.py

lint:
    uv run ruff check --fix .
    uv run ruff format .

test:
    uv run pytest

start:
    uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```