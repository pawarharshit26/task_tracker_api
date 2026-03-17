# Pragya API - Agent & Developer Guide

## Build / Run / Lint / Test Commands

```bash
# Install dependencies
poetry install

# Start database (PostgreSQL + pgAdmin)
docker-compose up -d

# Run database migrations (run from repo root; alembic.ini is in app/)
alembic -c app/alembic.ini upgrade head

# Generate a new migration after model changes
alembic -c app/alembic.ini revision --autogenerate -m "description"

# Start dev server (from repo root)
poetry run uvicorn app.main:app --reload

# Format & lint (always run before committing)
make fmt                     # runs: black app && ruff check app --fix

# Format only
black app

# Lint only (with autofix)
ruff check app --fix

# Lint without autofix (check mode)
ruff check app

# Tests — not yet configured. When added, the convention will be:
# pytest                           # run all tests
# pytest tests/test_user.py        # run a single test file
# pytest tests/test_user.py::test_signup -v   # run a single test function
```

## Project Structure

```
app/
├── main.py                  # FastAPI app entry point, exception handlers, middleware
├── apis/                    # API layer — routes, response format, HTTP exceptions
│   ├── base.py              # Root /api router, health check
│   ├── exceptions.py        # BaseAPIException, UnauthorizedException
│   ├── response.py          # ResponseEntity[T] generic response wrapper
│   └── v1/
│       ├── base.py          # /api/v1 sub-router, mounts feature routers
│       └── user.py          # User endpoints (signup, signin, me, signout)
├── core/                    # Cross-cutting utilities
│   ├── config.py            # Pydantic Settings (reads .env)
│   ├── exceptions.py        # BaseException (project-wide base)
│   ├── hash_ids.py          # HashId type (int ↔ obfuscated string in API)
│   ├── jwt.py               # JWT encode/decode helper class
│   ├── logging.py           # Structlog setup, request_id context var
│   ├── middlewares.py       # RequestIDMiddleware, RequestLoggingMiddleware
│   └── security.py          # Password hashing (passlib bcrypt_sha256)
├── db/
│   ├── base.py              # Async engine, session factory, get_db dependency
│   └── models/              # SQLAlchemy ORM models
│       ├── base.py          # BaseModel, CreateModel, UpdateModel, DeleteModel mixins
│       ├── user.py          # User, AuthToken
│       ├── vision.py        # Vision (identity anchor)
│       ├── theme.py         # Theme (life domain)
│       ├── track.py         # Track (skill/focus area)
│       ├── goal.py          # Goal (outcome-oriented)
│       ├── phase.py         # Phase (time-boxed)
│       ├── daily_commitment.py
│       └── execution_log.py
├── services/                # Business logic layer
│   ├── base.py              # BaseService(db), BaseEntity(BaseModel)
│   └── user.py              # UserService + Pydantic DTOs + get_current_user_id
└── migrations/              # Alembic migration versions
```

## Code Style Guidelines

### Formatter & Linter Config
- **Black**: line length 88, target Python 3.10
- **Ruff**: rules E, F, W, C, B, RUF, I; line length 88; E501 ignored (Black handles it)
- **Isort**: profile "black", trailing commas, `app` as known first-party
- Migrations directory is excluded from all linters

### Import Order (enforced by isort + ruff I)
1. Standard library (`datetime`, `typing`, `uuid`, etc.)
2. Third-party (`fastapi`, `sqlalchemy`, `structlog`, `pydantic`, etc.)
3. First-party (`app.core.*`, `app.db.*`, `app.apis.*`, `app.services.*`)

Separate each group with a blank line. Use absolute imports from `app.*` — never relative imports.

### Type Annotations
- Use `Annotated[Type, Depends(...)]` for FastAPI dependency injection parameters.
- Use Pydantic `BaseModel` subclasses for request/response schemas (called "Entities" here: `UserSignUpEntity`, `UserEntity`, etc.).
- Use `str | None` union syntax (Python 3.10+), not `Optional[str]`.
- SQLAlchemy models use `Mapped[T]` with `mapped_column()` for newer models (vision, theme, track, goal, phase) and legacy `Column()` style for older ones (user). Prefer `Mapped` + `mapped_column` for new code.

### Naming Conventions
- **Files**: `snake_case.py`
- **Classes**: `PascalCase` — `UserService`, `BaseAPIException`, `ResponseEntity`
- **Functions/methods**: `snake_case` — `get_user`, `create_auth_token`
- **Route functions**: `snake_case` matching the action — `signup`, `signin`, `me`
- **Constants**: `UPPER_SNAKE_CASE` (in config: `JWT_SECRET`, `DATABASE_URL`)
- **Pydantic DTOs**: suffix `Entity` — `UserSignUpEntity`, `UserTokenEntity`
- **Service classes**: suffix `Service` — `UserService`
- **Exception classes**: nested inside their Service class — `UserService.UserNotFoundException`
- **SQLAlchemy models**: singular PascalCase matching table name — `User`, `AuthToken`, `Vision`
- **Table names**: singular snake_case — `user`, `auth_token`, `vision`

### Error Handling Pattern
1. Define custom exceptions as **nested classes** inside the relevant Service, inheriting from a base service exception:
   ```python
   class UserService(BaseService):
       class UserException(BaseException):
           message = "User Exception"
       class UserNotFoundException(UserException):
           message = "User Not Found"
   ```
2. **Raise** exceptions in the service layer with a descriptive `message`.
3. **Catch** service exceptions in the API route and re-raise as `BaseAPIException` with the appropriate HTTP status code:
   ```python
   except UserService.UserNotFoundException as e:
       raise BaseAPIException(message=str(e.message), status_code=status.HTTP_404_NOT_FOUND) from None
   ```
4. Use `from None` to suppress exception chaining in API handlers.

### Response Format
All endpoints return `ResponseEntity[T]` — a generic Pydantic model:
```json
{"code": 200, "message": "", "data": { ... }, "error": null}
```

### Authentication Flow
- JWT tokens encode `{"sub": {"auth_token": "<random_string>"}}`.
- `get_current_user_id` dependency extracts the bearer token, decodes JWT, looks up `AuthToken` in DB, and returns `user_id: int`.
- Use `HashId` (in `core/hash_ids.py`) to obfuscate integer IDs in API responses.

### Logging
- Use `structlog.get_logger(__name__)` at module level.
- Log key events: `logger.info("action_name", key=value)`.
- Request ID is automatically injected via middleware.

### Database Conventions
- All DB operations are **async** (`await db.execute(...)`, `await db.commit()`).
- Sessions come from `get_db` dependency injection — never create sessions manually.
- Use `select()`, `delete()` from `sqlalchemy` — not legacy `Query` API.
- New models must inherit from `CreateUpdateDeleteModel` (provides `created_at`, `updated_at`, `deleted_at` + creator/updater/deleter FK fields).
- Soft-delete: filter with `Model.deleted_at.is_(None)` for active records.
- Always create Alembic migrations — never modify schema manually.

## Adding a New Feature (Checklist)

1. Define SQLAlchemy model in `app/db/models/` (inherit `CreateUpdateDeleteModel`)
2. Register model in `app/db/models/__init__.py` with explicit re-export
3. Generate migration: `alembic -c app/alembic.ini revision --autogenerate -m "add <feature>"`
4. Create Pydantic DTOs (Entities) in the service file
5. Create Service class in `app/services/` extending `BaseService`
6. Create API routes in `app/apis/v1/<feature>.py`
7. Register router in `app/apis/v1/base.py`
8. Run `make fmt` before committing
