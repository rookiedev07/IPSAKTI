"""
Local API server that wraps the REAL engine (engine/, api_layer/, schemas/)
so the mock UI (static/index.html) can call it over HTTP instead of using
its own JS re-implementation of the scoring logic.

Run with:
    python server.py

Then open:
    http://127.0.0.1:5000

Every request to /api/select runs through the exact same process_prompt()
function used in main.py -- so what you see in the browser IS your real
engine, not a simulation of it.
"""

from flask import Flask, request, jsonify, send_from_directory
from pydantic import ValidationError
import time

from main import load_models, process_prompt
from schemas.input_schema import PromptInput
from api_layer.key_manager import KeyManager
from logging_config import get_logger

logger = get_logger()

app = Flask(__name__, static_folder="static", static_url_path="")

# The 5 fixed roles the "House of Cards" UI deals out for every prompt.
# Each role maps to one of the existing scoring categories in config.py --
# this is what makes the whole multi-agent deal real instead of decorative.
ROLES = [
    {"id": "strategist", "name": "Strategist", "subtitle": "Orchestration & Logic", "rank": "A", "category": "reasoning"},
    {"id": "researcher",  "name": "Researcher",  "subtitle": "Context & Search",      "rank": "2", "category": "research"},
    {"id": "architect",   "name": "Architect",   "subtitle": "System Design",         "rank": "3", "category": "general"},
    {"id": "executor",    "name": "Executor",    "subtitle": "Code Generation",       "rank": "4", "category": "coding"},
    {"id": "verifier",    "name": "Verifier",    "subtitle": "Testing & QA",          "rank": "5", "category": "cheap_fast"},
]


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/cards")
def house_of_cards():
    return send_from_directory(app.static_folder, "house_of_cards.html")


@app.route("/api/models", methods=["GET"])
def get_models():
    """Returns the full 50-model list, straight from data/models_list.json."""
    return jsonify(load_models())


@app.route("/api/select", methods=["POST"])
def select():
    """
    Runs a prompt through the real engine end-to-end: selection -> fallback
    resolution -> mocked model call -> structured output.

    Expected JSON body:
    {
      "prompt_id": "web-001",
      "original_prompt": "...",
      "matched_prompt": "...",
      "category": "coding",            (optional, defaults to "general")
      "tags": [],                       (optional)
      "user_preferences": {
        "mode": "auto" | "manual",
        "manual_model_id": "claude-sonnet-5" or null
      },
      "keys": { "Google": "...", "Anthropic": "..." }   -- separate from the schema on purpose
    }
    """
    payload = request.get_json(force=True, silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    keys_data = payload.pop("keys", {})

    try:
        prompt_input = PromptInput(**payload)
    except ValidationError as e:
        return jsonify({"error": "Invalid prompt input.", "details": e.errors()}), 400

    key_manager = KeyManager()
    try:
        key_manager.load_bulk(keys_data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    models = load_models()

    try:
        output = process_prompt(prompt_input, models, key_manager)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return app.response_class(
        response=output.model_dump_json(),
        status=200,
        mimetype="application/json",
    )


@app.route("/api/orchestrate", methods=["POST"])
def orchestrate():
    """
    Runs ONE prompt through the real engine 5 TIMES -- once per fixed role
    (Strategist, Researcher, Architect, Executor, Verifier) -- each using a
    different scoring category, so each role gets its own genuinely best-fit
    model instead of all 5 landing on the same pick.

    Expected JSON body:
    {
      "prompt": "write me a letter",
      "keys": { "Google": "...", "Anthropic": "..." }
    }

    Returns:
    {
      "problem": "...",
      "agents": [
        {
          "role": "Strategist", "subtitle": "Orchestration & Logic", "rank": "A",
          "category": "reasoning",
          "selected_model": {...}, "reasoning": "...", "score": 0.8,
          "score_breakdown": {...}, "fallback_used": false,
          "api_key_status": "ok", "response_text": "..."
        },
        ...
      ]
    }
    """
    payload = request.get_json(force=True, silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    prompt_text = (payload.get("prompt") or "").strip()
    if not prompt_text:
        return jsonify({"error": "Prompt cannot be empty."}), 400

    keys_data = payload.get("keys", {})
    logger.info(
        "ORCHESTRATE request | prompt=%r | keys_provided=%s | roles=%d",
        prompt_text[:100], sorted(keys_data.keys()), len(ROLES),
    )
    models = load_models()
    agents = []

    for role in ROLES:
        key_manager = KeyManager()
        try:
            key_manager.load_bulk(keys_data)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        prompt_input = PromptInput(
            prompt_id=f"{role['id']}-{int(time.time() * 1000)}",
            original_prompt=prompt_text,
            matched_prompt=prompt_text,
            category=role["category"],
            tags=[],
            user_preferences={"mode": "auto", "manual_model_id": None},
        )

        try:
            output = process_prompt(prompt_input, models, key_manager)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        agents.append({
            "role": role["name"],
            "subtitle": role["subtitle"],
            "rank": role["rank"],
            "category": role["category"],
            "selected_model": output.selected_model.model_dump(),
            "reasoning": output.reasoning,
            "score": output.score,
            "score_breakdown": output.score_breakdown,
            "fallback_used": output.fallback_used,
            "api_key_status": output.api_key_status,
            "response_text": output.response_text,
        })

    error_count = sum(1 for a in agents if a["api_key_status"] == "fallback_missing_key")
    fallback_count = sum(1 for a in agents if a["fallback_used"])
    logger.info(
        "ORCHESTRATE complete | prompt=%r | 5/5 agents delivered | fallbacks=%d | missing_key_errors=%d",
        prompt_text[:100], fallback_count, error_count,
    )

    return jsonify({"problem": prompt_text, "agents": agents})


if __name__ == "__main__":
    app.run(debug=False, port=5000)
