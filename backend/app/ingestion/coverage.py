"""Bounded, roster-wide CP2 ingestion; no purchase-intent inference."""

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from time import sleep

import psycopg
from pydantic import BaseModel

from app.config import Settings
from app.ingestion.openalex import (
    OpenAlexError,
    get_json,
    institution_record,
    publication_record,
)
from app.ingestion.records import SourceRecord, store_records


class Target(BaseModel):
    key: str
    category: str
    name: str
    state: str
    query: str
    aliases: list[str]


def load_roster() -> list[Target]:
    path = Path(__file__).with_name("institution_roster.json")
    return [Target.model_validate(row) for row in json.loads(path.read_text("utf-8"))]


def normalize(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.casefold().replace("&", "and"))


def match_institution(target: Target, candidates: list[dict]) -> dict | None:
    allowed = {normalize(name) for name in target.aliases}
    matches = {}
    for candidate in candidates:
        if candidate.get("country_code") != "IN" or candidate.get("type") != "education":
            continue
        names = [
            candidate.get("display_name"),
            *(candidate.get("display_name_alternatives") or []),
            *(candidate.get("display_name_acronyms") or []),
        ]
        if allowed.intersection(normalize(name) for name in names if isinstance(name, str)):
            ident = candidate.get("id")
            if isinstance(ident, str):
                matches[ident] = candidate
    return next(iter(matches.values())) if len(matches) == 1 else None


def search_institution(target: Target) -> tuple[dict | None, list[dict]]:
    response = get_json(
        "/institutions",
        {
            "search": target.query,
            "filter": "country_code:IN,type:education",
            "per_page": "25",
        },
    )
    candidates = response.get("results")
    if not isinstance(candidates, list):
        raise OpenAlexError("Invalid institution search response")
    return match_institution(target, candidates), candidates


def fetch_works(ident: str, limit: int) -> list[SourceRecord]:
    response = get_json(
        "/works",
        {
            "filter": f"institutions.id:{ident},from_publication_date:2023-01-01",
            "sort": "publication_date:desc",
            "per_page": str(limit),
            "select": "id,display_name,doi,publication_date,publication_year,authorships",
        },
    )
    works = response.get("results")
    if not isinstance(works, list) or len(works) > limit:
        raise OpenAlexError("Invalid works response")
    retrieved = datetime.now(UTC)
    return [publication_record(raw, retrieved, ident) for raw in works]


def stored(conn: psycopg.Connection, record: SourceRecord) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT EXISTS (
                SELECT 1 FROM reusable_source_records
                WHERE source_id=%s AND kind=%s AND external_id=%s
                AND content_hash=%s AND method=%s
            )
            """,
            (
                record.source_id,
                record.kind,
                record.external_id,
                record.digest(),
                record.method,
            ),
        )
        return cur.fetchone() == (True,)


def collect(
    conn: psycopg.Connection,
    targets: list[Target],
    limit: int,
) -> dict:
    report = []
    exported = []
    used_ids = set()
    halted = False
    for target in targets:
        entry = {
            "key": target.key,
            "category": target.category,
            "name": target.name,
            "state": target.state,
            "status": "not_attempted",
            "openalex_id": None,
            "ror": None,
            "publication_count": 0,
        }
        report.append(entry)
        if halted:
            continue
        try:
            matched, candidates = search_institution(target)
            if matched is None:
                entry["status"] = "unresolved"
                entry["candidates"] = [
                    {"id": c.get("id"), "name": c.get("display_name")} for c in candidates
                ]
                continue
            institution = institution_record(matched, datetime.now(UTC))
            ident = institution.external_id
            if ident in used_ids:
                entry["status"] = "duplicate_identity"
                entry["openalex_id"] = ident
                continue
            used_ids.add(ident)
            entry["openalex_id"] = ident
            entry["ror"] = institution.payload.get("ror")
            entry["canonical_name"] = institution.payload["name"]
            store_records(conn, [institution])
            if not stored(conn, institution):
                raise RuntimeError("Institution persistence check failed")
            exported.append(institution.model_dump(mode="json"))
            entry["status"] = "institution_only"
            sleep(0.25)
            publications = fetch_works(ident, limit)
            store_records(conn, publications)
            if not all(stored(conn, record) for record in publications):
                raise RuntimeError("Publication persistence check failed")
            exported.extend(record.model_dump(mode="json") for record in publications)
            entry["publication_count"] = len(publications)
            entry["status"] = "collected" if publications else "no_recent_works"
        except OpenAlexError as exc:
            entry["error"] = str(exc)
            if entry["status"] == "not_attempted":
                entry["status"] = "api_error"
            # Stop on provider/network errors, rather than retrying or exhausting quotas.
            halted = True
        except (ValueError, KeyError, TypeError) as exc:
            entry["error"] = type(exc).__name__
            entry["status"] = "invalid_source_record"
        finally:
            sleep(0.25)
    return {
        "observed_at": datetime.now(UTC).isoformat(),
        "target_count": len(targets),
        "publication_limit": limit,
        "source": "OpenAlex",
        "coverage": report,
        "records": exported,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=87)
    parser.add_argument("--limit", type=int, choices=range(1, 11), default=5)
    args = parser.parse_args()
    roster = load_roster()
    if not 0 <= args.start < len(roster) or not 1 <= args.count <= len(roster):
        parser.error("Invalid roster range")
    targets = roster[args.start : args.start + args.count]
    url = Settings().database_url
    if not url:
        parser.error("DATABASE_URL is required")
    with psycopg.connect(url, connect_timeout=5, autocommit=True) as conn:
        result = collect(conn, targets, args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
