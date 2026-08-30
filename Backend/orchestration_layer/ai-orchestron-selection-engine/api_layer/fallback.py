"""
Task 3: fallback logic. If the selected/chosen model's provider has no
API key on file, fall back to Gemini (which the user must provide at
app start, per the brief).
"""

from typing import List, Tuple
from config import FALLBACK_MODEL_ID, FALLBACK_PROVIDER
from api_layer.key_manager import KeyManager
from engine.manual_selector import get_model_by_id


def resolve_execution_model(
    selected_model: dict,
    key_manager: KeyManager,
    models: List[dict],
) -> Tuple[dict, bool, str]:
    """
    Decides which model actually gets called.

    Returns: (model_to_use, fallback_used: bool, api_key_status: str)

    api_key_status is one of: "ok", "fallback_used", "fallback_missing_key"
    """
    if key_manager.has_key(selected_model["provider"]):
        return selected_model, False, "ok"

    # No key for the chosen model -> try Gemini fallback
    if key_manager.has_fallback_key():
        fallback_model = get_model_by_id(models, FALLBACK_MODEL_ID)
        if fallback_model is None:
            raise ValueError(
                f"FALLBACK_MODEL_ID '{FALLBACK_MODEL_ID}' not found in models list."
            )
        return fallback_model, True, "fallback_used"

    # No key for chosen model AND no Gemini key either -> hard failure state.
    # Teammate 2 / frontend should surface this as "please add an API key".
    return selected_model, False, "fallback_missing_key"
