# FAST-API-BEYOND-CRUD

A deep-dive, end-to-end exploration of FastAPI beyond simple CRUD examples — a hands-on project that demonstrates both minimal FastAPI usage and a more structured, production-oriented application shaped around a book-review service ("Bookly"). It contains example endpoints, an in-repo in-memory dataset, and a more complete package under `src/` with async DB initialization, routing modules, config via environment, error handlers, middleware and support code.

---

## Stack
- **Language(s):** Python (primary)
- **Framework / runtime:** FastAPI + Uvicorn
- **Notable libraries (observed from code):**
  - sqlmodel / SQLAlchemy (async engine usage in `src/db/main.py`)
  - pydantic / pydantic-settings (settings in `src/config.py`)
  - FastAPI middleware, custom error handlers (in `src/middleware.py`, `src/errors.py`)
  - Alembic indicated by `alembic.ini` and `migrations/` (DB migrations)

---

## Repository layout (annotated top-level tree)

```
./
  .gitignore                 # standard ignore file
  alembic.ini                # Alembic config for migrations
  db.py                      # small in-memory books dataset (used by top-level quick demo)
  main.py                    # quick demo app and minimal CRUD sample endpoints
  migrations/                # alembic migrations (directory present)
  requirements.txt           # requirements file (currently empty in repo)
  src/                       # structured application package (Bookly)
    __init__.py              # app factory, lifespan, router includes (Bookly API)
    config.py                # settings (env-driven) via pydantic-settings
    db/                      # database helpers (async SQLModel/SQLAlchemy engine)
      main.py                # async engine, initdb(), get_session() dependency
    books/                   # domain module for books (routes, models, service, data)
      book_data.py
      model.py
      routes.py
      schema.py
      service.py
    auth/                    # router for auth (present as package)
    reviews/                 # router for reviews (present as package)
    tags/                    # router for tags (present as package)
    errors.py                # custom exceptions and centralized error handlers
    middleware.py            # custom middleware + registration helper
    mail.py                  # utilities for sending mail (mail config used in config.py)
  test.py                    # placeholder or test script (empty)
```

Notes:
- The repository contains two entry points:
  - `main.py` — a short, example FastAPI app with quick demonstration endpoints (greeting, headers, in-memory users/books CRUD).
  - `src` package — a more organized API with routers and async DB initialization intended to run as `Bookly` (real-world style app).
- Alembic and migrations are present for database migrations; `src/db/main.py` uses SQLModel/async engine, so migrations + async DB are expected in a deployed setup.

---

## How it fits together (runtime shape)
- The `src` package builds a FastAPI app (`app`) with a lifespan event that calls `initdb()` to initialize the DB schema (in `src/db/main.py`), then registers middleware and custom error handlers.
- Routers are composed and included under path prefixes like `/api/1.0.0/books`, `/api/1.0.0/auth`, `/api/1.0.0/reviews`, `/api/1.0.0/tags` (see `src/__init__.py`).
- `src/config.py` loads environment-driven settings (DB URL, Redis, mail and JWT config). Database sessions are provided by `get_session()` (async session dependency).
- `main.py` (root) provides a lightweight set of endpoints that operate on the in-repo `db.py` dataset (a static list of books) for quick demonstrations and learning — useful when you want to try FastAPI primitives rapidly.

---

## Key endpoints (examples found in the repo)

Top-level demo app (`main.py`):
- `GET /` — Hello world
- `GET /greet/{username}` — path param greeting
- `GET /search?username=...` — simple search demo
- `GET /greet/` — optional query param greeting (`?username=...`)
- `POST /create_user` — accepts JSON body with `{ "username", "email" }`
- `GET /get_headers` — returns several request headers
- Books demo (in-memory, backed by `db.py`):
  - `GET /books` — list all books
  - `POST /books` — create a book (Book model used)
  - `GET /book/{book_id}` — retrieve a book by id
  - `PATCH /book/{book_id}` — partial update (uses BookUpdateModel)
  - `DELETE /book/{book_id}` — delete (204 No Content)

Structured app (Bookly) under `src/`:
- App is mounted with prefixes like `/api/1.0.0/books`, `/api/1.0.0/auth`, `/api/1.0.0/reviews`, `/api/1.0.0/tags`. Each of these routers is implemented inside the corresponding package directory (e.g. `src/books/routes.py`). The `src/books` module includes models, schemas, service layer and sample data.

---

## Configuration / Environment variables

`src/config.py` defines the settings expected to be present (via `.env` or environment):

- `DATABASE_URL`: str (e.g. `postgresql+asyncpg://user:pass@host/dbname`)
- `JWT_SECRET`: str
- `JWT_ALGORITHM`: str
- `REDIS_HOST`, `REDIS_PORT`, `REDIS_USERNAME`, `REDIS_PASSWORD`
- `REDIS_DECODE_RESPONSES`: bool
- `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_FROM`, `MAIL_PORT`, `MAIL_SERVER`, `MAIL_FROM_NAME`
- `MAIL_STARTTLS` (default True), `MAIL_SSL_TLS` (default False), `USE_CREDENTIALS` (True), `VALIDATE_CERTS` (True)
- `DOMAIN`

The settings object reads `.env` by default (see `model_config` in `src/config.py`).

---

## Database & Migrations

