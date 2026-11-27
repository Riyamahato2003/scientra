import argparse
import json
from pathlib import Path

import psycopg

from app.config import Settings
from app.ingestion.openalex import OpenAlexError, collect_pilot
from app.ingestion.records import SourceRecord, store_records


def load_seed() -> list[SourceRecord]:
    path = Path(__file__).with_name("seed_records.json")
    return [SourceRecord.model_validate(item) for item in json.loads(path.read_text("utf-8"))]


def main() -> None:
    parser = argparse.ArgumentParser(description="Scientra CP2 bounded source ingestion")
    parser.add_argument("command", choices=["seed", "live", "summary"])
    parser.add_argument("--limit", type=int, default=5, choices=range(1, 11))
    args = parser.parse_args()
    url = Settings().database_url
    if not url:
        parser.error("DATABASE_URL is required")
    try:
        with psycopg.connect(url, connect_timeout=5) as conn:
            if args.command != "summary":
                records = load_seed() if args.command == "seed" else collect_pilot(args.limit)
                print(f"Processed {store_records(conn, records)} real source observations")
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT r.rights_status, s.kind, s.method, count(*)
                    FROM source_snapshot s JOIN source_registry r ON r.id = s.source_id
                    GROUP BY 1,2,3 ORDER BY 1,2,3
                    """
                )
                for rights, kind, method, count in cur.fetchall():
                    print(f"{rights} | {kind} | {method} | {count}")
    except (OpenAlexError, ValueError) as exc:
        parser.exit(1, f"Ingestion stopped: {exc}\n")
    except psycopg.Error:
        parser.exit(1, "Database error; check schema migration and connection configuration\n")


if __name__ == "__main__":
    main()
