import os
import sys
import tempfile
from pathlib import Path

# Must run before `app` is imported: app.main creates tables and seeds data at
# import time, so point it at a throwaway SQLite DB and disable external APIs.
_tmpdir = tempfile.mkdtemp(prefix="tpb-tests-")
os.environ["DATABASE_URL"] = f"sqlite:///{_tmpdir}/test.db"
os.environ["OPENAI_API_KEY"] = ""
os.environ["BOOKING_API_KEY"] = ""
os.environ["STAY22_AID"] = "testaid"

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


@pytest.fixture(scope="session")
def client():
    from app.main import app

    with TestClient(app) as c:
        yield c
