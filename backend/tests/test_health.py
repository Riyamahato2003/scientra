import os

import pytest
from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


def test_live() -> None:
    assert client.get("/health/live").json() == {"status": "ok"}


def test_ready_when_database_available(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(main, "database_ready", lambda: True)
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ready"}


def test_unavailable_when_database_down(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(main, "database_ready", lambda: False)
    response = client.get("/health/ready")
    assert response.status_code == 503
    assert response.json() == {"status": "unavailable", "database": "not_ready"}


def test_missing_database_configuration(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert not main.database_ready()


@pytest.mark.integration
@pytest.mark.skipif(not os.getenv("DATABASE_URL"), reason="requires PostgreSQL")
def test_real_database_readiness() -> None:
    assert main.database_ready()
    assert client.get("/health/ready").status_code == 200
