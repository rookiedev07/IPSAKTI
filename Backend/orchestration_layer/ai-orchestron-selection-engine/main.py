"""
Demo entry point for the AI Selection & Decision Engine.

Run this to see the full flow:
  mock prompt (from Teammate 1)
      -> auto or manual model selection
      -> API key check + Gemini fallback if needed
      -> mocked API call
      -> structured output (for Teammate 2 / main-screen card)

Usage:
    python main.py
"""

import json

from config import MODELS_LIST_PATH
from schemas.input_schema import PromptInput
from schemas.output_schema import SelectionOutput, ModelSummary, AlternativeChoice
from engine.auto_selector import auto_select
from engine.manual_selector import get_model_by_id
from engine.scoring import score_components
from api_layer.key_manager import KeyManager
from api_layer.fallback import resolve_execution_model
from api_layer.api_router import call_ai_model
from logging_config import get_logger

logger = get_logger()


def load_models() -> list:
    with open(MODELS_LIST_PATH, "r") as f:
        return json.load(f)


def load_json(path: str):
    with open(path, "r") as f:
        return json.load(f)


def to_model_summary(model: dict) -> ModelSummary:
    return ModelSummary(
        id=model["id"],
        name=model["name"],
        provider=model["provider"],
        quality_tier=model["quality_tier"],
        cost_tier=model["cost_tier"],
        speed_tier=model["speed_tier"],
    )


def process_prompt(prompt_input: PromptInput, models: list, key_manager: KeyManager) -> SelectionOutput:
    """
    The main pipeline: selection -> fallback resolution -> mocked call -> structured output.
    This is the function Teammate 3 / the integration layer should call.
    """

    # --- 1. Selection: manual or auto ---
    if prompt_input.user_preferences.mode == "manual" and prompt_input.user_preferences.manual_model_id:
        chosen = get_model_by_id(models, prompt_input.user_preferences.manual_model_id)
        if chosen is None:
            raise ValueError(f"Manual model id '{prompt_input.user_preferences.manual_model_id}' not found.")
        chosen = dict(chosen)
        chosen["score"] = 1.0  # user-picked, score is not meaningful here
        reasoning = f"User manually selected {chosen['name']}."
        alternatives = []
    else:
        result = auto_select(prompt_input.category, models, top_n=3)
        chosen = result["selected"]
        reasoning = result["reasoning"]
        alternatives = result["alternatives"]

    # --- 2. Resolve execution model (handles API key + Gemini fallback) ---
    execution_model, fallback_used, api_key_status = resolve_execution_model(
        chosen, key_manager, models
    )

    # Raw attribute breakdown for the model that actually gets used --
    # this is what the UI's mixer-bar visualization is built from.
    category_used = prompt_input.category or "general"
    breakdown = score_components(execution_model, category_used)

    # --- 3. Call the AI (mocked) ---
    if api_key_status == "fallback_missing_key":
        response_text = "ERROR: No API key available for the selected model or the Gemini fallback."
    else:
        response_text = call_ai_model(execution_model, prompt_input.matched_prompt, key_manager)

    # --- 4. Build structured output for Teammate 2 ---
    output = SelectionOutput(
        prompt_id=prompt_input.prompt_id,
        problem=prompt_input.original_prompt,
        solution=response_text,
        selected_model=to_model_summary(execution_model),
        reasoning=reasoning if not fallback_used else (
            reasoning + f" NOTE: fell back to {execution_model['name']} because no API key "
            f"was available for the originally chosen provider."
        ),
        score=chosen.get("score", 1.0),
        score_breakdown=breakdown,
        alternatives=[
            AlternativeChoice(model=to_model_summary(alt), score=alt["score"])
            for alt in alternatives
        ],
        fallback_used=fallback_used,
        api_key_status=api_key_status,
        response_text=response_text,
    )

    # --- 5. Log the decision -- this is the audit trail for "why did the
    # engine pick this model", independent of anything the UI shows. ---
    logger.info(
        "DECISION prompt_id=%s category=%s mode=%s selected=%s(%s) score=%.4f "
        "fallback_used=%s api_key_status=%s",
        prompt_input.prompt_id,
        category_used,
        prompt_input.user_preferences.mode,
        execution_model["name"],
        execution_model["provider"],
        output.score,
        fallback_used,
        api_key_status,
    )
    if api_key_status == "fallback_missing_key":
        logger.warning(
            "NO KEY AVAILABLE prompt_id=%s -- neither the selected provider (%s) "
            "nor the Gemini fallback had a key on file.",
            prompt_input.prompt_id,
            chosen["provider"],
        )

    return output


def main():
    models = load_models()
    print(f"Loaded {len(models)} models.\n")

    # Set up API keys the way the user would at app start.
    mock_keys = load_json("mock_data/mock_keys.json")
    key_manager = KeyManager()
    key_manager.load_bulk(mock_keys)
    print(f"Keys available for: {list(mock_keys.keys())} (empty ones are treated as missing)\n")

    # --- Demo 1: primary mock input (auto mode, coding prompt) ---
    raw_input = load_json("mock_data/mock_input.json")
    prompt_input = PromptInput(**raw_input)

    print("=" * 70)
    print(f"PROMPT: {prompt_input.original_prompt}")
    output = process_prompt(prompt_input, models, key_manager)
    print(json.dumps(output.model_dump(), indent=2))
    print("=" * 70, "\n")

    # --- Demo 2: run through all variant prompts too ---
    variants = load_json("mock_data/mock_input_variants.json")
    for raw in variants:
        prompt_input = PromptInput(**raw)
        print("=" * 70)
        print(f"PROMPT: {prompt_input.original_prompt}")
        output = process_prompt(prompt_input, models, key_manager)
        print(f"-> Selected: {output.selected_model.name} ({output.selected_model.provider})")
        print(f"-> Fallback used: {output.fallback_used} | Key status: {output.api_key_status}")
        print(f"-> Reasoning: {output.reasoning}")
        print("=" * 70, "\n")


if __name__ == "__main__":
    main()
