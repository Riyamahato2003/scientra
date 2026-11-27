import hashlib
import json
from datetime import date, datetime
from typing import Literal
from urllib.parse import urlsplit

from psycopg import Connection
from psycopg.types.json import Jsonb
from pydantic import BaseModel, field_validator

Kind = Literal["institution", "publication", "laboratory", "equipment", "procurement"]
Method = Literal["manual_public_metadata", "openalex_api"]

SOURCE_HOSTS = {
    "openalex": {"openalex.org", "api.openalex.org"},
    "iitb_public": {"www.iitb.ac.in", "instruments.iitb.ac.in", "www.ese.iitb.ac.in"},
}


class SourceRecord(BaseModel):
    source_id: str
    kind: Kind
    external_id: str
    canonical_url: str
    locator: str
    payload: dict
    observed_on: date
    method: Method
    published_at: date | None = None
    retrieved_at: datetime | None = None

    @field_validator("external_id", "locator")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Blank identifier or locator")
        return value

    def validate_source(self) -> None:
        url = urlsplit(self.canonical_url)
        if (
            url.scheme != "https"
            or url.hostname not in SOURCE_HOSTS.get(self.source_id, set())
            or url.username
            or url.password
            or url.port
            or url.query
            or url.fragment
        ):
            raise ValueError("Unapproved canonical source URL")
        if self.method == "openalex_api":
            if self.source_id != "openalex" or self.retrieved_at is None:
                raise ValueError("API provenance required")
            if self.retrieved_at.utcoffset() is None:
                raise ValueError("Retrieval timestamp must be timezone-aware")
        elif self.retrieved_at is not None:
            raise ValueError("Manual observation has day precision only")
        if not self.payload:
            raise ValueError("Empty source record")

    def digest(self) -> str:
        content = {
            "canonical_url": self.canonical_url,
            "locator": self.locator,
            "payload": self.payload,
            "published_at": self.published_at.isoformat() if self.published_at else None,
        }
        encoded = json.dumps(content, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        return hashlib.sha256(encoded.encode()).hexdigest()


def store_records(conn: Connection, records: list[SourceRecord]) -> int:
    with conn.transaction(), conn.cursor() as cur:
        for record in records:
            record.validate_source()
            cur.execute(
                "SELECT rights_status FROM source_registry WHERE id = %s FOR SHARE",
                (record.source_id,),
            )
            result = cur.fetchone()
            if result is None or result[0] == "blocked":
                raise ValueError("Source not permitted")
            if result[0] == "review_only" and record.method != "manual_public_metadata":
                raise ValueError("Review-only source cannot be automated")
            cur.execute(
                """
                INSERT INTO source_snapshot (
                    source_id, kind, external_id, canonical_url, locator, payload,
                    content_hash, method, published_at, first_observed_on,
                    last_observed_on, retrieved_at
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (source_id, kind, external_id, content_hash, method)
                DO UPDATE SET
                    first_observed_on = LEAST(
                        source_snapshot.first_observed_on, EXCLUDED.first_observed_on
                    ),
                    last_observed_on = GREATEST(
                        source_snapshot.last_observed_on, EXCLUDED.last_observed_on
                    ),
                    last_ingested_at = now()
                """,
                (
                    record.source_id,
                    record.kind,
                    record.external_id,
                    record.canonical_url,
                    record.locator,
                    Jsonb(record.payload),
                    record.digest(),
                    record.method,
                    record.published_at,
                    record.observed_on,
                    record.observed_on,
                    record.retrieved_at,
                ),
            )
    return len(records)
