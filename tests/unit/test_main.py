"""L1 unit tests for the FastAPI application layer."""
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    with patch("app.agent.run", new_callable=AsyncMock, return_value="mocked answer") as _mock:
        from app.main import app
        yield TestClient(app), _mock


def test_health(client):
    c, _ = client
    r = c.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_ready(client):
    c, _ = client
    r = c.get("/ready")
    assert r.status_code == 200
    assert r.json()["status"] == "ready"


def test_list_models(client):
    c, _ = client
    r = c.get("/v1/models")
    assert r.status_code == 200
    ids = [m["id"] for m in r.json()["data"]]
    assert "research-agent" in ids


def test_chat_completions_non_stream(client):
    c, mock_run = client
    body = {
        "model": "research-agent",
        "messages": [{"role": "user", "content": "What is Solvency II?"}],
    }
    r = c.post("/v1/chat/completions", json=body)
    assert r.status_code == 200
    data = r.json()
    assert data["choices"][0]["message"]["role"] == "assistant"
    assert data["choices"][0]["message"]["content"] == "mocked answer"
    assert data["choices"][0]["finish_reason"] == "stop"
    mock_run.assert_awaited_once()


def test_chat_completions_stream(client):
    c, _ = client
    body = {
        "model": "research-agent",
        "messages": [{"role": "user", "content": "hello"}],
        "stream": True,
    }
    r = c.post("/v1/chat/completions", json=body)
    assert r.status_code == 200
    chunks = [line for line in r.text.splitlines() if line.startswith("data:")]
    assert any("[DONE]" in ch for ch in chunks)


def test_chat_unknown_model_uses_default(client):
    c, mock_run = client
    body = {
        "model": "nonexistent-model",
        "messages": [{"role": "user", "content": "hi"}],
    }
    r = c.post("/v1/chat/completions", json=body)
    assert r.status_code == 200
    mock_run.assert_awaited_once()


def test_empty_messages(client):
    c, _ = client
    body = {"model": "research-agent", "messages": []}
    r = c.post("/v1/chat/completions", json=body)
    assert r.status_code == 200
