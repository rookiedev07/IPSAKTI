"""
Confidence & Risk Assessment Engine (Layer 8 Main Orchestrator)
Calculates multi-dimensional confidence scores, determines refusal triggers,
and coordinates human expert escalation.
"""

from typing import Tuple
from ..core.schema import (
    UpstreamAgentOutput,
    VerificationResult,
    ConfidenceScore,
    ConfidenceLevel,
    ContradictionSeverity
)
from .refusal_handler import RefusalHandler
from .escalation_router import EscalationRouter
from .escalation_dossier import EscalationDossierGenerator


class ConfidenceEngine:
    """
    Layer 8: Confidence and Human Escalation Engine
    """

    def __init__(self):
        self.refusal_handler = RefusalHandler()
        self.escalation_router = EscalationRouter()
        self.dossier_generator = EscalationDossierGenerator()

    def evaluate_confidence(
        self,
        upstream_output: UpstreamAgentOutput,
        verification_result: VerificationResult
    ) -> ConfidenceScore:
        # Step 1: Calculate component weights
        groundedness = verification_result.overall_groundedness_score
        cit_soundness = verification_result.citation_soundness_score
        jur_coherence = verification_result.jurisdiction_coherence_score

        # Step 2: Compute contradiction penalty
        penalty = 0.0
        for c in verification_result.contradictions:
            if c.severity == ContradictionSeverity.CRITICAL:
                penalty += 0.50
            elif c.severity == ContradictionSeverity.HIGH:
                penalty += 0.25
            elif c.severity == ContradictionSeverity.MEDIUM:
                penalty += 0.10
            elif c.severity == ContradictionSeverity.LOW:
                penalty += 0.05

        penalty = min(1.0, penalty)

        # Step 3: Compute final composite numeric score
        base_score = (
            (0.35 * groundedness) +
            (0.25 * cit_soundness) +
            (0.20 * jur_coherence) +
            (0.20 * (1.0 - penalty))
        )
        final_score = max(0.0, min(1.0, round(base_score - (penalty * 0.3), 2)))

        # Step 4: Check Safe Refusal
        safe_refusal = self.refusal_handler.evaluate_refusal(
            upstream_output=upstream_output,
            verification_result=verification_result
        )

        # Step 5: Assign Confidence Level
        if safe_refusal or penalty >= 0.50 or final_score < 0.35:
            level = ConfidenceLevel.REFUSAL if safe_refusal else ConfidenceLevel.LOW
            is_safe = False
        elif final_score >= 0.80:
            level = ConfidenceLevel.HIGH
            is_safe = True
        elif final_score >= 0.55:
            level = ConfidenceLevel.MEDIUM
            is_safe = True
        else:
            level = ConfidenceLevel.LOW
            is_safe = False

        # Step 6: Route Escalation & Generate Dossier
        is_req, spec_role, urgency, triggers = self.escalation_router.evaluate_escalation(
            upstream_output=upstream_output,
            verification_result=verification_result,
            calculated_confidence=final_score
        )

        dossier = self.dossier_generator.generate_dossier(
            upstream_output=upstream_output,
            verification_result=verification_result,
            is_required=is_req,
            target_specialist=spec_role,
            urgency=urgency,
            triggers=triggers
        )

        # Step 7: Formulate confidence justification
        justification = self._build_justification(
            level=level,
            score=final_score,
            groundedness=groundedness,
            cit_soundness=cit_soundness,
            penalty=penalty,
            is_escalation_required=is_req,
            specialist=spec_role
        )

        return ConfidenceScore(
            overall_confidence=level,
            numeric_score=final_score,
            evidence_groundedness_weight=0.35,
            citation_soundness_weight=0.25,
            jurisdiction_coherence_weight=0.20,
            contradiction_penalty=penalty,
            confidence_justification=justification,
            is_safe_to_render=is_safe,
            safe_refusal_text=safe_refusal,
            escalation_dossier=dossier
        )

    def _build_justification(
        self,
        level: ConfidenceLevel,
        score: float,
        groundedness: float,
        cit_soundness: float,
        penalty: float,
        is_escalation_required: bool,
        specialist: any
    ) -> str:
        score_pct = int(score * 100)
        if level == ConfidenceLevel.HIGH:
            return (
                f"HIGH CONFIDENCE ({score_pct}%): Strong statutory grounding ({int(groundedness*100)}%), "
                f"verified citations ({int(cit_soundness*100)}%), and zero statutory contradictions. "
                "Advisory adheres strictly to Indian and international IP precedents."
            )
        elif level == ConfidenceLevel.MEDIUM:
            escalation_str = f" Advisory escalation to {specialist.value} is recommended." if is_escalation_required and specialist else ""
            return (
                f"MEDIUM CONFIDENCE ({score_pct}%): Grounded in core statutes with minor regulatory ambiguities or "
                f"novel proprietary extraction parameters.{escalation_str}"
            )
        elif level == ConfidenceLevel.LOW:
            return (
                f"LOW CONFIDENCE ({score_pct}%): High legal ambiguity or missing statutory clearances. "
                "Mandatory human review by a qualified Registered Patent Agent or AYUSH consultant required."
            )
        else:
            return (
                f"REFUSAL / ZERO CONFIDENCE ({score_pct}%): Critical statutory contradiction detected (Penalty: {int(penalty*100)}%). "
                "Direct automated generation halted to prevent unlawful compliance violations."
            )
