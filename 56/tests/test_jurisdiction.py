import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ip_sakti.jurisdiction import detect_jurisdiction


def test_india_only_prompt_detected_as_india():
    result = detect_jurisdiction("Do I need NBA approval under the Biological Diversity Act before filing a patent?")
    assert result["suggested_toggle"] == "India"
    assert len(result["matched_india_terms"]) > 0
    assert len(result["matched_international_terms"]) == 0


def test_international_only_prompt_detected_as_international():
    result = detect_jurisdiction("How does the WIPO GRATK treaty disclosure requirement affect my PCT filing?")
    assert result["suggested_toggle"] == "International"
    assert len(result["matched_international_terms"]) > 0


def test_mixed_prompt_detected_as_both():
    result = detect_jurisdiction(
        "I have a GI-tagged Ayurvedic formulation under the Geographical Indications Act "
        "and want to export it -- do I need a PCT filing too?"
    )
    assert result["suggested_toggle"] == "Both"
    assert len(result["matched_india_terms"]) > 0
    assert len(result["matched_international_terms"]) > 0


def test_neutral_prompt_defaults_to_india_with_low_confidence():
    result = detect_jurisdiction("What category does my herbal face cream fall under?")
    assert result["suggested_toggle"] == "India"
    assert result["confidence"] == "low"


def test_empty_prompt_does_not_crash():
    result = detect_jurisdiction("")
    assert result["suggested_toggle"] == "India"
    assert result["confidence"] == "low"
