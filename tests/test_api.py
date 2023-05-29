import pytest
from fastapi import FastAPI

from src import get_app


@pytest.mark.parametrize("init", [None, "get_app"])
def test_get_app(init, test_app):
    init = test_app if init == "get_app" else None
    app = get_app(app=init)
    assert app is not None
    assert isinstance(app, FastAPI)
    assert len(app.routes) > 0
