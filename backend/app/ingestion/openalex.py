import json
import os
import re
from datetime import UTC, date, datetime
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener

from app.ingestion.records import SourceRecord

PILOT_INSTITUTIONS = ("I162827531", "I68891433", "I154851008")
BASE_URL = "https://api.openalex.org"


class OpenAlexError(RuntimeError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def get_json(path: str, params: dict[str, str] | None = None) -> dict:
    if path != "/works" and not re.fullmatch(r"/institutions/I[0-9]+", path):
        raise ValueError("Unsupported OpenAlex path")
    url = BASE_URL + path
    if params:
        url += "?" + urlencode(params)
    headers = {"Accept": "application/json", "User-Agent": "Scientra-CP2/0.1"}
    key = os.getenv("OPENALEX_API_KEY")
    if key:
        headers["Authorization"] = "Bearer " + key
    try:
        with build_opener(NoRedirect()).open(Request(url, headers=headers), timeout=15) as resp:
            body = resp.read(8_000_001)
            if len(body) > 8_000_000:
                raise OpenAlexError("Response exceeded byte limit")
        result = json.loads(body)
    except HTTPError as exc:
        raise OpenAlexError(f"OpenAlex HTTP {exc.code}; no retry attempted") from None
    except (URLError, TimeoutError, ValueError) as exc:
        raise OpenAlexError(f"OpenAlex unavailable: {type(exc).__name__}") from None
    if not isinstance(result, dict):
        raise OpenAlexError("Unexpected response shape")
    return result


def short_id(value: str, prefix: str) -> str:
    match = re.fullmatch(rf"https://openalex\.org/({prefix}[0-9]+)", value)
    if not match:
        raise ValueError("Invalid OpenAlex identifier")
    return match.group(1)


def institution_record(raw: dict, retrieved: datetime) -> SourceRecord:
    ident = short_id(raw["id"], "I")
    if raw.get("country_code") != "IN" or not raw.get("display_name"):
        raise ValueError("Expected Indian institution")
    return SourceRecord(
        source_id="openalex",
        kind="institution",
        external_id=ident,
        canonical_url=f"https://openalex.org/institutions/{ident}",
        locator="API: id, display_name, country_code, ror",
        payload={
            "name": raw["display_name"],
            "country_code": raw["country_code"],
            "ror": raw.get("ror"),
        },
        observed_on=retrieved.date(),
        retrieved_at=retrieved,
        method="openalex_api",
    )


def publication_record(raw: dict, retrieved: datetime, institution: str) -> SourceRecord:
    ident = short_id(raw["id"], "W")
    matching = []
    for entry in raw.get("authorships") or []:
        affiliations = [
            {"id": item.get("id"), "name": item.get("display_name")}
            for item in entry.get("institutions") or []
            if item.get("id") == f"https://openalex.org/{institution}"
            and item.get("country_code") == "IN"
        ]
        if affiliations:
            author = entry.get("author") or {}
            matching.append(
                {
                    "author_id": author.get("id"),
                    "author_name": author.get("display_name"),
                    "affiliations": affiliations,
                }
            )
    if not matching or not raw.get("display_name"):
        raise ValueError("Work lacks matching Indian authorship or title")
    publication_date = raw.get("publication_date")
    return SourceRecord(
        source_id="openalex",
        kind="publication",
        external_id=ident,
        canonical_url=f"https://openalex.org/works/{ident}",
        locator="API: id, display_name, doi, publication_date, publication_year, authorships",
        payload={
            "title": raw["display_name"],
            "doi": raw.get("doi"),
            "publication_year": raw.get("publication_year"),
            "matching_authorships": matching,
            "scope_institution_id": institution,
        },
        observed_on=retrieved.date(),
        retrieved_at=retrieved,
        published_at=date.fromisoformat(publication_date) if publication_date else None,
        method="openalex_api",
    )


def collect_pilot(limit: int = 5) -> list[SourceRecord]:
    if not 1 <= limit <= 10:
        raise ValueError("Limit must be between 1 and 10")
    records = []
    for ident in PILOT_INSTITUTIONS:
        raw = get_json(f"/institutions/{ident}")
        record = institution_record(raw, datetime.now(UTC))
        if record.external_id != ident:
            raise ValueError("Institution identifier changed")
        records.append(record)
        page = get_json(
            "/works",
            {
                "search": "sputtering",
                "filter": f"institutions.id:{ident},from_publication_date:2023-01-01",
                "per_page": str(limit),
                "select": "id,display_name,doi,publication_date,publication_year,authorships",
            },
        )
        retrieved = datetime.now(UTC)
        works = page.get("results")
        if not isinstance(works, list) or not works or len(works) > limit:
            raise OpenAlexError("Empty or invalid pilot page; no successful import claimed")
        records.extend(publication_record(work, retrieved, ident) for work in works)
    return records
