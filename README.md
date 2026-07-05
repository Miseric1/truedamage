# LoL Analytics Platform

A full-stack League of Legends analytics platform (OP.GG-style), built incrementally as a
portfolio project. This repo is a **monorepo**: frontend and backend live side by side so a
single PR can span both when a feature touches the whole stack (e.g. "add summoner search"
touches a FastAPI route *and* a React page).

## Stage: Scaffolding only

This commit contains **no business logic and no Riot API calls**. The goal is to prove the
stack is wired together end to end:

- Postgres + Redis run locally via Docker Compose.
- FastAPI backend boots, reads config from environment variables, and exposes `/api/v1/health`.
- React frontend boots and successfully calls that health endpoint.
- CI lints both sides on every PR.

Nothing else should be assumed to exist yet — no DB models, no auth, no rate limiter, no Riot
API client. Those are separate, deliberate sessions.

## Running it locally

1. **Infra (Postgres + Redis):**
   ```bash
   cp .env.example .env       # only needed if you want to override defaults
   docker compose up -d
   ```

2. **Backend:**
   ```bash
   cd backend
   cp .env.example .env
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt -r requirements-dev.txt
   uvicorn app.main:app --reload
   ```
   Visit http://localhost:8000/api/v1/health

3. **Frontend:**
   ```bash
   cd frontend
   cp .env.example .env
   npm install
   npm run dev
   ```
   Visit http://localhost:5173 — it should say "Backend connection status: connected".

## Folder structure

```
lol-analytics-platform/
├── backend/            FastAPI service
├── frontend/            React + TypeScript (Vite) app
├── docker-compose.yml   Local infra: Postgres, Redis
└── .github/workflows/   CI (lint on every PR)
```

See inline comments in `docker-compose.yml`, `backend/app/core/config.py`, and
`frontend/src/api/client.ts` for the reasoning behind specific choices — treat this repo as
the running log of *why*, not just *what*.
