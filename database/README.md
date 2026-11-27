# Database

PostgreSQL 16 + pgvector. Migration 001 creates the extension and version marker; 002 adds source registry and source snapshots, plus a rights-filtered view. No private customer data. Seed import is an explicit CLI step. Compose applies SQL on first initialization. Future migrations must be versioned and tested against existing data; use a non-superuser app role and tenant policies before real data. Do not treat this local database user as a production role.

Verify: `docker compose exec db psql -U scientra -d scientra -c "SELECT extversion FROM pg_extension WHERE extname='vector';"`

Existing CP1 volumes: apply migration 002 using `docker compose exec -T db psql -v ON_ERROR_STOP=1 -U scientra -d scientra < database/migrations/002_source_ingestion.sql`. Migration is idempotent. See CP2 runbook. Never reset existing volumes just to migrate.
