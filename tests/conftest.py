import subprocess
import time
import pytest
from fastapi import FastAPI


@pytest.fixture
def test_app():
    app = FastAPI()
    return app


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
def postgresql_service(monkeypatch):
    command = "docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:alpine"
    process_result = subprocess.run(command, shell=True)
    container_id = process_result.stdout.decode("utf-8").strip()
    # Wait for the container to be ready
    for i in range(30):
        if not is_postgres_ready("127.0.0.1", 5432):
            time.sleep(1)
    # Setup the environment variables
    postgresql_url = f"postgresql://postgres:postgres@127.0.0.1:5432/postgres"
    monkeypatch.setenv("FAILSAFE_DB_URL", postgresql_url)
    yield postgresql_url
    # Clean up after the test
    subprocess.run(f"docker stop {container_id}", shell=True)
