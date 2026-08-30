"""
Points 5 & 6 API -- Jurisdiction Layer + Citation & Evidence Layer.

Run with:
    python run_server.py

Endpoints:
    GET  /api/health
    POST /api/jurisdiction/detect      { "prompt": "..." }
    POST /api/citations/retrieve       { "prompt": "...", "jurisdiction": "India"|"International"|"Both" (optional) }
    POST /api/structure-answer         { "prompt": "...", "draft_answer": "..." (optional), "jurisdiction_override": "..." (optional) }

`/api/structure-answer` is the main integration point: call it either
BEFORE your LLM call (to get the source context to inject into the system
prompt) or AFTER (passing the model's draft_answer to validate its
citations and get a confidence score). See Walkthrough.md for the full
two-call integration pattern.
"""

from flask import Flask, request, jsonify, send_from_directory

from ip_sakti.jurisdiction import detect_jurisdiction
from ip_sakti.citations import (
    retrieve_sources_by_jurisdiction_sections,
    build_structured_response,
)

app = Flask(__name__, static_folder="web", static_url_path="")


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "IP-SAKTI Jurisdiction & Citation Layer operational",
        "points_covered": [5, 6],
    })


@app.route("/api/jurisdiction/detect", methods=["POST"])
def jurisdiction_detect():
    payload = request.get_json(force=True, silent=True) or {}
    prompt = (payload.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "prompt is required"}), 400

    return jsonify(detect_jurisdiction(prompt))


@app.route("/api/citations/retrieve", methods=["POST"])
def citations_retrieve():
    payload = request.get_json(force=True, silent=True) or {}
    prompt = (payload.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "prompt is required"}), 400

    jurisdiction_override = payload.get("jurisdiction")
    if jurisdiction_override:
        toggle = jurisdiction_override
    else:
        toggle = detect_jurisdiction(prompt)["suggested_toggle"]

    sections = retrieve_sources_by_jurisdiction_sections(prompt, toggle)
    return jsonify({
        "suggested_toggle": toggle,
        "sources": sections,
    })


@app.route("/api/structure-answer", methods=["POST"])
def structure_answer():
    payload = request.get_json(force=True, silent=True) or {}
    prompt = (payload.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "prompt is required"}), 400

    draft_answer = payload.get("draft_answer")
    jurisdiction_override = payload.get("jurisdiction_override")

    if jurisdiction_override:
        jurisdiction_result = {
            "suggested_toggle": jurisdiction_override,
            "matched_india_terms": [],
            "matched_international_terms": [],
            "confidence": "user_override",
            "reasoning": "Jurisdiction was manually set by the user, overriding auto-detection.",
        }
    else:
        jurisdiction_result = detect_jurisdiction(prompt)

    result = build_structured_response(prompt, jurisdiction_result, draft_answer)
    return jsonify(result)


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


if __name__ == "__main__":
    app.run(debug=False, port=5050)
