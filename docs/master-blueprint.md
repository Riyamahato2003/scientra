# Our Startup — Complete Architecture & Development Plan

**Master reference | Version 1.0 | 27 November 2026 | Status: Planned**

We are building an **AI-powered Scientific Revenue Intelligence Platform for India**, inspired by SciLeads but focused on discovering genuinely qualified business opportunities for international manufacturers and Indian distributors.

We will use **LangChain Deep Agents** as our primary agent framework, with controlled workflows and independent verification.

The entire project will revolve around three objectives:

- **Revenue creation:** Discover new, qualified customers.
- **Revenue protection:** Prevent avoidable tender disqualifications.
- **Competitive advantage:** Build scientific and commercial intelligence that becomes increasingly difficult to replicate.

## 1. Complete system architecture

The architecture below preserves the original diagram as a static workflow.

| Layer | Components and responsibilities |
|---|---|
| Foreign Manufacturers & Indian Distributors | Customers of the platform |
| Customer Dashboard | Next.js + TypeScript; Discover opportunities; Market intelligence; Competitor tracking; Compliance auditor |
| Backend — FastAPI | Authentication · APIs · Business logic · Research jobs |
| Deep Agents Intelligence Engine | LangChain + LangGraph runtime |
| Research Supervisor Agent | Plans and delegates investigations |
| Scientific Research Agent | What customers work on |
| Buying Signal Agent | Potential purchasing demand |
| Equipment Agent | Existing instruments |
| Procurement Agent | Tenders and eligibility |
| Commercial Qualification Agent | Converts research into potential sales opportunities |
| Independent Verification & Quality Gate | Evidence checking · Deterministic rules · Commercial qualification |
| Intelligence Database | PostgreSQL — Structured information; pgvector — Semantic search |
| Data Acquisition Layer | OpenAlex; I-STEM; ANRF / SERB; GeM / CPPP; Institutional websites; Manufacturer catalogues |

**Flow:** Customers → Dashboard ↔ Backend ↔ Deep Agents Intelligence Engine → Independent Verification & Quality Gate ↔ Intelligence Database ↔ Data Acquisition Layer. The research supervisor delegates to specialist agents; their findings feed the commercial qualification agent.

Deep Agents provides the research harness, including subagent delegation and context management. LangGraph provides its underlying runtime. We will retain explicit application-level control over verification and publication.

## 2. Final technology stack

| Component | Technology | Why? |
|---|---|---|
| Frontend | Next.js + TypeScript | Modern, scalable dashboard |
| UI | Tailwind CSS + shadcn/ui | Clean professional interface |
| Backend | Python + FastAPI | Excellent AI ecosystem |
| Agent framework | **LangChain Deep Agents** | Autonomous, adaptive research |
| Agent runtime | LangGraph | State and workflow execution |
| AI models | OpenAI, Gemini, Claude adapters | Avoid dependency on one provider |
| Data validation | Pydantic | Reliable structured outputs |
| Database | PostgreSQL | Central intelligence database |
| Vector database | pgvector | Semantic search without separate infrastructure |
| Knowledge graph | PostgreSQL relationships | Simpler and cheaper initially |
| Document processing | PyMuPDF, python-docx, openpyxl | Brochures, tenders and compliance sheets |
| Web data extraction | APIs, BeautifulSoup, selective Playwright | Public and permitted information retrieval |
| Background jobs | PostgreSQL-backed worker initially | Scheduled research and monitoring |
| File storage | S3-compatible storage | Documents and evidence |
| Authentication | Supabase Auth | User and organisation management |
| Agent observability | LangSmith | Debugging, tracing and evaluation |
| Testing | Pytest + Playwright | Backend and frontend testing |
| Version control | GitHub | Development and collaboration |
| Deployment | Vercel + Railway + Supabase | Low initial infrastructure overhead |

We will select specific LLMs after benchmarking their accuracy and cost. We do not need Redis, Neo4j, Kubernetes or complex microservices initially.

## 3. How our AI agents will work

