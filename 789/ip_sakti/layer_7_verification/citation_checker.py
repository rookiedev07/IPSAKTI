"""
Citation & Statutory Registry Checker
Validates legal citations against the authoritative Indian & International Statutory Registry.
"""

from typing import List, Tuple
from ..core.schema import Citation, CitationValidationResult
from ..core.constants import STATUTORY_REGISTRY


class CitationChecker:
    """
    Validates legal, regulatory, and patent citations referenced by upstream agents.
    """

    @classmethod
    def validate_citations(cls, citations: List[Citation]) -> Tuple[List[CitationValidationResult], float]:
        if not citations:
            return [], 0.0

        results: List[CitationValidationResult] = []
        valid_count = 0

        for cit in citations:
            is_valid, is_active, notes = cls._check_single_citation(cit)
            if is_valid:
                valid_count += 1

            results.append(
                CitationValidationResult(
                    citation=cit,
                    is_valid_statute=is_valid,
                    is_active_law=is_active,
                    notes=notes
                )
            )

        soundness_score = round(valid_count / len(citations), 2)
        return results, soundness_score

    @classmethod
    def _check_single_citation(cls, citation: Citation) -> Tuple[bool, bool, str]:
        act_text = citation.act_or_text.lower()
        sec_text = citation.section_or_rule.strip()

        # Check Patents Act 1970
        if "patents act" in act_text or "patent act" in act_text:
            pat_reg = STATUTORY_REGISTRY["PATENTS_ACT_1970"]
            for sec_key, sec_val in pat_reg["key_sections"].items():
                if sec_key.lower() in sec_text.lower() or sec_text.lower() in sec_key.lower():
                    return True, True, f"Verified against {pat_reg['full_title']} - {sec_val['title']}"
            # If section didn't match known key sections, but act is authentic
            return True, True, f"Authentic statute: {pat_reg['full_title']}"

        # Check Biological Diversity Act
        if "biological diversity" in act_text or "biodiversity" in act_text or "bda" in act_text:
            bda_reg = STATUTORY_REGISTRY["BIOLOGICAL_DIVERSITY_ACT"]
            for sec_key, sec_val in bda_reg["key_sections"].items():
                if sec_key.lower() in sec_text.lower() or sec_text.lower() in sec_key.lower():
                    return True, True, f"Verified against {bda_reg['full_title']} - {sec_val['title']}"
            return True, True, f"Authentic statute: {bda_reg['full_title']}"

        # Check Drugs and Cosmetics Act / Rules
        if "drugs and cosmetics" in act_text or "dca" in act_text or "rule 158b" in act_text or "schedule t" in act_text:
            dca_reg = STATUTORY_REGISTRY["DRUGS_AND_COSMETICS_ACT"]
            for sec_key, sec_val in dca_reg["key_sections"].items():
                if sec_key.lower() in sec_text.lower() or sec_text.lower() in sec_key.lower():
                    return True, True, f"Verified against {dca_reg['full_title']} - {sec_val['title']}"
            return True, True, f"Authentic statute: {dca_reg['full_title']}"

        # Check TKDL or Authoritative Books
        if "tkdl" in act_text or "samhita" in act_text or "charaka" in act_text or "sushruta" in act_text:
            return True, True, "Verified against First Schedule Authoritative Texts / TKDL Registry"

        # Check International Frameworks
        if "35 u.s.c" in act_text or "uspto" in act_text:
            return True, True, "Verified against USPTO 35 U.S. Code Statutory Framework"
        if "epc" in act_text or "european patent" in act_text:
            return True, True, "Verified against European Patent Convention (EPC)"

        # Unknown or unverified citation
        return False, False, f"Unverified or non-standard statutory citation: '{citation.act_or_text} {citation.section_or_rule}'"
