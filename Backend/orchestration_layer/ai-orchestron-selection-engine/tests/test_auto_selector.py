import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.auto_selector import auto_select
from engine.manual_selector import filter_models, search_models, get_model_by_id
from api_layer.key_manager import KeyManager
from api_layer.fallback import resolve_execution_model
from config import MODELS_LIST_PATH, FALLBACK_MODEL_ID


def load_models():
    with open(MODELS_LIST_PATH, "r") as f:
        return json.load(f)


def test_auto_select_returns_top_pick_and_alternatives():
    models = load_models()
    result = auto_select("coding", models, top_n=3)
    assert "selected" in result
    assert "coding" in result["selected"]["categories"] or result["selected"]["score"] > 0
    assert len(result["alternatives"]) <= 2


def test_filter_models_by_category():
    models = load_models()
    coding_models = filter_models(models, category="coding")
    assert len(coding_models) > 0
    for m in coding_models:
        assert "coding" in m["categories"]


def test_search_models_finds_by_name():
    models = load_models()
    results = search_models(models, "gemini")
    assert any("Gemini" in m["name"] for m in results)


def test_get_model_by_id():
    models = load_models()
    model = get_model_by_id(models, FALLBACK_MODEL_ID)
    assert model is not None
    assert model["id"] == FALLBACK_MODEL_ID


def test_fallback_triggers_when_no_key_for_selected_model():
    models = load_models()
    selected = get_model_by_id(models, "gpt-5")  # OpenAI

    key_manager = KeyManager()
    key_manager.add_key("Google", "mock-gemini-key")  # only Gemini key present

    execution_model, fallback_used, status = resolve_execution_model(
        selected, key_manager, models
    )
    assert fallback_used is True
    assert status == "fallback_used"
    assert execution_model["provider"] == "Google"


def test_no_fallback_needed_when_key_present():
    models = load_models()
    selected = get_model_by_id(models, "gpt-5")

    key_manager = KeyManager()
    key_manager.add_key("OpenAI", "mock-openai-key")

    execution_model, fallback_used, status = resolve_execution_model(
        selected, key_manager, models
    )
    assert fallback_used is False
    assert status == "ok"
    assert execution_model["id"] == "gpt-5"


def test_hard_failure_when_no_keys_at_all():
    models = load_models()
    selected = get_model_by_id(models, "gpt-5")

    key_manager = KeyManager()  # no keys at all

    execution_model, fallback_used, status = resolve_execution_model(
        selected, key_manager, models
    )
    assert status == "fallback_missing_key"