| Agent | Responsibility |
|---|---|
| 01. Research Supervisor | Plans what needs to be investigated and delegates tasks to specialist agents. |
| 02. Scientific Research Agent | Understands researchers, publications, current projects and scientific applications. |
| 03. Buying Signal Agent | Investigates funding, new laboratories, expansion plans and potential purchasing demand. |
| 04. Equipment Intelligence Agent | Investigates existing equipment, manufacturers and competitor installations. |
| 05. Procurement Agent | Investigates tenders, historical purchases and published eligibility conditions. |
| 06. Commercial Qualification Agent | Determines whether the collected evidence supports a meaningful sales opportunity. |
| 07. Verification Agent | Independently checks evidence, contradictions and unsupported conclusions. |

Initially, we will combine some of these responsibilities into three specialist agents under the Deep Agents supervisor. We will separate them further only if doing so improves quality.

The agents will have restricted tools, research budgets, cached information and limited retries. They cannot independently publish unverified conclusions.

## 4. How the product works in real life

Suppose Korvus Technology signs up to discover Indian customers for its HEX PVD systems.

1. **Manufacturer uploads its product catalogue.** AI understands the instrument and its documented applications.
2. **System searches Indian scientific accounts.** Retrieves potentially relevant laboratories and researchers.
3. **Deep Agents investigate promising accounts.** Current research, funding, equipment and procurement activity.
4. **AI qualifies commercial relevance.** Separates general prospects from stronger purchasing signals.
5. **Independent verification checks the findings.** Unsupported claims are removed or explicitly marked unknown.
6. **Manufacturer receives actionable opportunities.** Who to approach, why, when and what to discuss.
7. **Distributor provides commercial feedback.** Our intelligence improves through actual sales outcomes.

### What the final result looks like

**ILLUSTRATIVE PRODUCT PREVIEW — Early opportunity**

**Scientific Opportunity Report**

Manufacturer: Korvus Technology

**Advanced Materials Research Laboratory**

Product match: HEX PVD system

| Dimension | Finding |
|---|---|
| Product relevance | High |
| Current research | Thin-film fabrication |
| Research funding | Verified grant |
| Equipment budget | Unknown |
| Purchase intention | Not confirmed |
| Commercial priority | Investigate |

**Why this customer matters**

Their current research aligns with the manufacturer's thin-film deposition applications, and they have documented research funding.

**Recommended sales action**

Contact the research group to establish its existing deposition capabilities and future equipment requirements.

*In the actual product, every factual finding will have clickable original evidence.*

## 5. Our opportunity qualification system

We must never confuse a relevant researcher with a qualified buyer.

| Level | Classification | Meaning |
|---|---|---|
| L1 | Relevant account | Research aligns with the product |
| L2 | Active prospect | Relevant ongoing research activity |
| L3 | Funded prospect | Relevant funding has been verified |
| L4 | High-intent opportunity | Specific equipment demand or expenditure evidence |
| L5 | Confirmed requirement | Active procurement or independently confirmed requirement |
| L6 | Sales-qualified opportunity | Product fit and purchasing requirements validated by the sales team |

Our AI will prioritise opportunities based on evidence. It will not fabricate purchase probabilities or guarantee that someone will buy.

**This qualification system will be the most important part of our entire product.**

## 6. Development checkpoints — start to finish

Each checkpoint will include actual implementation, testing, documentation and your approval before proceeding.

**Master development tracker: 0/12 reviewed.** All checkpoints are currently planned. Each checkbox represents a review of completed work, not a claim that the work has been completed.

### Checkpoint 01 — Project foundation

*Foundation*

- Create the GitHub repository.
- Define product requirements and architecture.
- Set up frontend, backend and database.
- Establish coding standards and testing infrastructure.

**Acceptance criteria:** All base services run successfully and communicate.

- [ ] Mark checkpoint reviewed

### Checkpoint 02 — Data feasibility and collection

*Foundation*

