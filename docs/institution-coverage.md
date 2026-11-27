# CP2 institutional coverage

User-supplied roster: all 23 IITs, 31 NITs, 25 IIITs, 7 IISERs and IISc Bengaluru (87 targets). The original three-institute sample was an integration smoke test, not the production scope. The full list, aliases and state labels are in backend/app/ingestion/institution_roster.json. User names/state labels are targeting inputs, not verified source metadata.

## Collection

The first full-roster pass resolves each target against OpenAlex institution metadata using exact normalized campus-specific names or aliases and Indian educational institution type. Unique match only; never assign the top search result by default. Unresolved or ambiguous candidates remain for manual review; no invented identifiers. Then collect up to five recent publications per institution across disciplines (from 2023 onward, latest first), validating directly attributed Indian authorship. No keyword restriction during this foundation pass; product relevance is evaluated later. Up to 174 requests, at most one institution search and one filtered works page per target, sequential with pacing. Stop on API errors/limits; record remaining targets as not attempted. Exact per-campus coverage can be resumed using --start/--count. No paid account, full texts, grants, equipment or restricted procurement implied by this run.

OpenAlex documentation (reviewed 2026-11-28): https://help.openalex.org/api/authentication/ ; https://help.openalex.org/access/example-costs/ ; https://help.openalex.org/data/institutions/. Estimated request cost for this pass under documented rates: $0.0957, within an unused anonymous daily $0.10 budget, but actual availability and cost can differ. If insufficient, stop and use a free user-provided key or later quota; never create accounts or buy credits automatically.

## Run and review

    docker compose exec -T backend python -m app.ingestion.coverage --limit 5 > coverage.json

Existing CP1 volumes require migration 002 first. For batches, add --start 0 --count 20 (offset is zero-based). Optional key supplied via environment to docker compose exec, never committed. The report includes every requested target, its status, identifiers, publication count, and database-verified source observations. CI also exports report and records as a downloadable artifact; the CI database is disposable. Distinguish target count from verified institutional count, unique works from campus-specific observations, and no recent results from missing data.

The initial 87-target run must be checked before claiming coverage. Broader institution categories and deeper collection are not included by default. Lab/equipment/procurement/funding coverage still depends on permitted sources and is not inferred from OpenAlex coverage. No knowledge graph or new product features.
