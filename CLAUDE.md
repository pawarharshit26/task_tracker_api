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

Filter active records with `Model.deleted_at.is_(None)`. The `creator_id`, `updater_id`, `deleter_id` fields are **not auto-populated** — set them explicitly in service methods using the authenticated `user_id`.

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
- Router registration: `app/apis/v1/base.py` — add new routers here

### Tech Stack
FastAPI + SQLAlchemy 2.0 async + AsyncPG + PostgreSQL + Pydantic v2 + PyJWT + structlog + Hashids + Alembic

Use `select()` / `delete()` (SQLAlchemy 2.0 style), not the legacy Query API. Use `Mapped[T]` + `mapped_column()` for new models (not `Column()`).

## Domain Model Semantics

All models are defined; only **User** has a service and API. The rest need to be built following the same pattern.

| Model | Constraint / Intent |
|-------|---------------------|
| `Vision` | Identity anchor. One active per user (`user_id` is unique). Rarely changes. |
| `Theme` | Life domain (Health, Career, etc.). 3–6 active per Vision max. |
| `Track` | Skill/focus area within a Theme (e.g. "Backend Engineering"). Can be paused. |
| `Goal` | Outcome direction for a Track. Multiple per Track, few active at once. |
| `Phase` | Time-boxed focus (with `start_date` / `end_date`). **Only 1 active Phase per Goal**. |
| `DailyCommitment` | Intent set at day start. Belongs to one Phase. Can be skipped but must be logged. |
| `ExecutionLog` | What actually happened. 1-to-1 with `DailyCommitment` (`commitment_id` is unique). Has `actual_output` + `reflection` text fields. |

## Adding a New Feature (Pattern)

Follow `app/services/user.py` + `app/apis/v1/user.py` as the reference implementation:

1. **Service** (`app/services/<entity>.py`): subclass `BaseService`, define inner exception classes, implement async methods, expose `get_<entity>_service(db) -> <Entity>Service` factory.
2. **Router** (`app/apis/v1/<entity>.py`): `APIRouter`, inject service via `Depends(get_<entity>_service)` and user via `Depends(get_current_user_id)`, map service exceptions to `BaseAPIException`.
3. **Register**: add router in `app/apis/v1/base.py`.
4. **Migration**: run `alembic revision --autogenerate` if models changed.
