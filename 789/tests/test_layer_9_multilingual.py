"""
Unit and Integration Tests for Layer 9 (Multilingual Layer)
"""

import pytest
from ip_sakti.core.mock_upstream import get_mock_scenario
from ip_sakti.core.schema import LanguageCode, AyurvedaCategory
from ip_sakti.layer_7_verification.verification_agent import VerificationAgent
from ip_sakti.layer_8_confidence.confidence_engine import ConfidenceEngine
from ip_sakti.layer_9_multilingual.language_detector import LanguageDetector
from ip_sakti.layer_9_multilingual.localized_formatter import LocalizedFormatter


def test_language_detector():
    en_text = "Can I patent this Ayurvedic formulation in India?"
    hi_text = "क्या मैं भारत में इस आयुर्वेदिक दवा का पेटेंट करा सकता हूँ?"
    mr_text = "आम्ही या आयुर्वेदिक औषधाचे भारतात पेटंट घेऊ शकतो का आणि परवाना कसा मिळेल?"

    assert LanguageDetector.detect_language(en_text) == LanguageCode.EN
    assert LanguageDetector.detect_language(hi_text) == LanguageCode.HI
    assert LanguageDetector.detect_language(mr_text) == LanguageCode.MR


def test_localized_formatter_hindi():
    l7 = VerificationAgent()
    l8 = ConfidenceEngine()
    l9 = LocalizedFormatter()

    upstream = get_mock_scenario("classical_chyawanprash")
    v_res = l7.verify(upstream)
    conf = l8.evaluate_confidence(upstream, v_res)
    resp = l9.format_response(upstream, v_res, conf, forced_language=LanguageCode.HI)

    assert resp.target_language == LanguageCode.HI
    assert "शास्त्रीय आयुर्वेदिक औषधि" in resp.product_classification_badge
    assert len(resp.key_actionable_steps) > 0
    assert "वैधानिक कानूनी और विनियामक अस्वीकरण" in resp.statutory_disclaimer
    assert len(resp.bilingual_glossary) > 0


def test_localized_formatter_marathi():
    l7 = VerificationAgent()
    l8 = ConfidenceEngine()
    l9 = LocalizedFormatter()

    upstream = get_mock_scenario("classical_chyawanprash")
    v_res = l7.verify(upstream)
    conf = l8.evaluate_confidence(upstream, v_res)
    resp = l9.format_response(upstream, v_res, conf, forced_language=LanguageCode.MR)

    assert resp.target_language == LanguageCode.MR
    assert "शास्त्रीय आयुर्वेदिक औषध" in resp.product_classification_badge or "पारंपारिक" in resp.product_classification_badge
    assert len(resp.key_actionable_steps) > 0
    assert "कायदेशीर व विनियामक अस्वीकरण" in resp.statutory_disclaimer
