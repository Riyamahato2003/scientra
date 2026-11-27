# Checkpoint 2 — data feasibility and collection

Status: expanded to all 87 owner-specified institutions; full coverage run pending. Original seed/database and three-institution live CI runs passed. CP1 accepted; CP3 not started.

Requirement R01: source feasibility and permitted traceable ingestion. See [source feasibility](../source-feasibility.md). Source tracking includes registry, source status, canonical URL, field locator, observation date, actual ingestion timestamp, publication date when known, retrieval timestamp for live API, and content hash. Duplicate identical observations are upserted; changed payloads create snapshots. No cross-source entity resolution (CP3).

| Task | Deliverable |
|---|---|
| Integrate OpenAlex | Bounded read-only API adapter; three-institution smoke test plus 87-target coverage workflow, first page only |
| Evaluate sources | OpenAlex/ROR CC0, I-STEM/ANRF review only, PRISM/GeM/CPPP blocked for automation |
| Collect scientific records | Nine actual manually reviewed metadata observations, of which six are CC0 and three restricted to internal factual review |
| Ingestion and tracking | Migration 002, source registry, snapshots, CLI, reuse-filtered view |
| Acceptance | CI real PostgreSQL seed import, idempotence and exclusion tests; separate live OpenAlex smoke test |

## Execute

From repository root, start existing local stack: `docker compose up --build --wait`. On any existing CP1 volume, apply `docker compose exec -T db psql -v ON_ERROR_STOP=1 -U scientra -d scientra < database/migrations/002_source_ingestion.sql`. New volumes initialize both migrations. Do not destroy a volume.

    docker compose exec backend python -m app.ingestion seed
    docker compose exec backend python -m app.ingestion summary
    docker compose exec backend python -m app.ingestion live --limit 5

Optional free OpenAlex key: export OPENALEX_API_KEY before running `docker compose exec -e OPENALEX_API_KEY backend python -m app.ingestion live --limit 5`. Never commit or print it. The live test performs at most six API requests, no retries or pagination; failures terminate without partial API imports. CI uses disposable PostgreSQL and uploads summary in logs; local volume persists data after seed. No cloud DB provisioned.

## Tests and blockers

Direct sandbox DNS lookup failed, but original foundation CI run 46051380907 and live pilot run 46051381123 passed. Full 87-target collection is separate and its coverage must be verified. No grant records collected from CAPTCHA-protected sites. No commercial permission for institutional content established. No graph, AI agents, ranking, dashboard or feature changes. The original blueprint remains intact. Decisions: original three-institution smoke test, all 87 owner-specified targets, bounded first-page ingestion, source-level rights gate, internal factual samples only. Owner review required before merge or CP3.

See [full coverage scope](../institution-coverage.md). No claim of exhaustive collection or grant/equipment/procurement data for all 87.
