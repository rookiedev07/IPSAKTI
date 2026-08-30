"""
Manual mode (Task 2, option "select your own").
The user browses/filters the 50-model list themselves instead of letting
the engine auto-decide.
"""

from typing import List, Optional


def filter_models(
    models: List[dict],
    category: Optional[str] = None,
    max_cost_tier: Optional[List[str]] = None,
    provider: Optional[str] = None,
) -> List[dict]:
    """
    Simple filter over the model list. All filters are optional and additive.

    category: only keep models that list this tag in their "categories"
    max_cost_tier: list of acceptable cost tiers, e.g. ["very_low", "low"]
    provider: only keep models from this provider (case-insensitive)
    """
    results = models

    if category:
        results = [m for m in results if category in m.get("categories", [])]

    if max_cost_tier:
        results = [m for m in results if m["cost_tier"] in max_cost_tier]

    if provider:
        results = [m for m in results if m["provider"].lower() == provider.lower()]

    return results


def search_models(models: List[dict], query: str) -> List[dict]:
    """Basic substring search across name, provider, and best_for."""
    query_lower = query.lower()
    return [
        m for m in models
        if query_lower in m["name"].lower()
        or query_lower in m["provider"].lower()
        or query_lower in m["best_for"].lower()
    ]


def get_model_by_id(models: List[dict], model_id: str) -> Optional[dict]:
    for m in models:
        if m["id"] == model_id:
            return m
    return None
