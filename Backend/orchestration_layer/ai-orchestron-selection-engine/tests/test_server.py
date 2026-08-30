import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import api_layer.api_router as api_router
from server import app, ROLES


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def disable_real_gemini_calls(monkeypatch):
    """
    Unit tests must be hermetic -- they should never depend on a real
    network call succeeding (or even being reachable). This forces every
    test in this file to use the mocked response path regardless of what
    config.py has ENABLE_REAL_GEMINI_CALLS set to.
    """
    monkeypatch.setattr(api_router, "ENABLE_REAL_GEMINI_CALLS", False)


# ---------- /api/models ----------

def test_get_models_returns_50(client):
    res = client.get("/api/models")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 50


# ---------- /api/select ----------

def test_select_auto_mode(client):
    res = client.post("/api/select", json={
        "prompt_id": "t1",
        "original_prompt": "Write a Python function",
        "matched_prompt": "Write a Python function",
        "category": "coding",
        "tags": [],
        "user_preferences": {"mode": "auto", "manual_model_id": None},
        "keys": {"Google": "fake-key"},
    })
    assert res.status_code == 200
    data = res.get_json()
    assert "selected_model" in data
    assert data["score"] > 0


def test_select_rejects_invalid_body(client):
    res = client.post("/api/select", json={"nonsense": True})
    assert res.status_code == 400


# ---------- /api/orchestrate ----------

def test_orchestrate_rejects_empty_prompt(client):
    res = client.post("/api/orchestrate", json={"prompt": "", "keys": {}})
    assert res.status_code == 400


def test_orchestrate_rejects_missing_body(client):
    res = client.post("/api/orchestrate", data="not json", content_type="text/plain")
    assert res.status_code == 400


def test_orchestrate_returns_all_5_roles_in_order(client):
    res = client.post("/api/orchestrate", json={
        "prompt": "Build a REST API for a todo app",
        "keys": {"Google": "fake-key", "DeepSeek": "fake-key"},
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["problem"] == "Build a REST API for a todo app"
    assert len(data["agents"]) == 5

    expected_roles = [r["name"] for r in ROLES]
    actual_roles = [a["role"] for a in data["agents"]]
    assert actual_roles == expected_roles


def test_orchestrate_each_agent_has_full_shape(client):
    res = client.post("/api/orchestrate", json={
        "prompt": "Summarize recent research",
        "keys": {"Google": "fake-key"},
    })
    data = res.get_json()
    required_fields = {
        "role", "subtitle", "rank", "category", "selected_model",
        "reasoning", "score", "score_breakdown", "fallback_used",
        "api_key_status", "response_text",
    }
    for agent in data["agents"]:
        assert required_fields.issubset(agent.keys())


def test_orchestrate_no_keys_at_all_reports_missing_key_for_every_role(client):
    """
    Mirrors the exact manual test scenario: zero keys entered anywhere.
    Every role should honestly report it has no usable key, rather than
    silently pretending to succeed.
    """
    res = client.post("/api/orchestrate", json={
        "prompt": "write a code for the while loop",
        "keys": {},
    })
    data = res.get_json()
    for agent in data["agents"]:
        assert agent["api_key_status"] == "fallback_missing_key"
        assert agent["fallback_used"] is False
        assert "ERROR" in agent["response_text"]


def test_orchestrate_gemini_only_key_triggers_fallback_for_non_google_picks(client):
    """
    With only a Gemini key present, any role whose best-fit model isn't
    Google should fall back to Gemini rather than erroring out.
    """
    res = client.post("/api/orchestrate", json={
        "prompt": "Build a REST API for a todo app",
        "keys": {"Google": "fake-key"},
    })
    data = res.get_json()
    for agent in data["agents"]:
        # With only a Gemini key, every role must resolve to either its
        # own model (if it happened to pick Google) or the Gemini fallback.
        assert agent["api_key_status"] in ("ok", "fallback_used")
        assert agent["selected_model"]["provider"] == "Google"


def test_orchestrate_roles_map_to_distinct_categories():
    categories = [r["category"] for r in ROLES]
    assert len(set(categories)) == 5  # every role should use a different scoring category
