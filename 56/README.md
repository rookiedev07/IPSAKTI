# IP-SAKTI Sahayak — Points 5 & 6

**Point 5 — Jurisdiction Layer**
**Point 6 — Citation & Evidence Layer**

Built to sit alongside the `789` folder (Points 7, 8, 9) inside the same
`ip_sakti` package namespace, so the two can be merged without import
changes.

## What this covers, against the actual PS text

> "a jurisdiction toggle (India vs international) with the two answer-sets
> kept visibly separate... so that answers are never conflated"
→ `ip_sakti/jurisdiction.py` + the `sources.india` / `sources.international`
split returned by every endpoint. Never a single blended list.

> "mandatory source citations with a confidence indicator"
→ `ip_sakti/citations.py` — retrieval, hallucination-guarded validation,
and a High/Medium/Low confidence score with a stated reason.

> "clearly state that it provides information and not legal advice"
→ `ip_sakti/disclaimer.py` — force-appended to every response, not left to
the LLM to remember.

> "never fabricate authority"
→ `validate_citations()` in `citations.py` strips any citation ID the
model used that doesn't actually exist in the source manifest.

## Setup & running

```bash
pip install -r requirements.txt
python run_server.py
```

Open **http://127.0.0.1:5050** for the standalone demo UI, or hit the API
directly (see below). Default port is 5050 to avoid colliding with the
Node backend (5000) if you run both side by side locally.

## API

- `GET  /api/health`
- `POST /api/jurisdiction/detect` — `{ "prompt": "..." }`
- `POST /api/citations/retrieve` — `{ "prompt": "...", "jurisdiction": "India"|"International"|"Both" (optional) }`
- `POST /api/structure-answer` — the main integration point. See Walkthrough.md.

## Files

```
ip_sakti/
  jurisdiction.py        Point 5 — jurisdiction detection
  citations.py            Point 6 — retrieval + hallucination-guarded validation
  disclaimer.py            Mandatory "not legal advice" text
  data/
    jurisdiction_keywords.json   Real Indian + international regime terms
    ip_sakti_sources.json         22-entry curated, version-tracked source manifest

main.py            Flask app / routes
run_server.py       Entry point
web/index.html       Standalone demo UI
tests/                14 tests covering both layers, including the hallucination guard
```

## Tests

```bash
python -m pytest tests/ -v
```
14 tests, all passing. Notably: `test_validate_citations_strips_hallucinated_id`
proves a fabricated citation ID gets caught and removed rather than trusted.

## Known scope limits (disclosed, not hidden)

- **Retrieval is keyword/topic matching, not a real vector database.** This
  matches the PS's own staged-delivery plan: *"a citation-grounded
  retrieval MVP first, then the graph and agentic layers."* Swap the
  internals of `retrieve_sources()` for real embedding search later --
  its function signature won't need to change.
- **The 22-entry source manifest is a curated starting set**, not the full
  corpus the PS describes (pharmacopoeial standards, registry records,
  case law). It's built from verified, real statutes/treaties -- see each
  entry's `url` -- but should be expanded before a real deployment.
- **Multilingual (Point 9) is out of scope here** -- that's your
  teammate's `789` folder.
