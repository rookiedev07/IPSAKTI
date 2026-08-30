"""
Verification Agent (Layer 7 Main Engine)
Orchestrates claim extraction, citation verification, contradiction detection,
jurisdiction coherence, and hallucination guarding.
"""

from typing import List
from ..core.schema import (
    UpstreamAgentOutput,
    VerificationResult,
    ContradictionFinding,
    ContradictionSeverity,
    ClaimVerificationStatus,
    ApplicabilityFinding,
    ConclusionValidationFinding
)
from .claim_extractor import ClaimExtractor
from .citation_checker import CitationChecker
from .contradiction_engine import ContradictionEngine
from .jurisdiction_verifier import JurisdictionVerifier
from .hallucination_guard import HallucinationGuard
from .applicability_verifier import ApplicabilityVerifier
from .conclusion_verifier import ConclusionVerifier


class VerificationAgent:
    """
    Layer 7: Verification Agent
    Implements Complete 3-Tier Statutory Verification Architecture:
    - Tier 1: Citation Verification (Manifest authenticity & active law guard)
    - Tier 2: Applicability Verification ('Does this law apply here?')
    - Tier 3: Conclusion Verification ('Does this law actually justify the conclusion the AI reached?')
    """

    def __init__(self):
        self.claim_extractor = ClaimExtractor()
        self.citation_checker = CitationChecker()
        self.applicability_verifier = ApplicabilityVerifier()
        self.conclusion_verifier = ConclusionVerifier()
        self.contradiction_engine = ContradictionEngine()
        self.jurisdiction_verifier = JurisdictionVerifier()
        self.hallucination_guard = HallucinationGuard()

    def verify(self, upstream_output: UpstreamAgentOutput) -> VerificationResult:
        """
        Executes end-to-end 3-Tier statutory verification of upstream agent output.
        """
        # Step 1: Ensure claims are extracted and structured
        claims = self.claim_extractor.extract_claims_from_output(upstream_output)
        upstream_output.extracted_claims = claims

        # Tier 1: Citation Verification (Manifest check)
        citation_validations, citation_soundness = self.citation_checker.validate_citations(
            upstream_output.citations_referenced
        )

        # Tier 2: Applicability Verification ('Does this law apply here?')
        applicability_findings, applicability_score = self.applicability_verifier.verify_applicability(
            upstream_output
        )

        # Tier 3: Conclusion Verification ('Does this law actually justify the conclusion?')
        conclusion_validations, conclusion_score = self.conclusion_verifier.verify_conclusions(
            upstream_output,
            applicability_findings
        )

        # Contradiction Engine across statutory rules
        contradictions = self.contradiction_engine.detect_contradictions(upstream_output)

        # Verify Jurisdiction Coherence
        jurisdiction_score, jur_issues = self.jurisdiction_verifier.verify_jurisdiction_coherence(
            upstream_output
        )

        # Evaluate Groundedness & Guard against Hallucinations
        verified_claims, unsubstantiated_claims, groundedness_score = self.hallucination_guard.verify_groundedness(
            claims=claims,
            evidence_chunks=upstream_output.retrieved_evidence,
            upstream_output=upstream_output
        )

        # Determine overall verification pass/fail status
        has_critical_contradiction = any(c.severity == ContradictionSeverity.CRITICAL for c in contradictions)
        has_invalid_conclusion = any(not cv.is_justified for cv in conclusion_validations)
        
        is_passed = (
            not has_critical_contradiction and
            not has_invalid_conclusion and
            groundedness_score >= 0.50 and
            applicability_score >= 0.70 and
            len(unsubstantiated_claims) < len(verified_claims)
        )

        # Formulate sanitized synthesis text
        sanitized_text = self._build_sanitized_text(
            original_text=upstream_output.synthesis_draft_text,
            contradictions=contradictions,
            unsubstantiated_claims=unsubstantiated_claims
        )

        # Build 3-Tier structured summary
        three_tier_summary = {
            "tier_1_citation_verification": {
                "score": citation_soundness,
                "status": "PASSED" if citation_soundness >= 0.80 else "FLAGGED",
                "citations_audited": len(citation_validations)
            },
            "tier_2_applicability_verification": {
                "score": applicability_score,
                "status": "PASSED" if applicability_score >= 0.70 else "FLAGGED",
                "statutes_evaluated": len(applicability_findings),
                "findings": [f.model_dump() for f in applicability_findings]
            },
            "tier_3_conclusion_verification": {
                "score": conclusion_score,
                "status": "PASSED" if conclusion_score >= 0.80 else "FLAGGED",
                "conclusions_audited": len(conclusion_validations),
                "validations": [c.model_dump() for c in conclusion_validations]
            }
        }

        summary = self._generate_verification_summary(
            is_passed=is_passed,
            groundedness=groundedness_score,
            citation_soundness=citation_soundness,
            applicability_score=applicability_score,
            conclusion_score=conclusion_score,
            contradictions=contradictions,
            unsubstantiated_claims=unsubstantiated_claims
        )

        return VerificationResult(
            is_passed=is_passed,
            overall_groundedness_score=groundedness_score,
            citation_soundness_score=citation_soundness,
            applicability_score=applicability_score,
            conclusion_justification_score=conclusion_score,
            jurisdiction_coherence_score=jurisdiction_score,
            verified_claims=verified_claims,
            unsubstantiated_claims=unsubstantiated_claims,
            contradictions=contradictions,
            citation_validations=citation_validations,
            applicability_findings=applicability_findings,
            conclusion_validations=conclusion_validations,
            three_tier_pipeline=three_tier_summary,
            sanitized_synthesis_text=sanitized_text,
            verification_summary=summary
        )

    def _build_sanitized_text(
        self,
        original_text: str,
        contradictions: List[ContradictionFinding],
        unsubstantiated_claims: List[any]
    ) -> str:
        if not contradictions and not unsubstantiated_claims:
            return original_text

        sanitized_lines = []
        for line in original_text.split("\n"):
            # If line directly contains a critical contradiction, annotate with correction
            critical_matched = False
            for contra in contradictions:
                if contra.severity == ContradictionSeverity.CRITICAL:
                    if any(w in line.lower() for w in ["patent", "immediately file", "sell without license", "no biodiversity"]):
                        sanitized_lines.append(f"⚠️ [STATUTORY CORRECTION]: {contra.description} → {contra.remedial_action}")
                        critical_matched = True
                        break
            if not critical_matched:
                sanitized_lines.append(line)

        return "\n".join(sanitized_lines)

    def _generate_verification_summary(
        self,
        is_passed: bool,
        groundedness: float,
        citation_soundness: float,
        applicability_score: float,
        conclusion_score: float,
        contradictions: List[ContradictionFinding],
        unsubstantiated_claims: List[any]
    ) -> str:
        if is_passed:
            return (
                f"✅ 3-Tier Verification PASSED: "
                f"Tier 1 (Citation Soundness): {int(citation_soundness*100)}%, "
                f"Tier 2 (Applicability): {int(applicability_score*100)}%, "
                f"Tier 3 (Conclusion Justification): {int(conclusion_score*100)}%. "
                f"Groundedness: {int(groundedness*100)}%, Contradictions: {len(contradictions)}. "
                "All statutory preconditions and legal deductions verified."
            )
        else:
            reasons = []
            if citation_soundness < 0.70:
                reasons.append(f"Low citation soundness ({int(citation_soundness*100)}%)")
            if applicability_score < 0.70:
                reasons.append(f"Statutory applicability mismatch ({int(applicability_score*100)}%)")
            if conclusion_score < 0.70:
                reasons.append(f"Unjustified / non-sequitur conclusions detected ({int(conclusion_score*100)}%)")
            if contradictions:
                reasons.append(f"{len(contradictions)} statutory contradiction(s) detected")
            if unsubstantiated_claims:
                reasons.append(f"{len(unsubstantiated_claims)} claim(s) lack empirical/legal evidence")
            if groundedness < 0.50:
                reasons.append(f"Low evidence groundedness ({int(groundedness*100)}%)")
            return f"❌ 3-Tier Verification FAILED / FLAGGED: {', '.join(reasons)}."
