import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.scoring import score_model, rank_models

CHEAP_MODEL = {
    "id": "cheap-1", "name": "Cheap Model", "provider": "Test",
    "categories": ["cheap_fast"], "cost_tier": "very_low",
    "speed_tier": "very_fast", "quality_tier": "budget", "context_window": 8000,
}

FRONTIER_MODEL = {
    "id": "frontier-1", "name": "Frontier Model", "provider": "Test",
    "categories": ["reasoning"], "cost_tier": "high",
    "speed_tier": "medium", "quality_tier": "frontier", "context_window": 500000,
}


def test_score_is_between_0_and_1():
    score = score_model(CHEAP_MODEL, "general")
    assert 0.0 <= score <= 1.0


def test_cheap_model_wins_cheap_fast_category():
    cheap_score = score_model(CHEAP_MODEL, "cheap_fast")
    frontier_score = score_model(FRONTIER_MODEL, "cheap_fast")
    assert cheap_score > frontier_score


def test_frontier_model_wins_reasoning_category():
    cheap_score = score_model(CHEAP_MODEL, "reasoning")
    frontier_score = score_model(FRONTIER_MODEL, "reasoning")
    assert frontier_score > cheap_score


def test_rank_models_sorts_descending():
    ranked = rank_models([CHEAP_MODEL, FRONTIER_MODEL], "reasoning")
    assert ranked[0]["score"] >= ranked[1]["score"]
