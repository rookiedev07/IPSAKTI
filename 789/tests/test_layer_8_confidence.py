"""
Unit and Integration Tests for Layer 8 (Confidence & Human Escalation)
"""

import pytest
from ip_sakti.core.mock_upstream import get_mock_scenario
from ip_sakti.core.schema import ConfidenceLevel, SpecialistRole
from ip_sakti.layer_7_verification.verification_agent import VerificationAgent
from ip_sakti.layer_8_confidence.confidence_engine import ConfidenceEngine


def test_confidence_engine_high_score():
    l7 = VerificationAgent()
    l8 = ConfidenceEngine()

    upstream = get_mock_scenario("classical_chyawanprash")
    v_res = l7.verify(upstream)
    conf = l8.evaluate_confidence(upstream, v_res)

    assert conf.overall_confidence == ConfidenceLevel.HIGH
    assert conf.numeric_score >= 0.80
    assert conf.is_safe_to_render is True
    assert conf.safe_refusal_text is None


def test_confidence_engine_refusal_on_critical_contra():
    l7 = VerificationAgent()
    l8 = ConfidenceEngine()

    flawed = get_mock_scenario("unsubstantiated_haldi_patent")
    v_res = l7.verify(flawed)
    conf = l8.evaluate_confidence(flawed, v_res)

    assert conf.overall_confidence in [ConfidenceLevel.REFUSAL, ConfidenceLevel.LOW]
    assert conf.is_safe_to_render is False
    assert conf.safe_refusal_text is not None
    assert "SAFE STATUTORY REFUSAL" in conf.safe_refusal_text
    assert conf.escalation_dossier.is_escalation_required is True
    assert conf.escalation_dossier.urgency_level == "IMMEDIATE"


def test_confidence_engine_phytopharmaceutical_escalation():
    l7 = VerificationAgent()
    l8 = ConfidenceEngine()

    phyto = get_mock_scenario("novel_phytopharmaceutical")
    v_res = l7.verify(phyto)
    conf = l8.evaluate_confidence(phyto, v_res)

    assert conf.overall_confidence in [ConfidenceLevel.HIGH, ConfidenceLevel.MEDIUM]
    # Phyto involves clinical trial protocols and NBA approval -> should trigger advisory escalation
    assert conf.escalation_dossier.is_escalation_required is True
    questions = conf.escalation_dossier.recommended_questions_for_counsel
    assert len(questions) > 0
    # Verify questions are dynamic and tailored to Giloy / Phytopharmaceutical / CDSCO / Form III
    assert any("CDSCO" in q or "phytopharmaceutical" in q or "Section 3(d)" in q for q in questions)


def test_confidence_engine_international_export_dynamic_questions():
    l7 = VerificationAgent()
    l8 = ConfidenceEngine()

    pct_scen = get_mock_scenario("international_pct_export")
    v_res = l7.verify(pct_scen)
    conf = l8.evaluate_confidence(pct_scen, v_res)

    assert conf.escalation_dossier.is_escalation_required is True
    questions = conf.escalation_dossier.recommended_questions_for_counsel
    assert len(questions) > 0
    # Must contain dynamic NBA Form III or ABS benefit sharing questions
    assert any("Form III" in q or "NBA" in q or "Section 6(1)" in q or "ABS" in q for q in questions)

