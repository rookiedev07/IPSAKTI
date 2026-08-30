"""
Point 5 -- Jurisdiction Layer.

The PS is explicit that this must be "a jurisdiction toggle (India vs
international) with the two answer-sets kept visibly separate... so that
answers are never conflated." This module does NOT decide the final
jurisdiction on the user's behalf -- it SUGGESTS a default toggle position
based on the prompt text, which the frontend should let the user override.

Detection is deliberately rule-based (keyword/phrase matching against a
curated list of real Indian and international IP/regulatory regimes -- see
data/jurisdiction_keywords.json) rather than an LLM call. For a compliance
tool, a deterministic, auditable decision is more defensible than an LLM
guess, and it's instant + free.
"""

import json
import os
from typing import Dict, List

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "jurisdiction_keywords.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    _KEYWORDS = json.load(f)

# Flatten each side's keyword groups into one lowercase list for matching.
_INDIA_TERMS: List[str] = [t.lower() for group in _KEYWORDS["india"].values() for t in group]
_INTL_TERMS: List[str] = [t.lower() for group in _KEYWORDS["international"].values() for t in group]


def _normalize(text: str) -> str:
    """Lowercase and turn hyphens/underscores into spaces so phrasing like
    'GI-tagged' or 'ayurveda_aahar' still matches keyword phrases written
    with spaces (e.g. 'gi tag')."""
    text = (text or "").lower()
    return text.replace("-", " ").replace("_", " ")


def detect_jurisdiction(prompt_text: str) -> Dict:
    """
    Suggests a jurisdiction toggle position for the given prompt.

    Returns:
        {
            "suggested_toggle": "India" | "International" | "Both",
            "matched_india_terms": [...],
            "matched_international_terms": [...],
            "confidence": "high" | "medium" | "low",
            "reasoning": "<human-readable explanation>"
        }

    The frontend should pre-select `suggested_toggle` but always let the
    user manually switch it -- this function is a helpful default, not an
    authority on jurisdiction.
    """
    text = _normalize(prompt_text)

    matched_india = sorted({term for term in _INDIA_TERMS if term in text})
    matched_intl = sorted({term for term in _INTL_TERMS if term in text})

    has_india = len(matched_india) > 0
    has_intl = len(matched_intl) > 0

    if has_india and has_intl:
        toggle = "Both"
        confidence = "high"
        reasoning = (
            f"Detected both India-specific terms ({', '.join(matched_india[:3])}) "
            f"and international terms ({', '.join(matched_intl[:3])}) -- "
            f"this query likely needs both jurisdictions answered separately."
        )
    elif has_india:
        toggle = "India"
        confidence = "high" if len(matched_india) >= 2 else "medium"
        reasoning = f"Detected India-specific terms: {', '.join(matched_india[:5])}."
    elif has_intl:
        toggle = "International"
        confidence = "high" if len(matched_intl) >= 2 else "medium"
        reasoning = f"Detected international terms: {', '.join(matched_intl[:5])}."
    else:
        # No explicit signal -- Ayurveda IP questions are India-centric by
        # default, so default to India rather than leaving it ambiguous.
        toggle = "India"
        confidence = "low"
        reasoning = (
            "No explicit jurisdiction terms detected. Defaulting to India, "
            "since Ayurveda IP/regulatory questions are India-centric by "
            "default -- but this is a low-confidence guess. Confirm with the user."
        )

    return {
        "suggested_toggle": toggle,
        "matched_india_terms": matched_india,
        "matched_international_terms": matched_intl,
        "confidence": confidence,
        "reasoning": reasoning,
    }
