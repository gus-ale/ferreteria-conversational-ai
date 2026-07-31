import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

os.environ["APP_ENV"] = "test"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite://"
os.environ["AI_PROVIDER"] = "demo"
os.environ["REALTIME_ENABLED"] = "false"
os.environ["AUTO_CREATE_TABLES"] = "true"
os.environ["SEED_DEMO_DATA"] = "true"
os.environ["LOG_LEVEL"] = "WARNING"

from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
