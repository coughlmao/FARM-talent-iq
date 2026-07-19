# FARM Talent IQ - Backend

FastAPI backend for the FARM Talent IQ platform.

## Tech Stack

- FastAPI
- Python 3.12+
- Beanie ODM
- MongoDB Atlas
- Clerk Authentication
- Stream Video & Chat
- Inngest
- Uvicorn
- Ruff
- Pytest
- uv

---

## Prerequisites

Before starting, install:

- Python 3.12+
- uv
- MongoDB Atlas (or local MongoDB)

Install uv if you don't already have it:

```bash
pip install uv
```

or

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Installation

Clone the repository and navigate to the backend.

```bash
cd backend
```

Install all dependencies.

```bash
uv sync --group dev
```

Install Git hooks.

```bash
uv run pre-commit install
```

---

## Environment Variables

Create a `.env` file in the backend root.

Example:

```env
ENV_TYPE=development

PORT=8000

CLIENT_URL=http://localhost:5173

MONGO_URI=
MONGO_DB_NAME=

CLERK_FRONTEND_API=
CLERK_SECRET_KEY=

STREAM_API_KEY=
STREAM_API_SECRET=

INNGEST_SIGNING_KEY=
INNGEST_EVENT_KEY=
INNGEST_DEV=1
```

---

## Running the Development Server

```bash
uv run fastapi dev app/main.py
```

The API will be available at:

```
http://localhost:8000
```

Interactive documentation:

```
http://localhost:8000/docs
```

ReDoc:

```
http://localhost:8000/redoc
```

---

## Production

Run the application with Uvicorn.

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Code Quality

Run Ruff linter.

```bash
uv run ruff check --fix .
```

Format the project.

```bash
uv run ruff format .
```

---

## Project Scripts

| Command | Description |
|----------|-------------|
| `uv sync --group dev` | Install project dependencies |
| `uv run pre-commit install` | Install Git hooks |
| `uv run fastapi dev app/main.py` | Start development server |
| `uv run uvicorn app.main:app --host 0.0.0.0 --port 8000` | Start production server |
| `uv run ruff check --fix .` | Run Ruff linter |
| `uv run ruff format .` | Format code |
| `uv run pytest` | Run tests |

---

## Project Structure

```
app/
├── api/
├── core/
├── dependencies/
├── integrations/
├── models/
├── repositories/
├── schemas/
├── services/
├── main.py
└── web.py
```

---

## Development Workflow

1. Pull the latest changes.
2. Run:

```bash
uv sync --group dev
```

1. Start the development server.

```bash
uv run fastapi dev app/main.py
```

1. Before committing:

```bash
uv run ruff check --fix .
uv run ruff format .
uv run pytest
```

The pre-commit hooks will also run automatically during commits.
