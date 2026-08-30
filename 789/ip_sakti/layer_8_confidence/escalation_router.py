"""
Escalation Router
Determines whether human specialist escalation is mandatory and identifies the appropriate domain expert.
"""

from typing import List, Tuple, Optional
from ..core.schema import (
    UpstreamAgentOutput,
    VerificationResult,
    SpecialistRole,
    EscalationTriggerReason,
    ContradictionSeverity,
    AyurvedaCategory,
    Jurisdiction
)


class EscalationRouter:
    """
    Evaluates risk signals and routes queries to designated human legal/regulatory specialists.
    """

    @classmethod
    def evaluate_escalation(
        cls,
        upstream_output: UpstreamAgentOutput,
        verification_result: VerificationResult,
        calculated_confidence: float
    ) -> Tuple[bool, Optional[SpecialistRole], str, List[EscalationTriggerReason]]:
        triggers: List[EscalationTriggerReason] = []

        # Trigger 1: Critical or High Severity Contradictions
        for c in verification_result.contradictions:
            triggers.append(
                EscalationTriggerReason(
                    trigger_code=c.conflict_type,
                    severity=c.severity,
                    explanation=c.description,
                    relevant_statutes=[c.statutory_authority]
                )
            )

        # Trigger 2: Low Confidence Score
        if calculated_confidence < 0.60:
            triggers.append(
                EscalationTriggerReason(
                    trigger_code="LOW_COMPLIANCE_CONFIDENCE",
                    severity=ContradictionSeverity.HIGH,
                    explanation=f"Overall compliance confidence score is low ({int(calculated_confidence*100)}%), requiring manual legal audit.",
                    relevant_statutes=[]
                )
            )

        # Trigger 3: Cross-Border Foreign Filing with Indian Bio-resources
        if upstream_output.target_jurisdiction in [Jurisdiction.US, Jurisdiction.EPO, Jurisdiction.WIPO_PCT, Jurisdiction.MULTI]:
            if len(upstream_output.botanical_and_herbal_ingredients) > 0:
                triggers.append(
                    EscalationTriggerReason(
                        trigger_code="CROSS_BORDER_NBA_ABS_FILING",
                        severity=ContradictionSeverity.MEDIUM,
                        explanation="Foreign patent prosecution on Indian bio-resources entails mandatory National Biodiversity Authority (NBA) approval to avoid penal liability under BDA Section 55.",
                        relevant_statutes=["Biological Diversity Act 2002 - Section 6 & 55"]
                    )
                )

        # Trigger 4: Phytopharmaceutical or New Drug Category
        if upstream_output.detected_category in [AyurvedaCategory.PHYTOPHARMACEUTICAL, AyurvedaCategory.NEW_HERBAL_ENTITY]:
            triggers.append(
                EscalationTriggerReason(
                    trigger_code="PHYTOPHARMACEUTICAL_CLINICAL_TRIAL_REVIEW",
                    severity=ContradictionSeverity.MEDIUM,
                    explanation="Requires protocol approval from CDSCO Subject Expert Committee (SEC) and Phase I/II human trials.",
                    relevant_statutes=["Drugs and Cosmetics Rules 1945 - Rule 2(eb) & Schedule Y/CT Rules"]
                )
            )

        # If no triggers, escalation is not mandatory
        if not triggers:
            return False, None, "NORMAL", []

        # Determine highest urgency
        has_critical = any(t.severity == ContradictionSeverity.CRITICAL for t in triggers)
        has_high = any(t.severity == ContradictionSeverity.HIGH for t in triggers)
        urgency = "IMMEDIATE" if has_critical else ("URGENT" if has_high else "ADVISORY")

        # Determine the most relevant specialist role
        target_role = cls._select_specialist_role(triggers, upstream_output)

        return True, target_role, urgency, triggers

    @classmethod
    def _select_specialist_role(
        cls,
        triggers: List[EscalationTriggerReason],
        upstream_output: UpstreamAgentOutput
    ) -> SpecialistRole:
        trigger_codes = {t.trigger_code for t in triggers}

        if "CROSS_BORDER_NBA_ABS_FILING" in trigger_codes or "BDA_NBA_APPROVAL_OMISSION" in trigger_codes:
            return SpecialistRole.NBA_ABS_COMPLIANCE_EXPERT

        if "SECTION_3P_TK_CONFLICT" in trigger_codes:
            return SpecialistRole.TKDL_PRIOR_ART_SPECIALIST

        if upstream_output.detected_category == AyurvedaCategory.PHYTOPHARMACEUTICAL or "PHYTOPHARMACEUTICAL_CLINICAL_TRIAL_REVIEW" in trigger_codes:
            return SpecialistRole.AYUSH_REGULATORY_CONSULTANT

        if any("PATENT" in code or "3D" in code for code in trigger_codes):
            return SpecialistRole.PATENT_ATTORNEY_LIFE_SCIENCES

        return SpecialistRole.SENIOR_IP_COUNSEL
