# Docker Deployment

All three services (frontend, admin panel, backend) plus an nginx gateway run
via a single `docker compose` command.

## Architecture

```
                       ┌─────────────────────────┐
  browser  ──:80──▶    │   gateway (nginx)        │
                       │                          │
                       │  /       → frontend:3000 │
                       │  /admin  → admin:3001    │
                       │  /api    → backend:8000  │
                       │  /docs   → backend:8000  │
                       └─────────────────────────┘
```

Only the gateway publishes a host port. The frontend and admin panel call the
API through the same origin (`/api/v1`), so no CORS or hard-coded host is needed
in the browser bundle.

## First-time setup

```bash
cp .env.example .env       # then edit .env and set OPENAI_API_KEY
```

`.env` is gitignored. The compose file reads it automatically.

## Deploy

```bash
docker compose up -d --build
```

- Frontend:    http://localhost/
- Admin panel: http://localhost/admin
- API docs:    http://localhost/docs

To use a different host port: `GATEWAY_PORT=8080 docker compose up -d --build`.

## Common commands

```bash
docker compose logs -f            # tail all logs
docker compose logs -f backend    # one service
docker compose ps                 # status
docker compose down               # stop (keeps the db volume)
docker compose down -v            # stop and delete the sqlite volume
docker compose up -d --build frontend   # rebuild one service
```

## Notes

- **Database**: the backend's SQLite file lives in the named volume
  `backend-data` (`/app/data`). It is seeded from `backend/data/` on first run
  and persists across restarts. Use `down -v` to reset it.
- **NEXT_PUBLIC_API_URL** is baked into the Next.js bundles at build time
  (build arg, default `/api/v1`). If you change it, rebuild the frontend/admin
  images.
- **Secrets** (`.env`, `backend/.env`) are excluded from the images via
  `.dockerignore` and passed in as environment variables at runtime.
