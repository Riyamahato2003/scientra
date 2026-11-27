# Scientra product requirements (PRD)

Status: checkpoint 1 design; all commercial functionality planned. Governing reference: master-blueprint.md.

## Purpose and users

Generate incremental scientific equipment sales in India and protect existing tender revenue. Paying customer: specialized foreign OEM (international sales director or founder); secondary: authorized Indian distributor and technical sales engineer. Start with PVD, sputtering, evaporation and related materials science; expand only after validation. Do not promise revenue or purchase intent. A lead list is not the product.

## Functional requirements and traceability

| ID | Requirement / observable outcome | Checkpoint |
|---|---|---|
| R01 | Ingest permitted Indian publications, institutions, funding, equipment, procurement and public announcements with provenance | 2 |
| R02 | Resolve institutions, labs, people, affiliations, publications, grants and equipment to stable entities; retain historical conflicts | 3 |
| R03 | Product profile from public/authorized catalogue; applications and documented capabilities; unknown customization stays unknown | 4 |
| R04 | Deep Agents adaptive investigations, three initial specialists plus supervisor; budget, checkpoint, tracing and baseline | 5 |
| R05 | Match products to active research; discover relevant accounts and distinguish current research from buying signals | 6 |
| R06 | Classify L1–L6, evidence and unknowns; separate fit, timing, eligibility and demand; mandatory verification and quality gate | 6 |
| R07 | Equipment and competitor installations, verified procurement awards, market coverage gaps using authorized CRM data | 7 |
| R08 | Monitor changing accounts and surface fresh signals; no duplicate alerts, mark stale and closed procurement | 7 |
| R09 | Manufacturer onboarding, search, filters, opportunity feed, evidence viewer, weekly reports and exports | 8 |
| R10 | Distributor workspaces, assignment, least-privilege sharing, known/rejected/contacted feedback | 8 |
| R11 | Review customer specifications vs manufacturer-issued compliance; numerical/unit/range/terminology checks, contradictory declarations, source locations and clarification | 9 |
| R12 | Temporal benchmark, accuracy, cost, security and organization isolation tests; competitor comparison if accessible | 10 |
| R13 | Deployment and paid pilot; measure previously unknown opportunities, meetings, RFQs, quotations, attributable pipeline and orders | 11 |
| R14 | Permissioned sales outcomes and commercial learning, improve ranking, expand only if recurring value proven | 12 |

## Qualification contract (no invented probabilities)

| Level | Meaning | Minimum required evidence |
|---|---|---|
| L1 Relevant account | Research aligns with product | Verified account and evidence of application fit |
| L2 Active prospect | Relevant ongoing research | L1 + dated relevant current activity |
| L3 Funded prospect | Relevant funding verified | L2 + actual awarded funding linked to account/project; equipment budget may be unknown |
| L4 High-intent opportunity | Specific equipment demand or expenditure evidence | Direct equipment requirement/planned acquisition or sanctioned equipment funding; fit established |
| L5 Confirmed requirement | Active procurement or independently confirmed requirement | Primary dated open notice or documented confirmation, status and eligibility separately recorded |
| L6 Sales-qualified opportunity | Product fit and purchasing requirements validated by sales | Authorized sales reviewer confirms fit, need and pursuit status, with review event; AI cannot assign L6 |

Levels are evidence stages, not purchase probabilities; L4/L5 do not require a publicly documented grant if specific demand is documented. Closed tenders are historical, not active L5. Unknown/restricted eligibility triggers a separate warning or blocks bid-ready recommendation. Stale evidence may downgrade a level with audit history. A relevant grant without equipment allocation is not L4.

## Opportunity output

Stable account/product identifiers, organization and research group, current research summary and date, fit rationale, evidence IDs/URLs/locators, funding and equipment status, procurement status/deadline/eligibility, qualification level and justification, missing information and recommended next action, freshness, known-to-sales status and verification result. Show facts separately from inference. No evidence means unknown, not negative.

## Acceptance targets

At least 80% of top-20 accounts rated relevant by independent domain reviewers; 100% material claims linked to evidence; zero fabricated funding/procurement or unsupported purchasing claims in acceptance tests. Track precision by level, false positives, new-to-CRM opportunities, cost per accepted opportunity, research latency, coverage and freshness. Compare a single-agent baseline, Deep Agents and controlled LangGraph with equal model/source budgets. Measure meetings, RFQs and attributable pipeline during pilot; at least one paid manufacturer pilot is a target, not achieved. Do not conflate research relevance and confirmed demand.

## Exclusions

No instrument operation, experimental analysis, generic CRM, marketplace, auto cold-email, compliance generation, unrestricted autonomous agents, technical customization guesses, or procurement-control bypass. Public data access and commercial reuse must be confirmed. No private company documents without authorization.