- `src/db/main.py` sets up an asynchronous SQLModel/SQLAlchemy engine using `Config.DATABASE_URL` and exposes:
  - `initdb()` — runs `SQLModel.metadata.create_all` asynchronously (called on server lifespan start).
  - `get_session()` — async session dependency (sessionmaker with `AsyncSession`).
- `alembic.ini` and a `migrations/` directory are present — Alembic is intended for versioned migrations. If you use a SQL database (Postgres/MySQL/etc.), you should configure `DATABASE_URL` and run Alembic commands to stamp/upgrade migrations.

---

## Installation & running (quick start)

1. Clone the repo:

```bash
git clone https://github.com/thisIsOwais/FAST-API-BEYOND-CRUD.git
cd FAST-API-BEYOND-CRUD
```

2. Create a virtual environment and install dependencies.
   The repository's `requirements.txt` is currently empty — install the packages used by the project (example list):
   - fastapi
   - uvicorn[standard]
   - sqlmodel
   - sqlalchemy (with async drivers if needed)
   - pydantic-settings (pydantic v2 settings)
   - alembic
   - fastapi-mail (if mail utilities used)
   - redis (if using Redis)

Example:

```bash
python -m venv .venv
source .venv/bin/activate
pip install "fastapi" "uvicorn[standard]" "sqlmodel" "pydantic-settings" "alembic" "fastapi-mail" "redis"
```

3. Provide environment variables (create a `.env` in project root) with at least:

```
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
JWT_SECRET=your-secret
JWT_ALGORITHM=HS256
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DECODE_RESPONSES=true
MAIL_USERNAME=...
MAIL_PASSWORD=...
MAIL_FROM=...
MAIL_PORT=587
MAIL_SERVER=smtp.example.com
MAIL_FROM_NAME="Bookly"
DOMAIN=example.com
```

4. Run the minimal demo app (uses top-level `main.py` and in-memory data):

```bash
uvicorn main:app --reload
```

Visit: http://127.0.0.1:8000/docs

5. Run the structured `Bookly` app (recommended for full features):

```bash
uvicorn src:app --reload
```

This app triggers `initdb()` on startup (it will attempt to create SQLModel tables using the configured DB). Visit the OpenAPI docs under: http://127.0.0.1:8000/docs

6. Alembic migrations:

- Configure `alembic.ini` to point to your `DATABASE_URL` or set env var and run typical alembic commands:

```bash
alembic revision --autogenerate -m "Create initial tables"
alembic upgrade head
```

---

## API examples (curl)

- List demo books (top-level main.py):

```bash
curl http://127.0.0.1:8000/books
```

- Create book (demo):

```bash
curl -X POST http://127.0.0.1:8000/books \
  -H "Content-Type: application/json" \
  -d '{"id": 7, "title": "New Book", "author":"Author", "publisher":"Pub", "published_date":"2026-01-01","page_count":100,"language":"English"}'
```

- Get Bookly (structured app) routes:
  - Base for routes: `/api/1.0.0/` — for example, `/api/1.0.0/books` — open `/docs` for automatic OpenAPI listing.

---

## Project notes, observations & suggestions

- The repository includes both a teaching/demo `main.py` and a structured package under `src/`. Use the demo file to learn FastAPI basics quickly; use the `src` package when you want to explore a more production-like setup (async SQLModel engine, routers, middleware, error handlers).
- `requirements.txt` is empty — add pinned dependencies to ensure reproducible installs.
- `src/config.py` is ready for secure configuration via environment `.env` files. Be sure to secure secrets (JWT_SECRET, mail and redis credentials) and not check them into version control.
- `src/errors.py` centralizes API error responses — a good pattern for consistent client-facing messages.
- `src/db/main.py` uses an async engine and `SQLModel.metadata.create_all` on startup. For production use you should rely on Alembic migrations rather than `create_all()`, and avoid automatic schema changes at runtime.

---

## Contributing

- Run tests or manual checks (there are no explicit tests in the repo as-is).
- Add dependencies to `requirements.txt` with pinned versions.
- If adding DB models, create corresponding Alembic revisions and document migration steps.
- Keep secrets and sensitive configuration out of the repository; use environment variables or secret managers.

---

## Troubleshooting checklist

- "App fails to connect to DB" — check `DATABASE_URL` in `.env`; confirm DB accepts async connections (asyncpg for Postgres).
- "Routes missing/404" — confirm you are running the intended app:
  - demo: `uvicorn main:app --reload`
  - structured: `uvicorn src:app --reload`
- "Migrations not applied" — make sure Alembic is configured and run `alembic upgrade head`.
- "Mail/Redis errors" — verify mail server and Redis credentials and connectivity.

---

## Final thoughts

This repository is both a learning playground (top-level `main.py` demonstrates many FastAPI features: path/query params, request bodies, headers, models, status codes) and a scaffold for a modular, async FastAPI service (`src/` with config, async DB, routers, middlewares and centralized error handling). It is well-positioned for expansion: add tests, populate `requirements.txt`, document deployment and CI, and scaffold Alembic migrations for safe schema changes.

---

If you'd like, I can:
- create a PR adding this `README.md` to the repo,
- generate a recommended `requirements.txt` with pinned versions,
- or produce a quick-start `.env.example` and Alembic instructions tailored to Postgres.
