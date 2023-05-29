import os
import subprocess
import time
import pytest
from fastapi import FastAPI


@pytest.fixture
def test_app():
    app = FastAPI()
    return app
