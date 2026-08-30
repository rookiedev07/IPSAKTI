import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ip_sakti.citations import (
    retrieve_sources,
    retrieve_sources_by_jurisdiction_sections,
    validate_citations,
    compute_confidence,
    build_structured_response,
)
from ip_sakti.jurisdiction import detect_jurisdiction


def test_retrieve_sources_filters_by_jurisdiction():
    india_sources = retrieve_sources("patent traditional knowledge", jurisdiction="India")
    for s in india_sources:
        assert s["jurisdiction"] == "India"

    intl_sources = retrieve_sources("patent traditional knowledge", jurisdiction="International")
    for s in intl_sources:
        assert s["jurisdiction"] == "International"


def test_retrieve_sources_relevant_to_abs_query():
    results = retrieve_sources("access and benefit sharing biological resources", jurisdiction="India", top_k=3)
    ids = [s["id"] for s in results]
    assert "in-bd-act-2002" in ids


def test_jurisdiction_sections_kept_separate():
    """
    Core requirement from the PS: 'the two answer-sets kept visibly
    separate... so that answers are never conflated.'
    """
    sections = retrieve_sources_by_jurisdiction_sections("GI tag export PCT filing", "Both")
    assert "india" in sections and "international" in sections
    for s in sections["india"]:
        assert s["jurisdiction"] == "India"
    for s in sections["international"]:
        assert s["jurisdiction"] == "International"


def test_validate_citations_keeps_real_citation():
    sources = retrieve_sources("traditional knowledge patent", jurisdiction="India")
    real_id = sources[0]["id"]
    draft = f"This is barred under [{real_id}]."
    result = validate_citations(draft, sources)
    assert result["citation_count"] == 1
    assert len(result["hallucinated_ids"]) == 0


def test_validate_citations_strips_hallucinated_id():
    """
    This is the core hallucination guard the PS requires: 'never fabricate
    authority.' A citation ID that doesn't exist in the manifest must be
    caught and flagged, not silently trusted.
    """
    sources = retrieve_sources("traditional knowledge patent", jurisdiction="India")
    draft = "This is supported by [in-completely-made-up-section]."
    result = validate_citations(draft, sources)
    assert result["citation_count"] == 0
    assert "in-completely-made-up-section" in result["hallucinated_ids"]


def test_confidence_low_when_hallucination_detected():
    confidence = compute_confidence(citation_count=0, hallucinated_count=1, jurisdiction_confidence="high")
    assert confidence["level"] == "Low"
    assert confidence["needs_escalation"] is True


def test_confidence_high_with_good_citations_and_jurisdiction_match():
    confidence = compute_confidence(citation_count=2, hallucinated_count=0, jurisdiction_confidence="high")
    assert confidence["level"] == "High"
    assert confidence["needs_escalation"] is False


def test_build_structured_response_always_includes_disclaimer():
    jurisdiction_result = detect_jurisdiction("Can I patent my classical Ayurvedic formulation?")
    result = build_structured_response("Can I patent my classical Ayurvedic formulation?", jurisdiction_result)
    assert "not legal advice" in result["disclaimer"].lower()


def test_build_structured_response_with_draft_answer_validates_citations():
    prompt = "Do I need NBA approval before filing a patent on my formulation?"
    jurisdiction_result = detect_jurisdiction(prompt)
    sections = retrieve_sources_by_jurisdiction_sections(prompt, jurisdiction_result["suggested_toggle"])
    real_id = sections["india"][0]["id"] if sections["india"] else "in-bd-act-2002"
    draft = f"Yes, prior NBA approval is required under [{real_id}] before filing."

    result = build_structured_response(prompt, jurisdiction_result, draft_answer=draft)
    assert result["citation_validation"]["citation_count"] >= 1
    assert result["confidence"]["level"] in ("High", "Medium")
