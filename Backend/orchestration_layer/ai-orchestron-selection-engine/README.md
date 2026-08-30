# AI Orchestron — Selection & Decision Engine

This is your module for **Task 2** (AI model selection engine) and **Task 3**
(API key handling + Gemini fallback) of the AI Orchestron project.

## What this does

1. Takes a prompt (with a detected category, e.g. `"coding"`) from Teammate 1's
   prompt-matching engine.
2. Either lets the user **manually pick** a model from the curated list of 50,
   or **auto-selects** the best-fit model using a scoring framework.
3. Checks whether an API key exists for the chosen model's provider. If not,
   it **falls back to Gemini** automatically.
4. Calls the model — **REAL for Gemini** when a Google key is present (see
   `api_layer/api_router.py`), still mocked for every other provider — and
   returns a structured result Teammate 2 (output/orchestration) and the
   main-screen card can consume directly.
5. Logs every decision it makes to `logs/engine.log` (and the console) --
   see "Logging" below.

## How to run it

**Option A — the engine-tester mock UI:**
```bash
pip install -r requirements.txt --break-system-packages   # or use a venv
python server.py
```
Open **http://127.0.0.1:5000** for the plain engine tester (single-model auto/manual selection).

Open **http://127.0.0.1:5000/cards** for the "House of Cards" themed UI --
this deals out 5 fixed roles (Strategist, Researcher, Architect, Executor,
Verifier), each independently matched against your real engine using a
different scoring category (reasoning, research, general, coding,
cheap_fast respectively). It's a visual reference matching Teammate 2/3's
actual frontend concept, but every model pick, score, and fallback shown is
real -- it calls `/api/orchestrate`, which runs `process_prompt()` five
times, once per role.

**Option B — command-line only:**
```bash
python main.py             # runs the full demo pipeline on mock data
python -m pytest tests/    # runs the test suite
```
(Use `python3` instead of `python` on Mac/Linux if needed.)

## Folder structure

```
data/models_list.json        Curated list of 50 AI models + attributes
config.py                    All tunable constants (weights, fallback model, tiers)
server.py                    Flask API that exposes the engine to the browser UI

engine/
  scoring.py                 Core scoring framework (the "how do we decide" logic)
  auto_selector.py           Auto-decide mode
  manual_selector.py         Manual browse/filter/search mode

api_layer/
  key_manager.py             Stores user-provided API keys per provider
  fallback.py                Falls back to Gemini when no key is available
  api_router.py               Sends the request to the chosen model (MOCKED for now)

schemas/
  input_schema.py            Contract with Teammate 1 (what you receive)
  output_schema.py           Contract with Teammate 2 (what you send)

static/
  index.html                 Plain engine-tester UI -- calls /api/select
  house_of_cards.html        5-role themed UI -- calls /api/orchestrate

mock_data/                   Fake data standing in for Teammate 1 & 2's real formats
tests/                       Unit tests for scoring, selection, and fallback logic
main.py                      Demo entry point + the process_prompt() function server.py calls
```

## How the live UI talks to your engine

- `GET /api/models` -- returns `data/models_list.json` as-is, straight to the browser.
- `POST /api/select` -- takes a prompt (plus API keys) from the browser, builds a
  `PromptInput`, runs it through the exact same `process_prompt()` function used
  in `main.py`, and returns a `SelectionOutput` as JSON. This is the one function
  that ties your whole pipeline together -- selection, fallback resolution, the
  mocked model call, and the structured output all happen inside it.
- The browser never does any scoring itself anymore -- it only renders whatever
  the API sends back.
- `POST /api/orchestrate` -- used by `house_of_cards.html`. Takes one prompt,
  then internally calls `process_prompt()` **five times**, once per fixed role
  (`server.py -> ROLES`), each using a different scoring category. Returns all
  5 results in one response. This is what powers the "deal 5 agents" concept
  without needing 5 separate frontend requests.

## Integration points (read this before demo day)

- **Teammate 1 hands you data matching `schemas/input_schema.py`.** Once their
  real prompt engine is ready, you only need to update that one file (and
  maybe `mock_data/mock_input.json` for testing) — nothing in `engine/` should
  need to change.
- **You hand Teammate 2 data matching `schemas/output_schema.py`.** Same idea
  in reverse — this is the one file they should build their consumer against.
- **`api_layer/api_router.py` makes REAL calls to Gemini** when a Google key
  is present and `config.py -> ENABLE_REAL_GEMINI_CALLS = True` (the default).
  Every other provider is still mocked -- wire those in the same way once you
  have real keys/endpoints for them. If the real Gemini call fails for any
  reason (bad key, no internet, rate limit), it never crashes the request --
  it logs a warning and falls back to a clearly-labeled mock response.

## Real API calls (Gemini)

- Toggle: `config.py -> ENABLE_REAL_GEMINI_CALLS` (`True`/`False`). Turn it
  off if you want fully offline, fast, deterministic demos, or if you're
  worried about API quota during rehearsal.
- Model name: `config.py -> GEMINI_API_MODEL_NAME`. Adjust this if your
  Gemini API key has access to a different model name than the default.
- Unit tests never make real network calls -- `tests/test_server.py` forces
  `ENABLE_REAL_GEMINI_CALLS = False` for every test via a pytest fixture, so
  the test suite stays fast and doesn't depend on internet access or a real
  key.

## Logging

Every decision the engine makes is logged to `logs/engine.log` (auto-created
on first run) and echoed to the console. Each line records: prompt ID,
category, mode (auto/manual), the model actually used, its score, whether a
fallback happened, and the API key status. A separate `WARNING` line is
logged any time a role has no usable key anywhere (neither its own provider
nor Gemini). This is your answer if a judge asks "how do we know this isn't
random" -- open `logs/engine.log` and every decision is right there with its
reasoning trail.

## Tests

`tests/test_server.py` covers the Flask API directly (both `/api/select` and
`/api/orchestrate`), including: all 5 roles come back in the right order,
each agent has the full expected shape, the "zero keys anywhere" error case,
and the "Gemini-only key" fallback case. Run the whole suite with:
```bash
python -m pytest tests/ -v
```

## Known tuning point: the scoring weights

`config.py -> CRITERIA_WEIGHTS` controls how much quality, cost, speed, and
context window matter for each prompt category. This is the most important
thing to be ready to explain to judges — it's the actual "intelligence" of
your decision engine. If you want the demo to show more variety across
categories, tweak these weights and re-run `python3 main.py` to see the
effect immediately.

## Known limitation: the 50-model list

The list in `data/models_list.json` was built from current public leaderboard
research (LLM Stats, Vellum, BenchLM, Artificial Analysis) as of August 2026,
but AI model rankings shift weekly. Treat the tiers (`cost_tier`,
`speed_tier`, `quality_tier`) as reasonable approximations, not exact
benchmark numbers — refresh them from a live leaderboard if you have time
before the demo.
