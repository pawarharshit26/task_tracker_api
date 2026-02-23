# Pragya API (Task Tracker) - Developer & Agent Guide

This document serves as a comprehensive guide for developers and AI agents working on the Pragya API codebase. It outlines the project structure, architectural patterns, technology stack, and operational workflows.

## 1. Project Overview

**Name:** Pragya API
**Purpose:** Backend API for a Task Tracker application.
**Status:** In active development (User Management implemented; Task Management pending).

## 2. Tech Stack

*   **Language:** Python 3.10+
*   **Web Framework:** **FastAPI** (Async)
*   **Database:** **PostgreSQL**
*   **ORM:** **SQLAlchemy** (Async)
*   **Database Driver:** **AsyncPG**
*   **Migrations:** **Alembic**
*   **Validation:** **Pydantic**
*   **Authentication:** **PyJWT** (JWT), **Passlib** (Hashing)
*   **Logging:** **Structlog** (JSON structured logs)
*   **Dependency Management:** **Poetry**
*   **Linting/Formatting:** **Black**, **Ruff**, **Isort**

## 3. Project Structure

The project follows a modular structure within the `app/` directory:

```
app/
├── apis/               # API Layer (Controllers/Routes)
│   ├── base.py         # Main router configuration
│   ├── exceptions.py   # Global exception handling logic
│   ├── response.py     # Standardized API response format (ResponseEntity)
│   └── v1/             # Version 1 endpoints
│       └── user.py     # User-related routes (signup, signin, me)
├── core/               # Core configuration & utilities
│   ├── config.py       # Pydantic Settings (env vars)
│   ├── logging.py      # Structlog setup
│   ├── security.py     # Auth utilities (password hashing, JWT)
│   └── middlewares.py  # Request logging, ID tracking
├── db/                 # Database Layer
│   ├── base.py         # DB connection & session management
│   └── models/         # SQLAlchemy models (User, Task, etc.)
├── services/           # Service Layer (Business Logic)
│   └── user.py         # User management logic (CRUD, Auth)
├── migrations/         # Alembic migration scripts
└── main.py             # Application entry point
```

## 4. Key Architectural Patterns

### Service-Repository Pattern
*   **API Layer (`app/apis/`)**: Handles HTTP requests, validation (Pydantic), and response formatting. It delegates business logic to the Service Layer.
*   **Service Layer (`app/services/`)**: Contains all business logic. It interacts directly with the database using SQLAlchemy sessions.
    *   **Dependency Injection**: Services are injected into API routes using FastAPI's `Depends`.
    *   **Transactional**: Service methods typically handle transaction commit/rollback (implicit via `AsyncSession` context or explicit management).

### Database Access
*   **Async SQLAlchemy**: All database operations are asynchronous.
*   **Session Management**: A database session is provided via dependency injection (`get_db`) to routes and passed down to services.

### Authentication
*   **JWT**: Stateless authentication using JSON Web Tokens.
*   **Current User**: A dependency `get_current_user` extracts the user from the token.

### Standardized Response
*   All API responses are wrapped in a generic `ResponseEntity` class to ensure a consistent JSON structure (e.g., `{ "code": 200, "message": "Success", "data": ... }`).

### Logging
*   **Structlog**: Used for structured, context-rich logging.
*   **Request ID**: A unique ID is generated for each request and included in logs for traceability.

## 5. Development Workflow

### Prerequisites
*   Python 3.10+
*   Poetry
*   Docker & Docker Compose (for database)

### Setup
1.  **Install Dependencies:**
    ```bash
    poetry install
    ```
2.  **Start Database:**
    ```bash
    docker-compose up -d
    ```
3.  **Run Migrations:**
    ```bash
    alembic upgrade head
    ```

### Running the Application
To start the development server with hot reload:
```bash
poetry run uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.
Docs are at `http://localhost:8000/docs`.

### Code Quality
Run the following command to format and lint code:
```bash
make fmt
```
(This runs `black` and `ruff` on the `app/` directory).

### Testing
*   **Status:** Test infrastructure is currently not set up.
*   **Goal:** Implement `pytest` for unit and integration tests.

## 6. Common Tasks for Agents

*   **Adding a New Feature:**
    1.  Define the **SQLAlchemy Model** in `app/db/models/`.
    2.  Generate a **Migration** (`alembic revision --autogenerate -m "add feature"`).
    3.  Create a **Service** in `app/services/` to handle logic.
    4.  Create a **Pydantic Schema** (DTO) for request/response.
    5.  Create an **API Route** in `app/apis/v1/`.
    6.  Register the router in `app/apis/base.py` (or `v1/base.py`).

*   **Modifying Database Schema:**
    *   Always use Alembic migrations. Never modify the database schema manually.

*   **Error Handling:**
    *   Raise custom exceptions in the Service layer.
    *   Catch them in the API layer and re-raise as `BaseAPIException` or use the global exception handler.