- Test OpenAlex API access.
- Investigate I-STEM, ANRF, SERB, GeM and CPPP permissions.
- Collect real data from selected Indian institutions.
- Build source tracking and data ingestion.

**Acceptance criteria:** Real, traceable scientific records are available in our database.

- [ ] Mark checkpoint reviewed

### Checkpoint 03 — Scientific knowledge graph

*Foundation*

- Connect researchers, institutions, laboratories and publications.
- Link funding, equipment and procurement records.
- Implement entity resolution and duplicate detection.
- Track timestamps and conflicting information.

**Acceptance criteria:** The system accurately connects scientific entities with supporting evidence.

- [ ] Mark checkpoint reviewed

### Checkpoint 04 — Manufacturer product intelligence

*Foundation*

- Implement catalogue upload and extraction.
- Understand instrument categories and applications.
- Build product-specific search profiles.
- Separate documented capabilities from unknown customisation options.

**Acceptance criteria:** Accurate product profiles without invented specifications.

- [ ] Mark checkpoint reviewed

### Checkpoint 05 — Deep Agents framework

*Core AI engine*

- Configure the Deep Agents supervisor.
- Implement specialist research tools and subagents.
- Add research budgets, checkpointing and tracing.
- Compare results against a simpler non-agentic baseline.

**Acceptance criteria:** Agents complete real investigations reliably and within configured budgets.

- [ ] Mark checkpoint reviewed

### Checkpoint 06 — Qualified opportunity engine

*Core AI engine*

- Implement product-to-research matching.
- Investigate funding, equipment and buying signals.
- Build commercial qualification rules.
- Add mandatory independent verification.

**Acceptance criteria:** At least 80% of top-20 results accepted as relevant by a domain reviewer; all material claims evidence-linked.

- [ ] Mark checkpoint reviewed

### Checkpoint 07 — Competitor and market intelligence

*Product development*

- Discover publicly documented competitor installations.
- Analyse historical purchases and awards.
- Identify potential uncovered accounts.
- Introduce continuous opportunity monitoring.

**Acceptance criteria:** Manufacturer-specific market maps backed by verifiable records.

- [ ] Mark checkpoint reviewed

### Checkpoint 08 — Customer dashboard

*Product development*

- Build manufacturer onboarding.
- Create opportunity feeds and advanced search.
- Build evidence viewers and market reports.
- Introduce distributor access and feedback.

**Acceptance criteria:** A manufacturer can independently complete the core workflow.

- [ ] Mark checkpoint reviewed

### Checkpoint 09 — Technical compliance auditor

*Product development*

- Upload customer specifications and manufacturer-issued compliance sheets.
- Compare numerical values, units, tolerances and technical terminology.
- Detect contradictory compliance declarations.
- Generate discrepancies requiring manufacturer clarification.

**Acceptance criteria:** Critical mismatches in the benchmark are flagged without inventing compliance commitments.

- [ ] Mark checkpoint reviewed

### Checkpoint 10 — Evaluation and security

*Commercial validation*

- Benchmark historical opportunities without future-information leakage.
- Measure agent accuracy and research costs.
- Test organisation isolation and document security.
- Compare against manual research and competitors where accessible.

**Acceptance criteria:** Quality, security and cost acceptance tests pass.

- [ ] Mark checkpoint reviewed

### Checkpoint 11 — Deployment and commercial pilot

*Commercial validation*

- Deploy the application.
- Onboard selected manufacturers.
- Deliver actual commercial opportunities.
- Test pricing and measure customer feedback.

**Acceptance criteria:** Target at least one paid manufacturer pilot.

- [ ] Mark checkpoint reviewed

### Checkpoint 12 — Commercial learning and expansion

*Commercial validation*

- Collect permissioned sales outcomes.
- Measure meetings, RFQs and incremental pipeline.
- Improve opportunity ranking.
- Expand into additional scientific instrument categories.

**Acceptance criteria:** Demonstrable recurring commercial value before expansion.

- [ ] Mark checkpoint reviewed

## 7. Technical compliance auditor

