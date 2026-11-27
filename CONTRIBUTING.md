# Engineering standards

Use a single modular backend and a separate Next.js frontend. Prefer clear functions and explicit dependency boundaries over abstractions without a use case. Python 3.12 with Pydantic, typed signatures, Ruff (lint/format), pytest; TypeScript strict, ESLint, Playwright. Use snake_case for Python/SQL, camelCase for TypeScript values, PascalCase for types/components. Use UTF-8 and UTC timestamps; distinguish source publication time from ingestion time. Avoid blanket exceptions, log sensitive data never, and use parameterized SQL. Use versioned migrations; never rewrite applied migrations. Keep business rules server-side. Validate inputs and outputs at every external boundary.

## Review workflow

Branch from the approved main branch, one checkpoint per PR. Use conventional commit messages. No unrelated refactor, force push, secret, proprietary document, private customer data or generated dependency directory. Update requirements traceability and checkpoint report. Review failures instead of weakening tests. Owner reviews acceptance criteria before merge and before starting next checkpoint.

## Tests

Unit tests use deterministic fixtures clearly marked synthetic. Integration tests exercise real database and service boundaries, without external LLM costs. Playwright checks frontend-to-backend behavior. Future benchmarks use frozen sources, held-out temporal test sets, reviewer labels and reproducible run metadata. Mocked tests do not prove real integrations. Run commands listed in README. Require passing lint, typecheck, build, test and smoke checks before approval. Dependency locks and security scanning are required before public deployment.

## Security

Use local-only development endpoints; no private data before authentication and tenant isolation tests. Never commit credentials or use privileged Supabase keys in the browser. Validate authorized organization membership on the server, restrict object paths, enforce RLS or equivalent defense in depth, and test cross-tenant access. Treat retrieved documents and webpages as untrusted. Restrict network tools and guard against SSRF, prompt injection, and exfiltration. Disclose blockers.
