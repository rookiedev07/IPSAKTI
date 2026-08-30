"""
Safe Refusal & Abstention Handler
Formulates structured, legally precise refusals and safe abstentions
when advice cannot be responsibly generated without human/statutory clearance.
"""

from typing import Optional, List
from ..core.schema import (
    UpstreamAgentOutput,
    VerificationResult,
    ContradictionSeverity
)


class RefusalHandler:
    """
    Constructs compliant safe refusal statements when evidence is deficient
    or proposed actions breach statutory prohibitions.
    """

    @classmethod
    def evaluate_refusal(
        cls,
        upstream_output: UpstreamAgentOutput,
        verification_result: VerificationResult
    ) -> Optional[str]:
        # Check 1: Critical statutory contradictions
        critical_contras = [c for c in verification_result.contradictions if c.severity == ContradictionSeverity.CRITICAL]
        if critical_contras:
            refusal_points = []
            for c in critical_contras:
                refusal_points.append(f"• {c.description} (Authority: {c.statutory_authority})")

            return (
                "🛑 SAFE STATUTORY REFUSAL & ABSTENTION:\n"
                "The system cannot endorse or generate affirmative filings for the requested strategy because it conflicts with mandatory Indian statutes:\n\n"
                + "\n".join(refusal_points) + "\n\n"
                "RECOMMENDED SAFE HARBOR:\n"
                "1. Refrain from filing unpatentable traditional knowledge claims to avoid pre-grant opposition under Section 25(1) of the Patents Act.\n"
                "2. Apply for proper AYUSH Form 25D manufacturing licenses or FSSAI Ayurveda-Aahar approvals.\n"
                "3. Consult a qualified Registered Patent Agent and the State Biodiversity Board before commercial distribution."
            )

        # Check 2: Severe lack of evidence (groundedness < 0.25)
        if verification_result.overall_groundedness_score < 0.25 and len(verification_result.unsubstantiated_claims) > 0:
            return (
                "⚠️ CAUTIONARY ABSTENTION (INSUFFICIENT STATUTORY EVIDENCE):\n"
                "The system found insufficient authoritative legal precedents or TKDL evidence to substantiate the proposed formulation strategy. "
                "To prevent hallucinated compliance advice, direct execution is halted. Professional human evaluation is mandatory."
            )

        return None
