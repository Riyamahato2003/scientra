# Data design and access policy

Only foundation schema is implemented at CP1: vector extension and schema version marker. Domain schemas below are planned; migrations belong to their checkpoints.

## Logical schema

| Entity | Fields / relationships |
|---|---|
| source_registry | id, name, access_method, rights_status, allowed_use, review_date, rate_limit |
| source_snapshot | source_id, canonical_url, retrieved_at, published_at (nullable), hash, object_key, version, extraction status |
| evidence | snapshot_id, locator, exact excerpt, observed_at, claim support state |
| institution / lab / researcher | stable UUID, canonical identifiers, aliases, country; dated affiliation and lab membership links |
| publication | DOI/OpenAlex ID, title, date, authorship and institution links |
| research_project / grant | funder, recipient, project, award status/date, amount/currency, equipment allocation if documented |
| equipment_installation | lab, equipment class, manufacturer/model, observed date, installation date nullable, evidence |
| procurement | authority, reference, item, route, publication date, deadline, amendments, status, eligibility, award details if verified |
| organization / membership / partner_grant | tenant, user, role, explicit permitted manufacturer/distributor scope |
| product / profile_version | tenant, product family, application taxonomy, source, documented specs, unknowns |
| research_run / job | tenant, profile version, as_of, state, budget, lease, retry, idempotency key |
| claim / verification | subject, predicate, object, evidence links, fact/inference, confidence category, conflict and verdict, version |
| opportunity / revision | tenant, product, account, qualification L1–L6, demand, fit, freshness, eligibility, gaps, next action, verification |
| feedback / outcome | tenant, opportunity, authorized actor, event, RFQ/order values if permitted, date, known-account marker |
| compliance_audit / discrepancy | tenant, original documents, requirement/response locators, quantities, units, result, clarification |
| audit_event | actor, organization, entity/version, action, timestamp, minimal non-sensitive metadata |

Use UUID PKs, foreign keys, explicit uniqueness on stable external IDs, indexed dates and tenant keys. Append versioned snapshots and preserve conflicting claims. Null means unknown, never zero. UTC times; preserve date precision. Publication date and retrieval date separate for leakage-free evaluation. Use migrations, constraints, parametrized SQL and scoped reads. Embedding dimensions and model version selected with benchmark; no arbitrary vector columns until then.

## Source policy

OpenAlex is first candidate for API and licensing review. ROR/Crossref evaluated. Institutional pages, public funding announcements, I-STEM, ANRF, SERB-PRISM, GeM and CPPP are candidates, not approved bulk feeds. Verify actual access, coverage, source terms, reuse and redistribution; maintain registry and rate limits. No bypass of authentication/CAPTCHA, no restricted grant databases. Keep private manufacturer files isolated and authorized; no employer records by default. Store minimal excerpts and official URLs in accordance with rights. No source access has been tested in CP1.
