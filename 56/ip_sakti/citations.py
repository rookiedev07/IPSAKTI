"""
Point 6 -- Citation & Evidence Layer.

Two responsibilities, and they must stay separate:

1. RETRIEVAL: given a prompt + jurisdiction, shortlist the most relevant
   entries from the curated source manifest (data/ip_sakti_sources.json).

2. VALIDATION: after an LLM produces a draft answer that cites sources by
   ID, strip out any citation ID that doesn't actually exist in the
   manifest. This is the hallucination guard the PS requires ("never
   fabricate authority") -- it does not trust the model's citations, it
   verifies them against ground truth.

Retrieval here is keyword/topic matching, not a real vector database --
that's a deliberate, disclosed scope choice for the hackathon MVP (the PS
itself describes staged delivery: "a citation-grounded retrieval MVP
first, then the graph and agentic layers"). Swap `retrieve_sources()`'s
internals for real embedding search later without touching its signature.
"""

import json
import os
import re
from typing import Dict, List, Optional

from ip_sakti.disclaimer import build_footer

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "ip_sakti_sources.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    _SOURCES: List[Dict] = json.load(f)

_SOURCES_BY_ID: Dict[str, Dict] = {s["id"]: s for s in _SOURCES}

# Matches citation markers like [in-patents-act-3p] or [intl-cbd] in model output.
_CITATION_PATTERN = re.compile(r"\[([a-z0-9\-]+)\]")


def _score_source(source: Dict, query_terms: List[str]) -> int:
    """Simple overlap score between query terms and a source's topic tags + title."""
    haystack = " ".join(source.get("topic", [])) + " " + source["title"].lower()
    haystack = haystack.lower()
    return sum(1 for term in query_terms if term in haystack)


def retrieve_sources(prompt_text: str, jurisdiction: str = "Both", top_k: int = 5) -> List[Dict]:
    """
    Returns up to top_k sources most relevant to prompt_text, filtered by
    jurisdiction ("India", "International", or "Both").
    """
    query_terms = [w for w in re.findall(r"[a-z]{4,}", (prompt_text or "").lower())]

    if jurisdiction == "Both":
        candidates = _SOURCES
    else:
        candidates = [s for s in _SOURCES if s["jurisdiction"] == jurisdiction]

    scored = [(_score_source(s, query_terms), s) for s in candidates]
    scored.sort(key=lambda pair: pair[0], reverse=True)

    # If nothing scored above 0, still return the top general-purpose entries
    # for that jurisdiction rather than an empty list -- an empty citation
    # list looks like a bug, not "no relevant law," to a user.
    nonzero = [s for score, s in scored if score > 0]
    if nonzero:
        return nonzero[:top_k]
    return [s for _, s in scored[:top_k]]


def retrieve_sources_by_jurisdiction_sections(prompt_text: str, suggested_toggle: str, top_k: int = 4) -> Dict[str, List[Dict]]:
    """
    Builds the "kept visibly separate" structure the PS requires: separate
    India and International source lists, never merged into one blended list.
    """
    sections = {"india": [], "international": []}

    if suggested_toggle in ("India", "Both"):
        sections["india"] = retrieve_sources(prompt_text, jurisdiction="India", top_k=top_k)
    if suggested_toggle in ("International", "Both"):
        sections["international"] = retrieve_sources(prompt_text, jurisdiction="International", top_k=top_k)

    return sections


def validate_citations(answer_text: str, allowed_sources: List[Dict]) -> Dict:
    """
    Scans answer_text for citation markers like [source-id] and checks each
    one against allowed_sources. Any ID not found in allowed_sources is
    flagged as hallucinated and stripped from the "confirmed" list.

    Returns:
        {
            "confirmed_citations": [<source dict>, ...],
            "hallucinated_ids": [<id strings not found in manifest>, ...],
            "citation_count": int,
        }
    """
    allowed_ids = {s["id"] for s in allowed_sources}
    cited_ids = set(_CITATION_PATTERN.findall(answer_text or ""))

    confirmed_ids = cited_ids & allowed_ids
    hallucinated_ids = sorted(cited_ids - allowed_ids)

    confirmed = [_SOURCES_BY_ID[cid] for cid in confirmed_ids if cid in _SOURCES_BY_ID]

    return {
        "confirmed_citations": confirmed,
        "hallucinated_ids": sorted(hallucinated_ids),
        "citation_count": len(confirmed),
    }


def compute_confidence(citation_count: int, hallucinated_count: int, jurisdiction_confidence: str) -> Dict:
    """
    Combines citation coverage + jurisdiction-detection confidence into a
    single High/Medium/Low rating with a stated reason, per the PS's
    "confidence indicator" and "safe abstention" requirements.
    """
    if hallucinated_count > 0:
        return {
            "level": "Low",
            "reason": (
                f"{hallucinated_count} cited source(s) could not be verified against the "
                f"source manifest and were removed. Treat this answer as low-confidence "
                f"and verify manually."
            ),
            "needs_escalation": True,
        }

    if citation_count == 0:
        return {
            "level": "Low",
            "reason": "No verifiable citations were found for this query. Abstaining from a confident answer.",
            "needs_escalation": True,
        }

    if citation_count >= 2 and jurisdiction_confidence == "high":
        return {
            "level": "High",
            "reason": f"{citation_count} verified citation(s) with high-confidence jurisdiction match.",
            "needs_escalation": False,
        }

    return {
        "level": "Medium",
        "reason": f"{citation_count} verified citation(s), but jurisdiction match confidence was '{jurisdiction_confidence}'.",
        "needs_escalation": jurisdiction_confidence == "low",
    }


def build_structured_response(
    prompt_text: str,
    jurisdiction_result: Dict,
    draft_answer: Optional[str] = None,
) -> Dict:
    """
    The main entry point most callers should use. Combines jurisdiction
    detection output (from ip_sakti.jurisdiction.detect_jurisdiction) with
    citation retrieval, optional citation validation against a draft
    answer, confidence scoring, and the mandatory disclaimer.
    """
    toggle = jurisdiction_result["suggested_toggle"]
    sections = retrieve_sources_by_jurisdiction_sections(prompt_text, toggle)

    all_candidate_sources = sections["india"] + sections["international"]

    if draft_answer:
        validation = validate_citations(draft_answer, all_candidate_sources)
    else:
        # No draft answer to validate yet -- this call is being used purely
        # for retrieval (e.g. to build the system prompt's source context
        # before calling the LLM).
        validation = {
            "confirmed_citations": [],
            "hallucinated_ids": [],
            "citation_count": 0,
        }

    confidence = compute_confidence(
        citation_count=validation["citation_count"],
        hallucinated_count=len(validation["hallucinated_ids"]),
        jurisdiction_confidence=jurisdiction_result["confidence"],
    )

    return {
        "jurisdiction": jurisdiction_result,
        "sources": {
            "india": sections["india"],
            "international": sections["international"],
        },
        "citation_validation": validation,
        "confidence": confidence,
        "disclaimer": build_footer(needs_escalation=confidence["needs_escalation"]),
    }
