from unittest.mock import patch, AsyncMock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from make_app import make_app


def test_make_app():
    app = make_app()
    assert isinstance(app, FastAPI)
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'payload': 'Hello world!'}


def test_make_app_mocked():
    """Tests just ASGI application layer, mocking actual implementation of service."""
    app = make_app()
    assert isinstance(app, FastAPI)
    client = TestClient(app)
    mock_cor_1 = AsyncMock(return_value='mock result')
    with patch('make_app.cor_1', mock_cor_1):
        response = client.get("/")
    mock_cor_1.assert_awaited_once_with()
    assert response.status_code == 200
    assert response.json() == {'payload': 'mock result'}
