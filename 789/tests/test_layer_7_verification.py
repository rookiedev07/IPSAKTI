"""
Unit and Integration Tests for Layer 7 (Verification Agent)
"""

import pytest
from ip_sakti.core.mock_upstream import get_mock_scenario
from ip_sakti.core.schema import ContradictionSeverity, ClaimVerificationStatus
from ip_sakti.layer_7_verification.verification_agent import VerificationAgent
from ip_sakti.layer_7_verification.citation_checker import CitationChecker
from ip_sakti.layer_7_verification.contradiction_engine import ContradictionEngine


def test_verification_agent_classical_success():
    agent = VerificationAgent()
    upstream = get_mock_scenario("classical_chyawanprash")
    result = agent.verify(upstream)

    assert result.is_passed is True
    assert result.overall_groundedness_score >= 0.70
    assert result.citation_soundness_score >= 0.90
    assert result.jurisdiction_coherence_score == 1.0
    assert len(result.contradictions) == 0
    assert len(result.verified_claims) >= 2


def test_verification_agent_detects_critical_flaw():
    agent = VerificationAgent()
    flawed_upstream = get_mock_scenario("unsubstantiated_haldi_patent")
    result = agent.verify(flawed_upstream)

    # Verification must fail due to critical contradictions and ungrounded claims
    assert result.is_passed is False
    assert len(result.contradictions) >= 2

    conflict_types = [c.conflict_type for c in result.contradictions]
    assert "SECTION_3P_TK_CONFLICT" in conflict_types
    assert "BDA_NBA_APPROVAL_OMISSION" in conflict_types


def test_citation_checker_authenticity():
    upstream = get_mock_scenario("novel_phytopharmaceutical")
    validations, score = CitationChecker.validate_citations(upstream.citations_referenced)

    assert score == 1.0
    assert len(validations) == len(upstream.citations_referenced)
    for v in validations:
        assert v.is_valid_statute is True
        assert v.is_active_law is True


def test_contradiction_engine_direct():
    flawed = get_mock_scenario("unsubstantiated_haldi_patent")
    findings = ContradictionEngine.detect_contradictions(flawed)

    severities = [f.severity for f in findings]
    assert ContradictionSeverity.CRITICAL in severities


def test_tier_2_applicability_verifier():
    from ip_sakti.layer_7_verification.applicability_verifier import ApplicabilityVerifier

    classical = get_mock_scenario("classical_chyawanprash")
    findings, score = ApplicabilityVerifier.verify_applicability(classical)

    assert score >= 0.80
    statute_codes = [f.statute_code for f in findings]
    assert "PAT-SEC-3P" in statute_codes
    assert "DCR-RULE-158B" in statute_codes

    sec_3p_finding = next(f for f in findings if f.statute_code == "PAT-SEC-3P")
    assert sec_3p_finding.is_applicable is True
    assert len(sec_3p_finding.preconditions_met) > 0


def test_tier_3_conclusion_verifier():
    from ip_sakti.layer_7_verification.applicability_verifier import ApplicabilityVerifier
    from ip_sakti.layer_7_verification.conclusion_verifier import ConclusionVerifier

    # 1. Valid Classical Scenario
    classical = get_mock_scenario("classical_chyawanprash")
    app_findings, _ = ApplicabilityVerifier.verify_applicability(classical)
    conc_validations, conc_score = ConclusionVerifier.verify_conclusions(classical, app_findings)

    assert conc_score >= 0.80
    assert all(c.is_justified for c in conc_validations)

    # 2. Flawed Haldi Scenario (claims patent without synergy, skips NBA)
    flawed = get_mock_scenario("unsubstantiated_haldi_patent")
    app_flawed, _ = ApplicabilityVerifier.verify_applicability(flawed)
    conc_flawed_val, conc_flawed_score = ConclusionVerifier.verify_conclusions(flawed, app_flawed)

    assert conc_flawed_score < 0.80
    statuses = [c.logical_status for c in conc_flawed_val]
    assert "STATUTORY_BAR_CONTRADICTION" in statuses or "UNAUTHORIZED_EXEMPTION" in statuses

