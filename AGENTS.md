# AGENTS.md - Pragya Task Tracker API

FastAPI + SQLAlchemy 2.0 (async) task tracker with vision/goal tracking system. Python >=3.10, PostgreSQL.

## Commands

### Development
```bash
# Run app
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Format & lint (ALWAYS run before committing)
make fmt                # Auto-format with black + isort + ruff --fix
black app               # Format only
ruff check app --fix    # Lint and fix

# Docker
docker-compose up -d    # Start PostgreSQL + pgAdmin
docker build -t pragya-api . && docker run -p 8000:8000 pragya-api
```

### Database
```bash
alembic revision --autogenerate -m "description"  # Create migration
alembic upgrade head                              # Apply migrations
alembic downgrade -1                              # Rollback one
```

### Testing (NOT IMPLEMENTED YET)
```bash
pytest                                  # Run all tests
pytest tests/unit/test_user_service.py  # Single file
pytest tests/unit/test_user_service.py::test_create_user  # Single test
pytest --cov=app --cov-report=html      # With coverage
```

## Architecture

**Layered:** Route → Service → Database

```
app/
├── main.py              # FastAPI app, middleware
├── apis/                # API routes (controllers)
│   ├── v1/user.py       # /api/v1/user/* endpoints
│   ├── exceptions.py    # HTTP exceptions
│   └── response.py      # ResponseEntity[T] wrapper
├── core/                # Config, JWT, security, logging, middleware
├── db/
│   ├── base.py          # SQLAlchemy engine, session
│   └── models/          # ORM models (User, Vision, Goal, etc.)
├── services/            # Business logic (UserService, etc.)
└── migrations/          # Alembic migrations
```

## Code Style

### Imports (CRITICAL: Always use this structure)
```python
# Block 1: Standard library (alphabetical)
import secrets
from datetime import datetime, timedelta
from typing import Annotated

# Block 2: Third-party (alphabetical)
import structlog
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Block 3: Local absolute imports (alphabetical)
from app.apis.exceptions import BaseAPIException
from app.core.config import settings
from app.services.user import UserService
```

**Rules:**
- NEVER use relative imports (`from .module import`)
- Black (line length 88) + isort (Black profile) + Ruff
- Always alphabetical within blocks

### Type Annotations (REQUIRED everywhere)
```python
# Functions
async def create_user(self, input: UserSignUpEntity) -> UserTokenEntity:
    ...

# SQLAlchemy 2.0 mapped columns
user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
title: Mapped[str] = mapped_column(String, nullable=False)

# FastAPI dependencies
async def signup(
    data: UserSignUpEntity,
    service: Annotated[UserService, Depends(get_user_service)]
):
    ...

# Use Python 3.10+ syntax: str | None (not Optional[str])
```

### Naming Conventions
- Functions: `snake_case` (`create_user`, `get_db`)
- Classes: `PascalCase` (`UserService`, `BaseAPIException`)
- Pydantic entities: `*Entity` suffix (`UserSignUpEntity`)
- Services: `*Service` suffix (`UserService`)
- Exceptions: `*Exception` suffix (`UserNotFoundException`)
- Variables: `snake_case` (`auth_token`, `user_id`)
- Constants: `UPPER_SNAKE_CASE` (`JWT_SECRET`)
- Booleans: `is_*` prefix (`is_active`, `is_deleted`)

### Error Handling (Hierarchical)
```python
# 1. Define nested exceptions in service
class UserService(BaseService):
    class UserException(BaseException):
        message = "User Exception"
    
    class UserNotFoundException(UserException):
        message = "User Not Found"

# 2. Raise in service
async def create_user(self, input: UserSignUpEntity) -> UserTokenEntity:
    if existing_user:
        raise self.UserAlreadyExistsException()

# 3. Catch and re-raise in route with HTTP status
@user_router.post("/signup")
async def signup(data: UserSignUpEntity, service: Annotated[UserService, Depends(get_user_service)]):
    try:
        user = await service.create_user(data)
        return ResponseEntity[UserTokenEntity](data=user)
    except UserService.UserAlreadyExistsException as e:
        raise BaseAPIException(
            message=str(e.message), 
            status_code=status.HTTP_400_BAD_REQUEST
        ) from None  # Always use 'from None' to suppress exception chain
```

### Database Patterns
```python
# SELECT
query = select(User).where(User.email == email, User.is_active.is_(True))
result = await self.db.execute(query)
user = result.scalar_one_or_none()

# INSERT
user = User(email=input.email, name=input.name)
self.db.add(user)
await self.db.commit()
await self.db.refresh(user)  # Get generated fields

# Model inheritance - use CreateUpdateDeleteModel for audit trails
class User(CreateUpdateDeleteModel):
    __tablename__ = "user"
    # Auto-includes: id, created_at, updated_at, deleted_at, creator_id, updater_id, deleter_id
```

### Logging (structlog)
```python
import structlog
logger = structlog.get_logger(__name__)

logger.info("Creating user", email=input.email)
logger.info("User created", user_id=user.id, email=user.email)
# Never use print() or standard logging module
```

## Critical Rules

1. **NEVER use relative imports** - always `from app.module import`
2. **ALWAYS add type hints** - functions, variables, SQLAlchemy columns
3. **ALWAYS use async/await** - this is an async-first codebase
4. **ALWAYS use soft deletes** - set `deleted_at`, don't actually delete rows
5. **ALWAYS use ResponseEntity[T]** wrapper for API responses
6. **ALWAYS use Annotated[Type, Depends()]** for dependency injection
7. **ALWAYS use structlog** for logging, not `print()` or `logging`
8. **ALWAYS run `make fmt`** before committing code
9. **ALWAYS handle exceptions** in routes with try-except and map to HTTP status codes
10. **ALWAYS use `from None`** when re-raising exceptions to suppress chain

## Environment Variables

In `.env` (see `env.example`): `DATABASE_URL`, `JWT_SECRET`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `HASHIDS_SALT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`

## Health Check

```bash
curl http://localhost:8000/api/health  # {"message": "ok"}
```