This will be a separate module, not part of the autonomous lead research workflow.

| Workflow stage | Responsibility |
|---|---|
| Inputs | Customer specification + Manufacturer compliance sheet |
| AI Semantic Comparison | Understands technical requirements and wording |
| Deterministic Numerical Validation | Values · Units · Ranges · Tolerances |
| Output | Supported / Unclear / Mismatch |

**Flow:** Customer specification + Manufacturer compliance sheet → AI Semantic Comparison → Deterministic Numerical Validation → Supported / Unclear / Mismatch.

We review what the manufacturer has committed to. We never generate commitments or assume customisation capabilities ourselves.

## 8. Proposed repository structure

```text
scientific-revenue-intelligence/
│
├── frontend/
├── backend/
│   ├── api/
│   ├── agents/
│   │   ├── supervisor/
│   │   ├── research/
│   │   ├── qualification/
│   │   ├── verification/
│   │   └── tools/
│   ├── ingestion/
│   ├── knowledge_graph/
│   ├── opportunities/
│   ├── compliance/
│   ├── models/
│   ├── workers/
│   └── services/
│
├── database/
├── evaluations/
├── tests/
├── infrastructure/
├── docs/
│   ├── architecture.md
│   ├── product-requirements.md
│   └── checkpoints/
└── README.md
```

One repository, a modular backend and a separate frontend. Simple enough for a small founding team to maintain.

## 9. Our competitive advantage over time

**Proprietary Commercial Intelligence** — intelligence flywheel:

Collect scientific data → Discover opportunities → Sales team feedback → Commercial outcomes → Improve intelligence → Collect scientific data.

*Our intelligence flywheel: verified commercial outcomes improve future opportunity qualification, subject to customer data permissions.*

This is how we become more defensible. Eventually, we want to understand which research activities, funding patterns and institutional developments actually translate into scientific equipment purchases.

Competitors can copy features. Replicating our accumulated, verified commercial intelligence would be considerably harder.

## 10. What we will not build initially

| Excluded feature | Reason |
|---|---|
| Generic CRM | Not our core business |
| Automated cold emailing | Quality matters more than volume |
| Compliance sheet generation | Manufacturer's responsibility |
| Scientific equipment marketplace | Operationally complex |
| Instrument operation AI | Outside our domain |
| Generic AI chatbot | Not sufficiently valuable |
| Unrestricted autonomous agents | Reliability and cost risks |

## 11. Our initial success criteria

| Metric | Initial target |
|---|---|
| Relevant accounts in top 20 results | At least 80% |
| Material claims with traceable evidence | 100% |
| Fabricated procurement or funding records | Zero in acceptance tests |
| Unsupported purchasing claims | Zero in acceptance tests |
| Previously unknown commercial opportunities | Measurable improvement |
| Manufacturer-generated meetings and RFQs | Tracked during pilots |
| First paying manufacturer | At least one during initial pilot |

These are targets, not achieved results.

## Final decisions

| Decision | Selection |
|---|---|
| Product | Scientific Revenue Intelligence Platform |
| Primary market | India |
| Paying customers | Global scientific instrument manufacturers |
| Core feature | Qualified commercial opportunity discovery |
| Secondary feature | Technical compliance auditing |
| AI framework | LangChain Deep Agents |
| Architecture | Hybrid agentic + deterministic |
| Initial segment | Thin-film deposition and materials science |
| Development approach | 12 reviewed checkpoints |

The remaining uncertainties are commercial data access, actual agent performance, competitive superiority and customer willingness to pay. We will validate these early rather than waiting until the entire product is built.

**Our next step is Checkpoint 1 — establishing the technical foundation, database architecture, product requirements and development repository.**

---

*Reference links for the architecture: [Deep Agents documentation](https://docs.langchain.com/oss/python/deepagents/overview) · [Deep Agents GitHub](https://github.com/langchain-ai/deepagents). The original interactive diagrams and checkpoint tracker have been converted to static, readable equivalents. The project scope and proposed acceptance criteria are preserved.*
