import psycopg
from fastapi import FastAPI, Response
from pydantic import BaseModel

from app.config import Settings

app = FastAPI(title="Scientra", version="0.1.0")


class Health(BaseModel):
    status: str
    database: str | None = None


def database_ready() -> bool:
    url = Settings().database_url
    if not url:
        return False
    try:
        with psycopg.connect(url, connect_timeout=3) as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector'), "
                "EXISTS (SELECT 1 FROM schema_versions WHERE version = 1)"
            )
            return cur.fetchone() == (True, True)
    except psycopg.Error:
        return False


@app.get("/health/live", response_model=Health, response_model_exclude_none=True)
def live() -> Health:
    return Health(status="ok")


@app.get("/health/ready", response_model=Health, responses={503: {"model": Health}})
def ready(response: Response) -> Health:
    if not database_ready():
        response.status_code = 503
        return Health(status="unavailable", database="not_ready")
    return Health(status="ok", database="ready")
