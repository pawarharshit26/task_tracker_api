# Pragya API

A personal growth and task tracking backend built with FastAPI, async SQLAlchemy, and PostgreSQL.

Pragya helps users define a life vision and break it down into actionable layers: **Vision → Themes → Tracks → Goals → Phases → Daily Commitments → Execution Logs**. Each layer narrows focus from abstract identity to concrete daily action, with built-in reflection to prevent self-deception.

## Tech Stack

- **Python 3.10+** / **FastAPI** (async)
- **PostgreSQL** with **AsyncPG** driver
- **SQLAlchemy 2.0** (async ORM) + **Alembic** (migrations)
- **Pydantic v2** (validation & settings)
- **PyJWT** + **Passlib** (auth)
- **Structlog** (structured JSON logging)
- **Poetry** (dependency management)
- **Docker Compose** (PostgreSQL + pgAdmin)

## Quick Start

```bash
# 1. Clone and install
git clone <repo-url> && cd vidhya_api
poetry install

# 2. Configure environment
cp env.example .env
# Edit .env with your database credentials and secrets

# 3. Start PostgreSQL
docker-compose up -d

# 4. Run migrations
alembic -c app/alembic.ini upgrade head

# 5. Start dev server
poetry run uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000` with interactive docs at `/docs`.

## Project Structure

```
app/
├── main.py              # Entry point, middleware, exception handlers
├── apis/                # Routes & response formatting
│   ├── v1/              # Versioned endpoints
│   ├── exceptions.py    # HTTP exception classes
│   └── response.py      # ResponseEntity[T] wrapper
├── core/                # Config, JWT, hashing, logging, middleware
├── db/models/           # SQLAlchemy ORM models
├── services/            # Business logic & Pydantic DTOs
└── migrations/          # Alembic versions
```

## Development

```bash
# Format & lint (run before every commit)
make fmt

# Generate a migration after model changes
alembic -c app/alembic.ini revision --autogenerate -m "description"

# Apply migrations
alembic -c app/alembic.ini upgrade head
```

A pre-commit hook runs `make fmt` automatically on commit.

## API Overview

All responses use a consistent envelope: `{"code", "message", "data", "error"}`.

| Method | Endpoint            | Description          | Auth     |
|--------|---------------------|----------------------|----------|
| GET    | `/api/health`       | Health check + DB    | No       |
| POST   | `/api/v1/user/signup`  | Register a new user  | No       |
| POST   | `/api/v1/user/signin`  | Sign in, get JWT     | No       |
| GET    | `/api/v1/user/me`      | Current user profile | Bearer   |
| POST   | `/api/v1/user/signout` | Invalidate token     | Bearer   |
