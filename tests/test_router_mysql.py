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


def is_mysql_ready(ip: str, port: int) -> bool:
    """Check if MySQL is ready"""
    import aiomysql

    async def check_db():
        try:
            conn = await aiomysql.connect(
                host=ip, port=port, user="mysql", password="mysql"
            )
            await conn.fetch("SELECT 1")
            await conn.close()
            return True
        except:
            return False

    return check_db


@pytest.fixture(scope="session")
def mysql_service():
    create_args = "podman run -d -q -p 3306:3306 -e MYSQL_ROOT_PASSWORD=secret -e MYSQL_PASSWORD=mysql docker.io/mysql:latest".split(
        " "
    )
    process_result = subprocess.run(args=create_args, text=True, capture_output=True)
    container_id = process_result.stdout.strip()
    # Wait for the container to be ready
    for i in range(30):
        if not is_mysql_ready("127.0.0.1", 3306):
            if i == 29:
                raise Exception("MySQL is not ready")
            time.sleep(1)
        continue
    # Setup the environment variables
    mysql_url = f"mysql://mysql:mysql@127.0.0.1:3306/mysql"
    yield mysql_url
    # Clean up after the test
    delete_args = f"podman rm -f {container_id}".split(" ")
    subprocess.run(delete_args, text=True)


@pytest.fixture
def with_mysql(test_app_with_router, mysql_service):
    return test_app_with_router


def test_router_get_all_with_mysql(with_mysql):
    test_router_get_all(with_mysql)


def test_router_crud_with_mysql(with_mysql):
    test_router_crud(with_mysql)


def test_router_create_with_mysql(with_mysql):
    test_router_create(with_mysql)
