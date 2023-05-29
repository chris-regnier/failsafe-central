import os
import subprocess
import time
from typing import Tuple

import pytest

from .test_router import (
    test_app_with_router,
    test_router_create,
    test_router_crud,
    test_router_get_all,
)


def is_postgres_ready(ip: str, port: int) -> bool:
    """Check if Postgres is ready"""
    import asyncpg

    async def check_db():
        try:
            conn = await asyncpg.connect(
                host=ip, port=port, user="postgres", password="postgres"
            )
            await conn.fetch("SELECT 1")
            await conn.close()
            return True
        except:
            return False

    return check_db


@pytest.fixture(scope="session")
def postgresql_service():
    create_args = "podman run -d -q -p 5432:5432 -e POSTGRES_PASSWORD=postgres docker.io/postgres:latest".split(
        " "
    )
    process_result = subprocess.run(args=create_args, text=True, capture_output=True)
    container_id = process_result.stdout.strip()
    previous_environment = os.environ.get("FAILSAFE_DB_URL", None)
    # Wait for the container to be ready
    for i in range(30):
        if not is_postgres_ready("127.0.0.1", 5432):
            time.sleep(1)
    # Setup the environment variables
    postgresql_url = f"postgresql://postgres:postgres@127.0.0.1:5432/postgres"
    os.environ["FAILSAFE_DB_URL"] = postgresql_url
    yield postgresql_url
    # Clean up after the test
    delete_args = f"podman rm -f {container_id}".split(" ")
    subprocess.run(delete_args, text=True)
    if previous_environment is not None:
        os.environ["FAILSAFE_DB_URL"] = previous_environment
    else:
        del os.environ["FAILSAFE_DB_URL"]


@pytest.fixture
def with_postgres(test_app_with_router, postgresql_service):
    return test_app_with_router


def test_router_get_all_with_postgres(with_postgres):
    test_router_get_all(with_postgres)


def test_router_crud_with_postgres(with_postgres):
    test_router_crud(with_postgres)


def test_router_create_with_postgres(with_postgres):
    test_router_create(with_postgres)
