"""
End-to-End Pipeline Integration Tests (Layers 7 -> 8 -> 9)
"""

import pytest
from ip_sakti.pipeline import IPSaktiPipeline
from ip_sakti.core.mock_upstream import list_mock_scenarios, get_mock_scenario
from ip_sakti.core.schema import LanguageCode, ConfidenceLevel


def test_full_pipeline_all_scenarios():
    pipeline = IPSaktiPipeline()
    scenarios = list_mock_scenarios()

    for sc_info in scenarios:
        sc_id = sc_info["id"]
        upstream = get_mock_scenario(sc_id)

        # Test English
        res_en = pipeline.process(upstream, target_language=LanguageCode.EN)
        assert res_en.execution_status == "SUCCESS"
        assert res_en.layer_9_response.target_language == LanguageCode.EN
        assert res_en.layer_7_verification is not None
        assert res_en.layer_8_confidence is not None

        # Test Hindi
        res_hi = pipeline.process(upstream, target_language=LanguageCode.HI)
        assert res_hi.layer_9_response.target_language == LanguageCode.HI

        # Test Marathi
        res_mr = pipeline.process(upstream, target_language=LanguageCode.MR)
        assert res_mr.layer_9_response.target_language == LanguageCode.MR


def test_full_pipeline_refusal_behaviour():
    pipeline = IPSaktiPipeline()
    flawed = get_mock_scenario("unsubstantiated_haldi_patent")

    res = pipeline.process(flawed, target_language=LanguageCode.EN)

    # Flawed scenario must result in refusal/safe escalation
    assert res.layer_7_verification.is_passed is False
    assert res.layer_8_confidence.overall_confidence in [ConfidenceLevel.REFUSAL, ConfidenceLevel.LOW]
    assert res.layer_9_response.safe_refusal_notice is not None
    assert res.layer_9_response.escalation_notice is not None
