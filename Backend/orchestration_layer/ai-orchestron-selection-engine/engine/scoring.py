"""
The scoring framework: turns a model's attributes + a prompt's category
into a single comparable number.

This is the heart of "Task 2" -- everything else in engine/ and api_layer/
just calls into this.
"""

from typing import Dict, List
from config import (
    QUALITY_TIER_SCORES,
    COST_TIER_SCORES,
    SPEED_TIER_SCORES,
    CRITERIA_WEIGHTS,
    DEFAULT_CATEGORY,
    CONTEXT_WINDOW_CAP,
)


def normalize_context(context_window: int) -> float:
    """
    Turn a raw token count into a 0-1 score, capped at CONTEXT_WINDOW_CAP.
    Uses a square-root curve instead of linear so a handful of models with
    huge (2M token) context windows don't automatically dominate every
    category just because of that one attribute.
    """
    ratio = min(context_window / CONTEXT_WINDOW_CAP, 1.0)
    return ratio ** 0.5


def get_weights_for_category(category: str) -> Dict[str, float]:
    """Look up the weight profile for a category, falling back to 'general'."""
    return CRITERIA_WEIGHTS.get(category, CRITERIA_WEIGHTS[DEFAULT_CATEGORY])


def score_model(model: dict, category: str) -> float:
    """
    Score a single model against a given prompt category.
    Returns a float between 0 and 1 (higher = better fit).
    """
    weights = get_weights_for_category(category)

    quality_score = QUALITY_TIER_SCORES.get(model["quality_tier"], 0.5)
    cost_score = COST_TIER_SCORES.get(model["cost_tier"], 0.5)
    speed_score = SPEED_TIER_SCORES.get(model["speed_tier"], 0.5)
    context_score = normalize_context(model.get("context_window", 0))

    # Small bonus if the model's own category tags match the detected category --
    # rewards purpose-built models (e.g. a "coding" model for a coding prompt).
    # Prompt categories like "creative_writing" or "cheap_fast" are compound
    # words, but model tags use the individual words ("creative", "writing",
    # "cheap", "fast") -- so match on any overlapping token, not just an
    # exact string match.
    model_tags = set(model.get("categories", []))
    category_tokens = set(category.split("_"))
    category_match_bonus = 0.05 if category_tokens & model_tags else 0.0

    total = (
        weights["quality"] * quality_score
        + weights["cost"] * cost_score
        + weights["speed"] * speed_score
        + weights["context"] * context_score
        + category_match_bonus
    )

    return round(min(total, 1.0), 4)


def score_components(model: dict, category: str) -> Dict[str, float]:
    """
    Returns the four raw 0-1 attribute scores (before weighting) for a model
    against a category. Used by the UI to render the mixer-bar breakdown --
    separate from score_model() so score_model()'s return type never changes.
    """
    return {
        "quality": round(QUALITY_TIER_SCORES.get(model["quality_tier"], 0.5), 4),
        "cost": round(COST_TIER_SCORES.get(model["cost_tier"], 0.5), 4),
        "speed": round(SPEED_TIER_SCORES.get(model["speed_tier"], 0.5), 4),
        "context": round(normalize_context(model.get("context_window", 0)), 4),
    }


def rank_models(models: List[dict], category: str) -> List[dict]:
    """
    Score every model against a category and return them sorted best-first.
    Each returned dict is the original model dict plus a 'score' key.
    """
    ranked = []
    for model in models:
        scored = dict(model)
        scored["score"] = score_model(model, category)
        ranked.append(scored)

    ranked.sort(key=lambda m: m["score"], reverse=True)
    return ranked
