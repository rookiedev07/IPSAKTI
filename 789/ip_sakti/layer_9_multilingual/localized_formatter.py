"""
Localized Response Formatter (Layer 9 Main Orchestrator)
Assembles the complete verified, confidence-scored, multilingual response
ready for delivery to the end user.
"""

from typing import Dict, Any, Optional
from ..core.schema import (
    UpstreamAgentOutput,
    VerificationResult,
    ConfidenceScore,
    MultilingualResponse,
    LanguageCode
)
from ..core.constants import STATUTORY_DISCLAIMERS
from .language_detector import LanguageDetector
from .terminology_preserver import TerminologyPreserver
from .translator import DomainTranslator


class LocalizedFormatter:
    """
    Layer 9: Multilingual Response Formatter
    """

    def __init__(self):
        self.detector = LanguageDetector()
        self.preserver = TerminologyPreserver()
        self.translator = DomainTranslator()

    def format_response(
        self,
        upstream_output: UpstreamAgentOutput,
        verification_result: VerificationResult,
        confidence_score: ConfidenceScore,
        forced_language: Optional[LanguageCode] = None
    ) -> MultilingualResponse:
        # Step 1: Detect or select language
        detected_input_lang = self.detector.detect_language(upstream_output.raw_user_query)
        target_lang = forced_language or detected_input_lang

        # Step 2: Extract Badges in target language
        cat_badge = self.translator.get_category_badge(upstream_output.detected_category, target_lang)
        conf_badge = self.translator.get_confidence_badge(confidence_score.overall_confidence, target_lang)
        score_percent = int(confidence_score.numeric_score * 100)

        # Step 3: Localize Title, Legal Analysis, and Action Steps
        title, detailed_analysis, action_steps = self.translator.translate_analysis(
            text=verification_result.sanitized_synthesis_text,
            lang=target_lang,
            category=upstream_output.detected_category,
            product_name=upstream_output.product_name
        )

        # Step 4: Format Verified Citations
        verified_citations = []
        for cv in verification_result.citation_validations:
            verified_citations.append({
                "citation_id": cv.citation.citation_id,
                "act": cv.citation.act_or_text,
                "section_or_rule": cv.citation.section_or_rule,
                "jurisdiction": cv.citation.jurisdiction.value,
                "summary": cv.citation.summary_of_statute,
                "status": "VALID & ACTIVE STATUTE" if cv.is_valid_statute else "UNVERIFIED"
            })

        # Step 5: Format Escalation Notice if required
        escalation_notice = None
        if confidence_score.escalation_dossier.is_escalation_required:
            dossier = confidence_score.escalation_dossier
            escalation_notice = {
                "specialist_role": dossier.target_specialist.value if dossier.target_specialist else "Senior Legal Counsel",
                "urgency": dossier.urgency_level,
                "risk_summary": dossier.risk_summary,
                "expert_brief": dossier.brief_for_expert,
                "questions_for_counsel": dossier.recommended_questions_for_counsel,
                "flags": dossier.human_in_the_loop_flags
            }

        # Step 6: Generate Bilingual Domain Glossary
        glossary = self.preserver.get_bilingual_glossary_for_output(
            category=upstream_output.detected_category,
            text_content=verification_result.sanitized_synthesis_text,
            target_lang=target_lang
        )

        # Step 7: Localized Disclaimer
        disclaimer = STATUTORY_DISCLAIMERS.get(target_lang, STATUTORY_DISCLAIMERS[LanguageCode.EN])

        # Step 8: Verification Audit Trail
        audit_trail = {
            "query_id": upstream_output.query_id,
            "verification_passed": verification_result.is_passed,
            "groundedness_score": verification_result.overall_groundedness_score,
            "citation_soundness_score": verification_result.citation_soundness_score,
            "jurisdiction_coherence_score": verification_result.jurisdiction_coherence_score,
            "contradictions_count": len(verification_result.contradictions),
            "unsubstantiated_claims_count": len(verification_result.unsubstantiated_claims),
            "confidence_level": confidence_score.overall_confidence.value,
            "numeric_confidence": confidence_score.numeric_score,
            "confidence_justification": confidence_score.confidence_justification
        }

        # Step 9: Build Executive Summary
        if target_lang == LanguageCode.HI:
            exec_summary = (
                f"{upstream_output.product_name} का मूल्यांकन '{cat_badge}' के अंतर्गत संपन्न हुआ। "
                f"वैधानिक विश्वास स्तर: {conf_badge} ({score_percent}%)। "
                f"{len(verified_citations)} प्रामाणिक कानूनी स्रोतों द्वारा सत्यापित।"
            )
        elif target_lang == LanguageCode.MR:
            exec_summary = (
                f"{upstream_output.product_name} ची पडताळणी '{cat_badge}' अंतर्गत पूर्ण झाली. "
                f"कायदेशीर विश्वास पातळी: {conf_badge} ({score_percent}%). "
                f"{len(verified_citations)} अधिकृत वैधानिक संदर्भांद्वारे प्रमाणित."
            )
        else:
            exec_summary = (
                f"Compliance analysis completed for {upstream_output.product_name} classified as '{cat_badge}'. "
                f"Statutory Confidence: {conf_badge} ({score_percent}%). "
                f"Corroborated by {len(verified_citations)} authoritative statutory citation(s)."
            )

        return MultilingualResponse(
            query_id=upstream_output.query_id,
            target_language=target_lang,
            detected_input_language=detected_input_lang,
            title=title,
            product_classification_badge=cat_badge,
            confidence_level_badge=conf_badge,
            confidence_score_percent=score_percent,
            executive_summary=exec_summary,
            detailed_legal_analysis=detailed_analysis,
            key_actionable_steps=action_steps,
            verified_statutory_citations=verified_citations,
            escalation_notice=escalation_notice,
            safe_refusal_notice=confidence_score.safe_refusal_text,
            bilingual_glossary=glossary,
            statutory_disclaimer=disclaimer,
            verification_audit_trail=audit_trail
        )
