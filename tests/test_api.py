import datetime
import json
import random
from typing import Tuple

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from inflection import dasherize
from polyfactory.factories.pydantic_factory import ModelFactory

from framework.controller import CollectionsAPIRouter
from src.api.process import ProcessRouter
from src.api.projects import ProjectsRouter
from src.api.reference import ReferenceRouter

ROUTERS = [ReferenceRouter, ProjectsRouter, ProcessRouter]


@pytest.fixture(params=ROUTERS)
def test_app_with_router(request, test_app: FastAPI):
    test_app.include_router(request.param)
    return test_app, request.param


def test_router_get_all(test_app_with_router: Tuple[CollectionsAPIRouter, FastAPI]):
    """
    Tests each router in turn to ensure that the API is working as expected.
    """
    test_app, router = test_app_with_router
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


def test_router_crud(test_app_with_router: Tuple[CollectionsAPIRouter, FastAPI], postgresql_service):
    test_app, router = test_app_with_router
    test_client = TestClient(test_app)

    for collection in router.collections:
        # prepare
        collection_name = dasherize(collection.__tablename__)
        collection_factory = ModelFactory.create_factory(model=collection.input_model())
        path = f"{router.prefix}/{collection_name}"

        # Test POST
        resource = collection_factory.build()
        json_payload = json.loads(resource.json())
        response = test_client.post(path, json=json_payload)
        post_content = response.json()
        assert response.status_code == 201
        for key, value in json_payload.items():
            assert post_content[key] == value
        assert post_content["id"] is not None
        id_ = post_content["id"]
        assert post_content["created_at"] is not None
        assert post_content["updated_at"] is not None

        # Test GET one
        response = test_client.get(f"{path}/{id_}")
        get_one_content = response.json()
        assert response.status_code == 200
        for key, value in json_payload.items():
            assert get_one_content[key] == value
        assert (
            datetime.datetime.fromisoformat(get_one_content["created_at"])
            < datetime.datetime.now()
        )
        assert (
            datetime.datetime.fromisoformat(get_one_content["updated_at"])
            < datetime.datetime.now()
        )
        assert "deleted_at" not in get_one_content.keys()

        # Test GET all
        response = test_client.get(path)
        get_all_content = response.json()
        assert response.status_code == 200
        assert isinstance(get_all_content, list)
        assert len(get_all_content) > 0
        assert get_one_content in get_all_content

        # Test PUT
        resource = collection_factory.build()
        put_json_payload = json.loads(resource.json())
        response = test_client.put(f"{path}/{id_}", json=put_json_payload)
        put_content = response.json()
        assert response.status_code == 200
        for key, value in put_json_payload.items():
            assert put_content[key] == value, f"{key} != {value}"

        # Test PATCH
        resource = collection_factory.build()
        random_key = random.choice(list(resource.dict().keys()))
        patch_json_payload = json.loads(resource.json())
        # remove random key for simulating partial update
        del patch_json_payload[random_key]
        response = test_client.patch(f"{path}/{id_}", json=patch_json_payload)
        patch_content = response.json()
        assert response.status_code == 200
        for key, value in patch_json_payload.items():
            assert patch_content[key] == value, f"{key} != {value}"

        # Test DELETE
        response = test_client.delete(f"{path}/{id_}")
        assert response.status_code == 204
        response = test_client.get(f"{path}/{id_}")
        assert response.status_code == 404
