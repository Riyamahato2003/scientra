# Scientra

**Turning scientific intelligence into revenue.**

An India-first, evidence-backed commercial intelligence platform for global scientific instrument manufacturers and Indian distributors. Initial focus: thin-film deposition and materials science.

**Status:** Checkpoint 1 foundation only. No live data, agents, qualified opportunities, compliance verdicts or customer accounts are implemented yet.

## Start here

- [Master blueprint v1.0](docs/master-blueprint.md) — original scope and 11 sections.
- [Product requirements](docs/product-requirements.md)
- [Technical architecture](docs/architecture.md)
- [Agent design](docs/agent-architecture.md)
- [Data model and source policy](docs/data-design.md)
- [Checkpoint tracker](docs/checkpoints/README.md)
- [Checkpoint 1 review](docs/checkpoints/01-foundation.md)
- [Coding standards](CONTRIBUTING.md) and [agent instructions](AGENTS.md).

## Run locally

Requires Docker with Compose v2, Node.js 22, and Python 3.12 for host-side tests. No API key or cloud account required.

    docker compose up --build --wait

Open http://localhost:3000 for the foundation status page and http://localhost:8000/docs for the API. GET /health/live checks the API; GET /health/ready checks real PostgreSQL connectivity, schema marker and pgvector. Ports bind to loopback only. The default database password is for disposable local development only.

    docker compose logs
    docker compose down

Keep the volume by default. SQL initialization runs on a fresh volume only. For schema changes add versioned migrations; never delete existing data casually.

## Tests

With Compose running, from repository root:

    cd backend
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements-dev.txt
    ruff check .
    ruff format --check .
    DATABASE_URL=postgresql://scientra:scientra_dev_only@localhost:5432/scientra pytest
    cd ../frontend
    npm install
    npm run lint
    npm run typecheck
    npm run build
    npx playwright install chromium
    npm run test:e2e

The GitHub Actions foundation workflow is intended to exercise these checks against real services. Do not claim successful execution without a recorded passing run. Dependency ranges are initial compatibility constraints; resolved lockfiles and image digests remain a review item before customer deployment.

Do not expose this development stack publicly. Cloud hosting, Supabase Auth, protected tenant data, and production secrets are later checkpoints.

## Checkpoint 2 — scientific source ingestion

See [source feasibility](docs/source-feasibility.md) and [CP2 runbook](docs/checkpoints/02-data-infrastructure.md). Apply migration 002 to existing databases before importing. Run `docker compose exec backend python -m app.ingestion seed` to populate the local database with nine real source observations. `summary` reports counts by rights, kind, and method; `live --limit 5` attempts bounded OpenAlex API collection. Institutional review records are not approved commercial data. No customer functionality added.

Full institutional coverage: see [87-institution roster and collection runbook](docs/institution-coverage.md). The three-institution `live` command remains a smoke test only; the full `coverage` command is the initial population workflow.
