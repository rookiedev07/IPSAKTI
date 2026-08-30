"""
Escalation Dossier Generator
Generates a structured human-in-the-loop legal and regulatory briefing package.
"""

from typing import List, Optional
from ..core.schema import (
    UpstreamAgentOutput,
    VerificationResult,
    SpecialistRole,
    EscalationTriggerReason,
    EscalationDossier
)


class EscalationDossierGenerator:
    """
    Assembles a comprehensive case dossier for human IP Attorneys, AYUSH Regulators, and NBA Officers.
    """

    @classmethod
    def generate_dossier(
        cls,
        upstream_output: UpstreamAgentOutput,
        verification_result: VerificationResult,
        is_required: bool,
        target_specialist: Optional[SpecialistRole],
        urgency: str,
        triggers: List[EscalationTriggerReason]
    ) -> EscalationDossier:
        if not is_required:
            return EscalationDossier(
                is_escalation_required=False,
                target_specialist=None,
                urgency_level="NONE",
                risk_summary="Standard statutory compliance. No immediate human escalation triggered.",
                triggers=[],
                brief_for_expert="",
                recommended_questions_for_counsel=[],
                human_in_the_loop_flags=[]
            )

        # Build risk summary
        trigger_bullets = "\n".join([f"• [{t.severity.value}] {t.trigger_code}: {t.explanation}" for t in triggers])
        risk_summary = f"Query requires human oversight due to {len(triggers)} detected risk factors:\n{trigger_bullets}"

        # Build expert briefing
        brief = (
            f"=== IP-SAKTI HUMAN ESCALATION BRIEF ===\n"
            f"CASE ID: {upstream_output.query_id}\n"
            f"PRODUCT: {upstream_output.product_name} ({upstream_output.detected_category.value})\n"
            f"TARGET JURISDICTION: {upstream_output.target_jurisdiction.value}\n"
            f"DESIGNATED SPECIALIST: {target_specialist.value if target_specialist else 'Senior Legal Counsel'}\n"
            f"URGENCY: {urgency}\n\n"
            f"CORE INGREDIENTS:\n"
            f"{', '.join(upstream_output.botanical_and_herbal_ingredients) if upstream_output.botanical_and_herbal_ingredients else 'None specified'}\n\n"
            f"PROPOSED CLAIM:\n"
            f"{upstream_output.proposed_use_or_claim}\n\n"
            f"VERIFICATION STATUS:\n"
            f"• Groundedness: {int(verification_result.overall_groundedness_score*100)}%\n"
            f"• Citation Soundness: {int(verification_result.citation_soundness_score*100)}%\n"
            f"• Contradictions Detected: {len(verification_result.contradictions)}\n"
        )

        # Questions for legal counsel
        questions = cls._formulate_counsel_questions(upstream_output, triggers)

        # Human in the loop flags
        flags = [f"FLAG-{idx+1:02d}: {t.trigger_code} ({t.severity.value})" for idx, t in enumerate(triggers)]

        return EscalationDossier(
            is_escalation_required=True,
            target_specialist=target_specialist,
            urgency_level=urgency,
            risk_summary=risk_summary,
            triggers=triggers,
            brief_for_expert=brief,
            recommended_questions_for_counsel=questions,
            human_in_the_loop_flags=flags
        )

    @staticmethod
    def _formulate_counsel_questions(
        upstream_output: UpstreamAgentOutput,
        triggers: List[EscalationTriggerReason]
    ) -> List[str]:
        questions = []
        trigger_codes = {t.trigger_code for t in triggers}
        
        herbs = upstream_output.botanical_and_herbal_ingredients
        herb_str = " & ".join(herbs[:2]) if herbs else (upstream_output.product_name or "the active botanical formulation")
        jurisdiction = upstream_output.target_jurisdiction.value if upstream_output.target_jurisdiction else "India"
        category = upstream_output.detected_category.value if upstream_output.detected_category else "AYURVEDIC_FORMULATION"
        claim_text = (upstream_output.proposed_use_or_claim or "").lower()

        # 1. Section 3(p) / Traditional Knowledge Conflict
        if "SECTION_3P_TK_CONFLICT" in trigger_codes or "TRADITIONAL_KNOWLEDGE_PRIOR_ART" in trigger_codes:
            questions.append(
                f"Can we furnish quantifiable synergy data (Combination Index CI < 1.0 or comparative therapeutic bioassays) for {herb_str} to overcome the Section 3(p) Traditional Knowledge bar?"
            )
            questions.append(
                f"Would pursuing a classical manufacturing license under Rule 158B(I)(A) coupled with proprietary trademark/trade-dress registration offer a lower-risk commercial pathway for {herb_str}?"
            )

        # 2. Section 3(d) / Section 3(e) Patent Ineligibility
        if "PATENT_INELIGIBLE_COMBINATION_3E" in trigger_codes or "SECTION_3D_EFFICACY_DEFICIT" in trigger_codes or "novelty" in claim_text or "patent" in claim_text:
            if not any("Section 3(d)" in q for q in questions):
                questions.append(
                    f"Has comparative in-vivo or clinical bioequivalence data been documented to substantiate enhanced therapeutic efficacy under Section 3(d) of the Patents Act for {herb_str}?"
                )

        # 3. NBA / Biodiversity Access & Benefit Sharing
        if "CROSS_BORDER_NBA_ABS_FILING" in trigger_codes or "BDA_NBA_APPROVAL_OMISSION" in trigger_codes:
            questions.append(
                f"Has Form III been prepared for submission to the National Biodiversity Authority (NBA) under Section 6(1) prior to foreign filing in {jurisdiction}?"
            )
            questions.append(
                f"Have State Biodiversity Board (SBB) intimations under Section 7 and Access and Benefit Sharing (ABS) revenue levies (0.1%–0.5%) been factored for procurement of {herb_str}?"
            )

        # 4. Phytopharmaceutical Clinical Trials / CDSCO Review
        if "PHYTOPHARMACEUTICAL_CLINICAL_TRIAL_REVIEW" in trigger_codes or category == "PHYTOPHARMACEUTICAL":
            questions.append(
                f"What specific safety, toxicology, and chromatographic fingerprinting data (at least 4 bioactive markers) are required by the CDSCO Subject Expert Committee (SEC) for {herb_str} under Rule 2(eb)?"
            )

        # 5. Low Compliance Confidence / Ambiguity
        if "LOW_COMPLIANCE_CONFIDENCE" in trigger_codes:
            questions.append(
                f"Please conduct an exhaustive statutory audit of the proposed {category} claims for {herb_str} against the latest Gazette notifications and Indian patent guidelines."
            )

        # 6. Fallback
        if not questions:
            questions.append(
                f"Please verify the statutory compatibility of the proposed claims for {herb_str} with the latest Gazette notifications, Rule 158B requirements, and Indian patent guidelines."
            )
            questions.append(
                f"Have all mandatory provenance records and NBA clearance requirements under the Biological Diversity Act been audited for {herb_str}?"
            )

        return questions[:4]
