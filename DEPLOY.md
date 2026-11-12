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

## Automatic deploys (GitHub Actions)

Every push to `main` runs CI (`.github/workflows/ci.yml`). If all checks pass,
the `deploy` job SSHes into the server, checks out that exact commit and runs
`docker compose up -d --build`, then verifies `https://travelplannerbro.com/health`.
Pull requests run CI only — they never deploy.

### One-time server setup

```bash
# On the server, as the deploy user (must be able to run docker):
git clone https://github.com/faizulki/travel-planner.git /opt/travel-planner
cd /opt/travel-planner && cp .env.example .env   # fill in secrets
sudo usermod -aG docker "$USER"                   # if not root; re-login after

# Create a dedicated key for GitHub Actions and authorize it:
ssh-keygen -t ed25519 -N "" -C "github-actions-deploy" -f ~/gh_deploy_key
cat ~/gh_deploy_key.pub >> ~/.ssh/authorized_keys
cat ~/gh_deploy_key          # copy into the SSH_PRIVATE_KEY secret, then:
rm ~/gh_deploy_key ~/gh_deploy_key.pub
```

### GitHub secrets

Repo → Settings → Secrets and variables → Actions → *New repository secret*:

| Secret            | Example                       |
|-------------------|-------------------------------|
| `SSH_HOST`        | `185.197.251.19`              |
| `SSH_USER`        | `deploy` (or `root`)          |
| `SSH_PRIVATE_KEY` | contents of `gh_deploy_key`   |
| `APP_DIR`         | `/opt/travel-planner`         |
| `SSH_PORT`        | optional, defaults to `22`    |

App secrets (`OPENAI_API_KEY`, etc.) stay in the server's `.env`; they are not
stored in GitHub. Optionally add required reviewers to the `production`
environment (Settings → Environments) to approve each deploy manually.

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
