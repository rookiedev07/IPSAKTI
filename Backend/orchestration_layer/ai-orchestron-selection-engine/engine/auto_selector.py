"""
Auto-decide mode (Task 2, option "let the AI decide").
Takes the prompt data from Teammate 1 and returns the best-matched model
plus runner-ups and a human-readable reason.
"""

from typing import List
from config import DEFAULT_CATEGORY
from engine.scoring import rank_models


CATEGORY_REASON_TEMPLATES = {
    "coding": "matched because your prompt needs strong coding ability",
    "reasoning": "matched because your prompt needs deep multi-step reasoning",
    "creative_writing": "matched because your prompt is a creative/narrative writing task",
    "research": "matched because your prompt needs research depth and large context",
    "cheap_fast": "matched because speed and low cost were prioritized",
    "general": "matched as a well-rounded pick for a general-purpose prompt",
}


def _build_reason(model: dict, category: str) -> str:
    template = CATEGORY_REASON_TEMPLATES.get(category, CATEGORY_REASON_TEMPLATES["general"])
    return (
        f"{model['name']} was {template}. "
        f"Quality tier: {model['quality_tier']}, cost tier: {model['cost_tier']}, "
        f"speed tier: {model['speed_tier']}, context window: {model['context_window']:,} tokens."
    )


def auto_select(prompt_category: str, models: List[dict], top_n: int = 3) -> dict:
    """
    Returns:
        {
            "selected": <top model dict with score>,
            "reasoning": <str>,
            "alternatives": [<runner-up model dicts with score>, ...]
        }
    """
    category = prompt_category or DEFAULT_CATEGORY
    ranked = rank_models(models, category)

    if not ranked:
        raise ValueError("No models available to select from.")

    selected = ranked[0]
    alternatives = ranked[1:top_n]

    return {
        "selected": selected,
        "reasoning": _build_reason(selected, category),
        "alternatives": alternatives,
    }
