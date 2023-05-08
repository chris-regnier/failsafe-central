import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api import CollectionsAPIRouter
from src import App
from src.models import Detection, Impact, Likelihood, Severity


@pytest.fixture
def reference_client():
    app = app
    return TestClient(app)


def test_get_collections(reference_client):
    response = reference_client.get("/severities/")
    assert response.status_code == 200
    assert response.json() == []