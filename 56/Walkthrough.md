# Walkthrough — Points 5 & 6

## The two-call integration pattern

`/api/structure-answer` is designed to be called **twice** around your
actual LLM call (the Groq call in `promptController.js`, or whatever the
final orchestrator uses) — once before, once after:

### Call 1 — BEFORE the LLM call, to get source context

```
POST /api/structure-answer
{ "prompt": "Can I patent my classical Ayurvedic formulation?" }
```

This returns `sources.india` and `sources.international` — the shortlisted
real statutes/treaties relevant to the question. Take these and inject them
into your system prompt, e.g.:

```
Here are the ONLY sources you may cite. Cite using their exact ID in
square brackets, like [in-patents-act-3p]. If none of these sources
support a claim you want to make, say so explicitly instead of citing
something not listed here.

- [in-patents-act-3p]: The Patents Act, 1970 — Section 3(p). Bars patenting
  an invention that is, in effect, traditional knowledge...
- [in-tkdl]: Traditional Knowledge Digital Library (TKDL)...
```

This is what turns "the model might cite something real" into "the model
can only choose from a pre-verified list" — a much stronger guarantee.

### Call 2 — AFTER the LLM call, to validate what it actually did

```
POST /api/structure-answer
{
  "prompt": "Can I patent my classical Ayurvedic formulation?",
  "draft_answer": "<the raw text the LLM returned>"
}
```

This re-runs retrieval AND checks every `[citation-id]` marker in
`draft_answer` against the real manifest. Anything the model cited that
isn't real gets caught in `citation_validation.hallucinated_ids` and
excluded from `confirmed_citations`. The `confidence` field then reflects
that: even a fluent, confident-sounding answer gets marked "Low" if it
cited something fake.

## Why jurisdiction detection is separate from citation retrieval

Two different failure modes, two different fixes:

- Point 5 answers "which law/country applies here" — get this wrong and
  you show the user Indian patent rules for a question about US filing.
- Point 6 answers "is this specific claim actually backed by something
  real" — get this wrong and you get a confident-sounding hallucination.

Keeping them as separate functions (`detect_jurisdiction()` vs
`retrieve_sources()` / `validate_citations()`) means each can be tested,
tuned, and explained independently — which matters a lot if a judge asks
"how does X work" and you need a clean answer for each piece.

## What "kept visibly separate" actually means in the data shape

The PS's wording — "never conflated" — is the reason `sources` is returned
as `{ "india": [...], "international": [...] }` rather than one flat list
with a jurisdiction field on each item. It would be easy for a frontend
developer to accidentally render a flat list as one merged block; the
split-object shape makes that mistake much harder to make by accident.

If the frontend renders two visually distinct columns (see `web/index.html`
for a working example), that satisfies the requirement directly — a user
should never have to mentally sort Indian and international answers apart
themselves.

## Extending the source manifest

To add a new source, add an entry to
`ip_sakti/data/ip_sakti_sources.json` with all of: `id` (unique, kebab-case,
prefixed `in-` or `intl-`), `title`, `type`, `section_or_article`,
`jurisdiction` (must be exactly `"India"` or `"International"`), `topic`
(array of lowercase tags used for retrieval matching), `source_portal`,
`url`, `version`, `last_verified`, `summary`. No code changes needed —
both `retrieve_sources()` and `validate_citations()` read the manifest at
import time.

## Extending jurisdiction keywords

Same idea — add terms to
`ip_sakti/data/jurisdiction_keywords.json` under the appropriate
`india`/`international` group. Keywords are matched as substrings after
lowercasing and normalizing hyphens to spaces, so multi-word phrases
("gi tag") will match hyphenated real-world phrasing ("GI-tagged") too.
