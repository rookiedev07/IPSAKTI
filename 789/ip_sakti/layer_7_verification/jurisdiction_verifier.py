"""
Jurisdiction Coherence Verifier
Ensures statutes, regulatory pathways, and claims strictly align with the target jurisdiction(s).
"""

from typing import List, Tuple
from ..core.schema import Claim, Jurisdiction, UpstreamAgentOutput


class JurisdictionVerifier:
    """
    Verifies that claims do not conflate domestic and international legal frameworks.
    """

    @classmethod
    def verify_jurisdiction_coherence(cls, upstream_output: UpstreamAgentOutput) -> Tuple[float, List[str]]:
        target_jur = upstream_output.target_jurisdiction
        issues: List[str] = []
        text = upstream_output.synthesis_draft_text.lower()

        total_claims = len(upstream_output.extracted_claims)
        if total_claims == 0:
            return 1.0, []

        misaligned_claims = 0

        for claim in upstream_output.extracted_claims:
            stmt = claim.statement.lower()

            # Rule 1: India-only jurisdiction should not cite US/EPO specific statutory standards as Indian law
            if target_jur == Jurisdiction.INDIA:
                if "35 u.s.c" in stmt or "uspto" in stmt:
                    if "foreign" not in stmt and "export" not in stmt:
                        misaligned_claims += 1
                        issues.append(f"Claim '{claim.claim_id}' cites US law (35 U.S.C.) in an India-focused inquiry without clear context.")
            
            # Rule 2: US/EPO/International jurisdiction using Indian bio-resources MUST cite BDA Sec 6(1)
            if target_jur in [Jurisdiction.US, Jurisdiction.EPO, Jurisdiction.WIPO_PCT, Jurisdiction.MULTI]:
                if len(upstream_output.botanical_and_herbal_ingredients) > 0:
                    if "nba" not in text and "biodiversity" not in text and "section 6" not in text:
                        issues.append("International patent filing utilizing Indian biological materials omits mandatory NBA Section 6(1) approval.")
                        misaligned_claims += 1

        coherence_score = max(0.0, round(1.0 - (misaligned_claims / max(1, total_claims)), 2))
        return coherence_score, issues
