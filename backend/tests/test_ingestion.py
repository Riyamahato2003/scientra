import os
from datetime import UTC, date, datetime

import psycopg
import pytest

from app.ingestion.__main__ import load_seed
from app.ingestion.openalex import institution_record, publication_record
from app.ingestion.records import store_records

# Synthetic API fixture only. Never imported as real source data.
STAMP = datetime(2026, 11, 28, tzinfo=UTC)
INSTITUTION = "I123"


def test_seed_provenance() -> None:
    records = load_seed()
    assert len(records) == 9
    assert len({(r.source_id, r.kind, r.external_id) for r in records}) == 9
    for record in records:
        record.validate_source()
        assert record.observed_on == date(2026, 11, 28)
        assert record.retrieved_at is None
        assert len(record.digest()) == 64


def test_blocked_source_rejected() -> None:
    record = load_seed()[0].model_copy(update={"source_id": "cppp"})
    with pytest.raises(ValueError, match="Unapproved"):
        record.validate_source()


def test_institution_validation() -> None:
    raw = {"id": "https://openalex.org/I123", "display_name": "Synthetic", "country_code": "IN"}
    assert institution_record(raw, STAMP).external_id == INSTITUTION
    with pytest.raises(ValueError, match="Indian institution"):
        institution_record({**raw, "country_code": "US"}, STAMP)


def test_publication_matching_and_no_invention() -> None:
    raw = {
        "id": "https://openalex.org/W123",
        "display_name": "Synthetic work",
        "publication_date": "2026-01-01",
        "authorships": [
            {
                "author": {"id": "https://openalex.org/A123", "display_name": "Synthetic author"},
                "institutions": [{"id": "https://openalex.org/I123", "country_code": "IN"}],
            }
        ],
    }
    record = publication_record(raw, STAMP, INSTITUTION)
    assert record.published_at == date(2026, 1, 1)
    assert record.payload["doi"] is None
    with pytest.raises(ValueError, match="matching Indian"):
        publication_record(raw, STAMP, "I456")


@pytest.mark.integration
@pytest.mark.skipif(not os.getenv("DATABASE_URL"), reason="requires PostgreSQL")
def test_real_seed_persistence_and_idempotence() -> None:
    records = load_seed()
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        assert store_records(conn, records) == 9
        assert store_records(conn, records) == 9
        with conn.cursor() as cur:
            for record in records:
                cur.execute(
                    """
                    SELECT count(*), min(first_observed_on), min(ingested_at)
                    FROM source_snapshot
                    WHERE source_id=%s AND kind=%s AND external_id=%s
                    AND content_hash=%s AND method=%s
                    """,
                    (
                        record.source_id,
                        record.kind,
                        record.external_id,
                        record.digest(),
                        record.method,
                    ),
                )
                row = cur.fetchone()
                assert row is not None
                assert row[0] == 1 and row[1] == record.observed_on and row[2] is not None
            cur.execute("SELECT count(*) FROM reusable_source_records WHERE source_id='iitb_public'")
            assert cur.fetchone() == (0,)
