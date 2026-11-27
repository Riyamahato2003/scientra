BEGIN;
CREATE TABLE IF NOT EXISTS source_registry (
    id text PRIMARY KEY,
    name text NOT NULL,
    homepage text NOT NULL,
    rights_status text NOT NULL CHECK (rights_status IN ('open_metadata', 'review_only', 'blocked')),
    access_method text NOT NULL,
    policy_url text NOT NULL,
    reviewed_on date NOT NULL,
    notes text NOT NULL
);
INSERT INTO source_registry VALUES
('openalex','OpenAlex','https://openalex.org','open_metadata','API or public metadata',
 'https://help.openalex.org/api/','2026-11-28','CC0 metadata only; no publisher full text'),
('ror','ROR','https://ror.org','open_metadata','API or data dump',
 'https://ror.org/about/terms/','2026-11-28','CC0; evaluated, not integrated'),
('iitb_public','IIT Bombay public pages','https://www.iitb.ac.in','review_only','manual factual review',
 'https://instruments.iitb.ac.in/dual-chamber-sputter-system','2026-11-28',
 'All rights reserved; minimal factual observations, no commercial redistribution approval'),
('istem','I-STEM','https://www.istem.gov.in','review_only','public page review only',
 'https://www.istem.gov.in/resources/privacy-policy','2026-11-28','Third-party ownership; bulk rights unverified'),
('anrf','ANRF','https://www.anrfonline.in','review_only','public program pages only',
 'https://www.anrfonline.in/ANRF/HomePage','2026-11-28','No authenticated or private proposal data'),
('serb_prism','ANRF / historical SERB PRISM','https://prism.serbonline.in','blocked','CAPTCHA-gated searches',
 'https://prism.serbonline.in/EquipmentSearch','2026-11-28','No automated access or bypass'),
('gem','GeM','https://gem.gov.in','blocked','no adapter',
 'https://static-sit.gem.gov.in/privacy-policy.html','2026-11-28','Award access and reuse not verified'),
('cppp','CPPP','https://eprocure.gov.in','blocked','CAPTCHA-gated search',
 'https://eprocure.gov.in/eprocure/app?page=FrontEndAdvancedSearch&service=page',
 '2026-11-28','No automated access or bypass')
ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS source_snapshot (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_id text NOT NULL REFERENCES source_registry(id),
    kind text NOT NULL CHECK (kind IN ('institution','publication','laboratory','equipment','procurement')),
    external_id text NOT NULL,
    canonical_url text NOT NULL CHECK (canonical_url LIKE 'https://%'),
    locator text NOT NULL,
    payload jsonb NOT NULL CHECK (jsonb_typeof(payload) = 'object'),
    content_hash text NOT NULL CHECK (length(content_hash) = 64),
    method text NOT NULL CHECK (method IN ('manual_public_metadata','openalex_api')),
    published_at date,
    first_observed_on date NOT NULL,
    last_observed_on date NOT NULL,
    retrieved_at timestamptz,
    ingested_at timestamptz NOT NULL DEFAULT now(),
    last_ingested_at timestamptz NOT NULL DEFAULT now(),
    CHECK (last_observed_on >= first_observed_on),
    CHECK ((method = 'openalex_api') = (retrieved_at IS NOT NULL)),
    UNIQUE (source_id, kind, external_id, content_hash, method)
);
CREATE INDEX IF NOT EXISTS source_snapshot_lookup
ON source_snapshot (source_id, kind, external_id, last_observed_on);
CREATE OR REPLACE VIEW reusable_source_records AS
SELECT s.* FROM source_snapshot s
JOIN source_registry r ON r.id = s.source_id
WHERE r.rights_status = 'open_metadata';

INSERT INTO schema_versions(version) VALUES (2) ON CONFLICT DO NOTHING;
COMMIT;
