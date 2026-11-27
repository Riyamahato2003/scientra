# Agent architecture (Checkpoint 5 design; not implemented in CP1)

Deep Agents (LangChain agent harness over LangGraph) handles adaptive research. Use the simplest workflow that meets the benchmark. Agent roles are logical responsibilities, not necessarily seven separate LLM processes.

| Role | Responsibility | Initial runtime grouping |
|---|---|---|
| Research Supervisor | Plan, delegate, prioritize missing evidence; bounded task list | Deep Agent supervisor |
| Scientific Research Agent | Research papers, active projects, affiliation, relevance | Research specialist |
| Buying Signal Agent | Grants, appointments, facilities, explicit demand | Commercial investigation specialist |
| Equipment Intelligence Agent | Documented instruments, manufacturer/model, dates | Research specialist |
| Procurement Agent | Tender status, amendments, deadlines, eligibility and awards | Commercial investigation specialist |
| Commercial Qualification Agent | Propose fit/demand/timing and classification using evidence | Qualification specialist |
| Verification Agent | Independently re-read original evidence, challenge contradictions and reject unsupported claims | Mandatory separate verifier outside supervisor delegation |

Three initial specialists plus supervisor and mandatory verification pass; no role is silently removed. Combining roles is a proposed implementation decision; benchmark separation before adding more workers.

## Execution

Deterministic candidate retrieval and deduplication precede agent research. Supervisor delegates bounded investigations to isolated subagents. Tools return structured evidence IDs and excerpts, not unconstrained browser control. Consolidate claims and gaps; qualification proposes a level. Independent verifier receives original evidence and proposed claims, not hidden rationale. Application quality gate checks evidence support verdicts, IDs, freshness, contradictions, deadline, required fields and L6 human approval. It publishes only allowed results; failed verification may trigger bounded targeted retry, then mark partial/unverified. No agent has permission to publish, contact customers, alter sources or access other tenants.

State: run_id, org_id, product_profile_version, as_of, candidate_ids, evidence_ids, claim proposals, conflicts, unknowns, verification verdicts, stage, model/version, prompt version, tool/cost/token counts, retries and timestamps. Store sensitive artifacts in tenant-scoped workspace; redacted tracing. Persist checkpoints and idempotent tool records.

## Budgets and tests

Set per-run monetary, token, tool-call, wall-time, concurrency, candidate-count and retry ceilings; shared budget enforced outside agent prompts across subagents, including retries. Stop before further calls if exhausted; mark partial. Use cheaper extraction models and stronger reasoning only if evaluated. Cache permissible source snapshots, keyed by source/version, not private customer output across tenants. Compare same 30 labeled accounts, identical models/sources/time cutoffs/budgets against single agent and controlled LangGraph/Pydantic AI baseline. Measure relevance, evidence support, demand precision, false positives, cost per accepted opportunity, latency and failure recovery. Exact model/framework versions chosen and locked in CP5; no real agent functionality claimed now.

Official reference: https://docs.langchain.com/oss/python/deepagents/overview
