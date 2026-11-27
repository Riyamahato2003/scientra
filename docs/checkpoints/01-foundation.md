# Checkpoint 1 — review record

Status: submitted for review; execution evidence pending. No later checkpoint started.

| Acceptance item | Deliverable |
|---|---|
| Existing GitHub repository initialized | README and checkpoint branch |
| Product requirements and architecture | PRD, architecture, agent architecture, data design, original blueprint |
| Frontend scaffold | Next.js TypeScript / Tailwind status page |
| Backend scaffold | FastAPI, Pydantic config, live/readiness endpoints |
| Database scaffold | PostgreSQL 16 + pgvector, initial schema marker, Compose health check |
| Coding standards | AGENTS.md, CLAUDE.md, CONTRIBUTING.md, strict TS, Ruff |
| Testing | pytest unit/integration, Playwright smoke and CI configuration |

Required runtime proof: compose build and up; backend liveness/readiness 200; frontend renders real readiness; pgvector and schema marker verified by query; unit tests, lint, typecheck, build and Playwright pass. Record actual CI run in PR. Until then runtime gate is unverified. Dependencies use initial compatible ranges; lockfiles/digests pending resolution, no claim of reproducibility yet.

Decisions: local-only Compose, no cloud spend or API credentials, no live scientific data or agent implementations, no real customer data; auth/storage/worker and remaining blueprint technologies deferred to owning checkpoints. Preserve blueprint, not replace it. Owner review and approval required before merge/CP2.
