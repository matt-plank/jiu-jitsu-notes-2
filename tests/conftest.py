from fastapi.testclient import TestClient
from pytest import fixture


@fixture
def client():
    from jiu_jitsu_notes.app import app

    return TestClient(app)
