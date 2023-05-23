import json
from typing import Tuple

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from inflection import dasherize
from polyfactory.factories.pydantic_factory import ModelFactory

from src import App
from src.api import CollectionsAPIRouter
from src.api.process import ProcessRouter
from src.api.projects import ProjectsRouter
from src.api.reference import ReferenceRouter

ROUTERS = [ReferenceRouter, ProjectsRouter, ProcessRouter]


@pytest.fixture
def test_app():
    app = FastAPI()
    return app


@pytest.fixture(params=ROUTERS)
def test_app_with_router(request, test_app: FastAPI):
    test_app.include_router(request.param)
    return test_app, request.param


def test_router_get_all(test_app_with_router: Tuple[CollectionsAPIRouter, FastAPI]):
    """
    Tests each router in turn to ensure that the API is working as expected.
    """
    test_app, router = test_app_with_router
    test_app.include_router(router)
    test_client = TestClient(test_app)

    # Test GET all
    for collection in router.collections:
        collection_name = dasherize(collection.__tablename__)
        path = f"{router.prefix}/{collection_name}/"
        response = test_client.get(path)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


def test_router_create(test_app_with_router: Tuple[CollectionsAPIRouter, FastAPI]):
    test_app, router = test_app_with_router
    test_app.include_router(router)
    test_client = TestClient(test_app)

    for collection in router.collections:
        collection_name = dasherize(collection.__tablename__)
        collection_factory = ModelFactory.create_factory(model=collection.input_model())
        resource = collection_factory.build()
        path = f"{router.prefix}/{collection_name}"
        json_payload = json.loads(resource.json())
        response = test_client.post(path, json=json_payload)
        response_content = response.json()
        assert response.status_code == 201
        for key, value in json_payload.items():
            assert response_content[key] == value
        assert response_content["id"] is not None
        id_ = response_content["id"]
        assert response_content["created_at"] is not None
        assert response_content["updated_at"] is not None
        delete_response = test_client.delete(f"{path}/{id_}")
        assert delete_response.status_code == 204
