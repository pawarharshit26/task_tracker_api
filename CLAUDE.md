# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Server
```bash
uv run uvicorn app.main:app --reload
# or
poetry run uvicorn app.main:app --reload
```

### Database (Docker)
```bash
docker-compose up -d        # Start PostgreSQL + pgAdmin
docker-compose down         # Stop
```

### Migrations (Alembic)
```bash
alembic -c app/alembic.ini upgrade head                                    # Apply pending
alembic -c app/alembic.ini revision --autogenerate -m "description"        # New migration
alembic -c app/alembic.ini downgrade -1                                    # Rollback one
```

### Formatting & Linting
```bash
make fmt                    # black app && ruff check app --fix
```

### Setup (first time)
```bash
./setup.sh                  # Creates venv, installs deps, sets up pre-commit
```

## Architecture

**Pragya API** is a personal growth tracker implementing a strict hierarchy:

**Vision → Themes → Tracks → Goals → Phases → Daily Commitments → Execution Logs**

Each layer narrows from abstract identity to concrete daily action. A user owns one Vision; all other entities cascade from it.

### Layer Responsibilities

| Layer | Location | Role |
|-------|----------|------|
| HTTP | `app/apis/` | Routes, request parsing, exception → HTTP status mapping |
| Service | `app/services/` | Business logic, DTOs, auth dependency |
| DB | `app/db/` | Async SQLAlchemy engine, session, ORM models |
| Core | `app/core/` | Config, JWT, logging, security, HashId, middlewares |

### Request Lifecycle
Request → `RequestIDMiddleware` (UUID per request) → `RequestLoggingMiddleware` → route handler → `Service` → DB → `ResponseEntity[T]` wrapper

All responses follow this structure:
```json
{ "code": 200, "message": "", "data": {...}, "error": null }
```

### Authentication
- JWT payload: `{"sub": {"auth_token": "<random_string>"}}`
- `AuthToken` row in DB links token string to user; deleted on signout
- `get_current_user_id` dependency in `app/services/user.py` validates JWT + DB presence

### ID Obfuscation
Integer PKs are never exposed. `HashId` (a custom Pydantic type in `app/core/hash_ids.py`) auto-converts `int ↔ hash string` during serialization/deserialization. Salt comes from `settings.SECRET_KEY`.

### Model Mixins (`app/db/models/base.py`)
All domain models inherit `CreateUpdateDeleteModel`, which provides:
- `created_at / creator_id / creator`
- `updated_at / updater_id / updater`
- `deleted_at / deleter_id / deleter` (soft delete)

Filter active records with `Model.deleted_at.is_(None)`.

### Exception Pattern
1. Define nested exception classes inside the Service:
   ```python
   class UserService(BaseService):
       class UserNotFoundException(BaseException):
           message = "User Not Found"
   ```
2. Raise in service layer
3. Catch in route, re-raise as `BaseAPIException(message=..., status_code=...)` with `from None`

### Naming Conventions
- DTOs (Pydantic): suffix `Entity` — e.g. `UserSignUpEntity`
- Services: suffix `Service` — e.g. `UserService`
- ORM models: singular PascalCase — e.g. `User`, `Vision`
- Table names: singular snake_case — e.g. `user`, `auth_token`

### Key Files
- Entry point: `app/main.py`
- Settings: `app/core/config.py` (reads `.env`)
- DB session: `app/db/base.py`
- Model mixins: `app/db/models/base.py`
- Auth dependency: `app/services/user.py` → `get_current_user_id`
- Response wrapper: `app/apis/response.py`

### Tech Stack
FastAPI + SQLAlchemy 2.0 async + AsyncPG + PostgreSQL + Pydantic v2 + PyJWT + structlog + Hashids + Alembic

Use `select()` / `delete()` (SQLAlchemy 2.0 style), not the legacy Query API. Use `Mapped[T]` + `mapped_column()` for new models (not `Column()`).
