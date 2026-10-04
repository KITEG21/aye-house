# Aye House API

FastAPI backend with Vertical Slice Architecture.

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
- PostgreSQL 15+
- uv (recommended) or pip

## Setup

1. **Clone and navigate to backend:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   uv sync --dev
   # or
   pip install -e ".[dev]"
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Start development server:**
   ```bash
   uv run fastapi dev app/main.py
   # or
   uvicorn app.main:app --reload
   ```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

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