# Aye House API

FastAPI backend with Vertical Slice Architecture.

## Quick Start

Requires Python 3.12+, [uv](https://docs.astral.sh/uv/) and PostgreSQL (via Docker or a
local install; see [Setup](#setup) for both options).

```bash
# 1. Start PostgreSQL (from the repository root). Skip if you use a local PostgreSQL.
docker pull postgres:18.3
docker compose up -d db

# 2. Install, configure, migrate and run (from backend/)
cd backend
uv sync --extra dev
cp .env.example .env          # with a local PostgreSQL, edit DATABASE_URL here
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

Open http://localhost:8000/docs.

## Architecture

This project follows **Vertical Slice Architecture**, where features are organized as self-contained modules containing all their components (routes, handlers, models, schemas, repositories, services) rather than traditional layered architecture.

```
app/
├── core/                 # Shared core functionality
│   ├── config.py         # Application settings
│   ├── database.py       # Database configuration
│   ├── exceptions.py     # Custom exceptions
│   └── security.py       # Security utilities
├── features/             # Feature slices (vertical slices)
│   ├── health/           # Health check feature
│   │   ├── router.py     # API routes
│   │   └── schemas.py    # Pydantic schemas
│   └── users/            # Users feature
│       ├── models.py     # SQLAlchemy models
│       ├── schemas.py    # Pydantic schemas
│       ├── repository.py # Data access layer
│       ├── service.py    # Business logic
│       ├── dependencies.py # FastAPI dependencies
│       └── router.py     # API routes
├── main.py               # Application entry point
└── __init__.py
```

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Docker (for PostgreSQL), or a local PostgreSQL 15+ instance

## Setup

1. **Start PostgreSQL** — either with Docker or a local install.

   **Option A: Docker** (from the repository root):
   ```bash
   docker pull postgres:18.3   # once; docker-compose.yml uses pull_policy: never
   docker compose up -d db
   ```
   This creates user `postgres` / password `postgres` and database `aye_house`,
   which matches the default `DATABASE_URL`, so no extra configuration is needed.

   **Option B: Local PostgreSQL (no Docker)**

   Install PostgreSQL 15+ ([Windows installer](https://www.postgresql.org/download/windows/),
   `brew install postgresql` on macOS, `apt install postgresql` on Debian/Ubuntu) and make
   sure the service is running. Then create a user and database with `psql`:
   ```bash
   psql -U postgres
   ```
   On Windows, if `psql` is not recognized, add `C:\Program Files\PostgreSQL\<version>\bin`
   to your `PATH` or use the "SQL Shell (psql)" app that ships with the installer.
   ```sql
   CREATE USER aye_house WITH PASSWORD 'aye_house';
   CREATE DATABASE aye_house OWNER aye_house;
   \q
   ```
   Point `DATABASE_URL` in `.env` (step 3) at it:
   ```env
   DATABASE_URL="postgresql+asyncpg://aye_house:aye_house@localhost:5432/aye_house"
   ```
   The format is `postgresql+asyncpg://<user>:<password>@<host>:<port>/<database>`.
   The `+asyncpg` driver part is required. Characters such as `@`, `:` or `/` in the
   password must be URL-encoded (e.g. `@` → `%40`). If you'd rather reuse the
   `postgres` superuser, just create the database (`CREATE DATABASE aye_house;`) and
   set your own password in the URL.

   Either way, the app connects on startup and fails with
   `Connect call failed ('127.0.0.1', 5432)` if the database is not reachable.
   Alembic reads the same `DATABASE_URL` (or `ALEMBIC_DATABASE_URL`, if set).

2. **Install dependencies** (inside `backend/`):
   ```bash
   cd backend
   uv sync --extra dev
   ```
   Dev tools are declared under `[project.optional-dependencies]`, so they need
   `--extra dev`; `uv sync --dev` would uninstall them.

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run database migrations:**
   ```bash
   uv run alembic upgrade head
   ```

5. **Start development server:**
   ```bash
   uv run uvicorn app.main:app --reload
   ```
   Always prefix commands with `uv run` so they use the project's `.venv`
   instead of the global Python. (`fastapi dev` is not available because
   `fastapi[standard]` is not installed.)

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `uv sync --dev` uninstalls pytest, ruff, mypy… | Dev tools are an extra, not a dependency group. Use `uv sync --extra dev`. |
| `To use the fastapi command, please install "fastapi[standard]"` | `fastapi dev` is not supported. Use `uv run uvicorn app.main:app --reload`. |
| `uvicorn` / `alembic` not recognized, or they run from the global Python | Prefix every command with `uv run` so it uses the project's `.venv`. |
| `Connect call failed ('127.0.0.1', 5432)` on startup | PostgreSQL is not running or `DATABASE_URL` is wrong. Start it (`docker compose up -d db` or the local service) and check `.env`. |
| `docker compose up` fails with an image not found error | `docker-compose.yml` uses `pull_policy: never`. Run `docker pull postgres:18.3` first. |
| `password authentication failed` | User or password in `DATABASE_URL` doesn't match PostgreSQL. URL-encode special characters in the password. |

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Zones

Provinces, municipalities and neighborhoods are fixed reference data: the API only
exposes them for reading. They are defined in `app/features/zones/seed_data.py` and
loaded with an idempotent seeder (it only inserts missing entries, so re-run it after
editing the data file):

```bash
uv run python -m app.cli seed-zones
```

For now all provinces are loaded, but only La Habana has municipalities and neighborhoods.

## Authentication

JWT bearer tokens (OAuth2 password flow), passwords hashed with argon2.

```bash
# Create the first superuser (or promote an existing email); prompts for the password
uv run python -m app.cli create-superuser --email admin@example.com --username admin

# Log in with email or username (form data) to get a token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=admin&password=<password>"

# Call protected endpoints
curl http://localhost:8000/api/v1/users/me -H "Authorization: Bearer <access_token>"
```

In Swagger UI, use the **Authorize** button to log in. Protect a route with the
`CurrentUserDep` or `SuperUserDep` dependencies from `app/features/users/dependencies.py`.
`SECRET_KEY` must be set when `ENVIRONMENT=production`, otherwise the app refuses to start.

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_health.py
```

## Code Quality

```bash
# Format code
uv run ruff format

# Lint code
uv run ruff check

# Type check
uv run mypy app
```

## Adding New Features

1. Create a new directory under `app/features/`:
   ```bash
   mkdir app/features/your_feature
   ```

2. Create the feature components:
   - `models.py` - SQLAlchemy models
   - `schemas.py` - Pydantic request/response schemas
   - `repository.py` - Data access layer
   - `service.py` - Business logic
   - `dependencies.py` - FastAPI dependencies (if needed)
   - `router.py` - API routes
   - `__init__.py` - Export router

3. Register the router in `app/main.py`:
   ```python
   from app.features.your_feature import your_feature_router
   
   app.include_router(your_feature_router, prefix=settings.api_prefix)
   ```

## Project Structure Details

### Core Module

The `core` module contains shared functionality used across all features:

- **config.py**: Pydantic Settings for environment-based configuration
- **database.py**: Async SQLAlchemy engine, session management, and lifecycle
- **exceptions.py**: Custom exception classes with consistent error responses
- **security.py**: Password hashing and JWT token management

### Feature Slices

Each feature is a self-contained vertical slice:

- **Router**: Defines API endpoints using FastAPI's APIRouter
- **Schemas**: Pydantic models for request/response validation
- **Models**: SQLAlchemy ORM models
- **Repository**: Data access abstraction layer
- **Service**: Business logic layer
- **Dependencies**: FastAPI dependency injection for the feature

### Benefits of Vertical Slice Architecture

1. **High Cohesion**: Related code stays together
2. **Low Coupling**: Features don't depend on each other
3. **Scalability**: Easy to add/remove features
4. **Testability**: Each feature can be tested in isolation
5. **Maintainability**: Changes to one feature don't affect others

## Environment Variables

See `.env.example` for all available configuration options.

## License

MIT