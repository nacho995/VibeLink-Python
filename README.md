# VibeLink Backend

Backend for VibeLink, a dating app that matches people based on shared interests in movies, series, music, and games.

Built with FastAPI + PostgreSQL (async). This is a rewrite of the original .NET version into Python.

## Tech Stack

- **FastAPI** with async/await
- **PostgreSQL** via SQLAlchemy + asyncpg
- **Alembic** for migrations
- **JWT** auth (python-jose)
- **Stripe** for payments
- **Docker** ready for production

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your values.

```bash
cp .env.example .env
```

Run the server:

```bash
uvicorn app.main:app --reload
```

Docs available at `/swagger` in dev mode.

## Docker

```bash
docker build -t vibelink-backend .
docker run -p 8080:8080 --env-file .env vibelink-backend
```

## API Endpoints

- `/health` - Health check
- Auth, users, matching, chat, discover, content, payments, legal — all under their own route prefixes

## Status

Work in progress. Migrating features from the .NET backend.
