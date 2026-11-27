# CP2 source feasibility — 28 November 2026

Scope: thin-film deposition, IIT Bombay, IIT Delhi and IIT Roorkee. Not a lead database, buying-intent assessment, or nationwide coverage claim.

| Source | Observed access | Reuse and decision |
|---|---|---|
| OpenAlex | Public institution and work metadata pages reviewed. API docs support keyless first page; free key increases budget. Direct API attempt from development environment could not resolve host; live CI probe pending. | CC0 metadata; integrate bounded API only, no article full text. |
| ROR | Official open API and data dump documented. | CC0; supporting source evaluated, adapter deferred. |
| I-STEM | Public equipment record and policy pages accessible. | Terms allow accurate, attributed reproduction in relevant contexts but exclude third-party rights; privacy policy says ownership remains with providers. No commercial bulk permission established. Review only, no adapter. |
| ANRF | Public schemes and proposal portal accessible. | No private proposals or authenticated data. Grant database permissions not established. |
| Historical SERB-PRISM | Historical portal now branded ANRF-PRISM. FundingDetails, Search, and EquipmentSearch pages show CAPTCHA. | No automated adapter; obtain explicit permitted data access before reconsidering. |
| GeM | Public all-bids request timed out in research tool; user reports award and PO restrictions. | No confirmed bulk access or award rights; no adapter. |
| CPPP | Official advanced search explicitly requires CAPTCHA. | No automated search or restricted award/PO access. |
| IIT Bombay pages | Facility, department lab and historical tender pages manually reviewed. | All-rights-reserved footers; minimal factual internal review samples only; not cleared for commercial redistribution. No scraping. |

## Official references

- OpenAlex: https://help.openalex.org/api/ ; https://help.openalex.org/api/authentication/ ; https://help.openalex.org/api/filtering/
- ROR: https://ror.org/about/terms/
- I-STEM: https://www.istem.gov.in/terms_of_use ; https://www.istem.gov.in/resources/privacy-policy ; https://www.istem.gov.in/equipment-info/47288/Dual-Chamber-Sputter-system
- ANRF: https://www.anrfonline.in/ANRF/HomePage
- Historical SERB release (11 March 2021): https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=1704029&lang=2&reg=48
- PRISM: https://prism.serbonline.in/ ; https://prism.serbonline.in/FundingDetails ; https://prism.serbonline.in/Search ; https://prism.serbonline.in/EquipmentSearch
- GeM: https://bidplus.gem.gov.in/all-bids ; https://static-sit.gem.gov.in/privacy-policy.html
- CPPP: https://eprocure.gov.in/eprocure/app?page=FrontEndAdvancedSearch&service=page

## Pilot records

See backend/app/ingestion/seed_records.json. Nine real observations manually transcribed from public source pages, not fabricated API responses: three OpenAlex institutions, three OpenAlex publications, one equipment record, one laboratory record, one procurement notice. All have canonical URLs, field locators and observation dates. Institutional records are internal review only and excluded from reusable_source_records. No copied PDFs, full text, private contact details, grant budget, award winner or PO price. Publication year is not converted to an invented publication date. Procurement due date is historical, not a purchase outcome. No data proves demand. Exact web page fetch times are unavailable; only observation day is recorded. API observations use actual UTC retrieval timestamps.

Access and terms can change; recheck before scaling. Source review is engineering due diligence, not legal clearance. No external scraping or account creation authorized.
