# Database

PostgreSQL 16 + pgvector. Migration 001 creates the extension and version marker only. No scientific or private customer data yet. Compose applies SQL on first initialization. Future migrations must be versioned and tested against existing data; use a non-superuser app role and tenant policies before real data. Do not treat this local database user as a production role.

Verify: `docker compose exec db psql -U scientra -d scientra -c "SELECT extversion FROM pg_extension WHERE extname='vector';"`
