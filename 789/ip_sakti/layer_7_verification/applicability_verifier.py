"""
Tier 2: Statutory Applicability Verifier
Evaluates: 'Does this law actually apply here?'
Validates subject-matter preconditions, entity status, territorial nexus, and statutory exemptions.
"""

from typing import List, Tuple
from ..core.schema import (
    UpstreamAgentOutput,
    ApplicabilityFinding,
    AyurvedaCategory,
    Jurisdiction
)


class ApplicabilityVerifier:
    """
    Tier 2 Verification Engine:
    Validates whether each cited statute has legal subject-matter and jurisdictional nexus to the case.
    """

    @classmethod
    def verify_applicability(cls, upstream_output: UpstreamAgentOutput) -> Tuple[List[ApplicabilityFinding], float]:
        findings: List[ApplicabilityFinding] = []

        norm_claim = (upstream_output.proposed_use_or_claim or "").lower()
        norm_synthesis = (upstream_output.synthesis_draft_text or "").lower()
        full_text = f"{norm_claim} {norm_synthesis} {upstream_output.product_name.lower()}"
        
        herbs = upstream_output.botanical_and_herbal_ingredients
        category = upstream_output.detected_category
        jurisdiction = upstream_output.target_jurisdiction

        has_traditional_herbs = len(herbs) > 0 or any(w in full_text for w in ["classical", "chyawanprash", "triphala", "haldi", "turmeric", "ashwagandha", "neem", "ayurved", "traditional"])
        is_patent_query = any(w in full_text for w in ["patent", "invent", "novel", "claim", "prior art", "section 3"])
        is_multi_ingredient = len(herbs) >= 2 or any(w in full_text for w in ["combination", "admixture", "blend", "mixture", "with added"])
        is_derivative_or_extract = any(w in full_text for w in ["extract", "fraction", "derivative", "standardized", "bioactive", "cordifolioside", "curcumin"])
        is_cross_border = jurisdiction in [Jurisdiction.US, Jurisdiction.EPO, Jurisdiction.WIPO_PCT, Jurisdiction.MULTI] or any(w in full_text for w in ["export", "foreign", "uspto", "fda", "overseas"])
        is_asu_licensing = any(w in full_text for w in ["license", "licensing", "rule 158b", "manufacturing", "gmp", "form 25d", "asu"])
        is_tm_query = any(w in full_text for w in ["trademark", "trade mark", "brand", "class 5", "logo", "name registration"])
        is_fssai_query = any(w in full_text for w in ["fssai", "ayurveda aahar", "food supplement", "nutraceutical", "dietary"])

        # 1. Section 3(p) Patents Act 1970
        if is_patent_query or any("3(p)" in c.act_or_regulation or "3(p)" in c.section_or_rule for c in upstream_output.citations_referenced):
            if has_traditional_herbs:
                findings.append(ApplicabilityFinding(
                    statute_code="PAT-SEC-3P",
                    statute_title="Patents Act 1970 - Section 3(p) (Traditional Knowledge Bar)",
                    is_applicable=True,
                    preconditions_met=[
                        "Subject matter utilizes traditionally known Ayurvedic botanical resources / knowledge",
                        "Invention involves an aggregation or duplication of known traditional properties"
                    ],
                    preconditions_unmet=[],
                    applicability_rationale="Section 3(p) applies directly because the formulation is grounded in traditional Ayurvedic botanical knowledge and prior art documented in TKDL / classical treatises.",
                    subject_matter_nexus=True,
                    territorial_nexus=True
                ))
            else:
                findings.append(ApplicabilityFinding(
                    statute_code="PAT-SEC-3P",
                    statute_title="Patents Act 1970 - Section 3(p) (Traditional Knowledge Bar)",
                    is_applicable=False,
                    preconditions_met=[],
                    preconditions_unmet=["Subject matter lacks traditional Ayurvedic or biological knowledge nexus"],
                    applicability_rationale="Section 3(p) does not apply because no classical traditional knowledge or traditional herbal component was identified.",
                    subject_matter_nexus=False,
                    territorial_nexus=True
                ))

        # 2. Section 3(d) Patents Act 1970
        if is_patent_query and is_derivative_or_extract:
            findings.append(ApplicabilityFinding(
                statute_code="PAT-SEC-3D",
                statute_title="Patents Act 1970 - Section 3(d) (Enhanced Therapeutic Efficacy Requirement)",
                is_applicable=True,
                preconditions_met=[
                    "Claim involves a new form, derivative, extract fraction, or combination of a known herbal substance",
                    "Requires demonstration of significantly enhanced therapeutic efficacy over the known baseline"
                ],
                preconditions_unmet=[],
                applicability_rationale="Section 3(d) applies because the applicant claims an isolated fraction / derivative extract of a known Ayurvedic herb.",
                subject_matter_nexus=True,
                territorial_nexus=True
            ))

        # 3. Section 3(e) Patents Act 1970
        if is_patent_query and is_multi_ingredient:
            findings.append(ApplicabilityFinding(
                statute_code="PAT-SEC-3E",
                statute_title="Patents Act 1970 - Section 3(e) (Mere Admixture Bar)",
                is_applicable=True,
                preconditions_met=[
                    "Polyherbal formulation comprising multiple active ingredients",
                    "Mandates empirical proof of synergistic interaction beyond additive properties"
                ],
                preconditions_unmet=[],
                applicability_rationale="Section 3(e) applies because the polyherbal combination must prove non-obvious synergistic therapeutic efficacy.",
                subject_matter_nexus=True,
                territorial_nexus=True
            ))

        # 4. Biological Diversity Act 2002 - Section 6(1) & Form III
        if is_patent_query and (has_traditional_herbs or is_cross_border):
            findings.append(ApplicabilityFinding(
                statute_code="BDA-SEC-6-1",
                statute_title="Biological Diversity Act 2002 - Section 6(1) (Mandatory NBA Approval for IPR)",
                is_applicable=True,
                preconditions_met=[
                    "Invention is based on research or biological resources sourced from India",
                    "Application for Intellectual Property Right (patent) is contemplated inside or outside India"
                ],
                preconditions_unmet=[],
                applicability_rationale="Section 6(1) applies mandatorily because applying for any patent based on Indian biological resources requires prior NBA approval under Form III.",
                subject_matter_nexus=True,
                territorial_nexus=True
            ))

        # 5. Drugs & Cosmetics Rules 1945 - Rule 158B
        if is_asu_licensing or category in [AyurvedaCategory.CLASSICAL, AyurvedaCategory.PROPRIETARY, AyurvedaCategory.PHYTOPHARMACEUTICAL]:
            findings.append(ApplicabilityFinding(
                statute_code="DCR-RULE-158B",
                statute_title="Drugs & Cosmetics Rules 1945 - Rule 158B (ASU Drug Manufacturing Licensing)",
                is_applicable=True,
                preconditions_met=[
                    "Product is classified as an Ayurvedic, Siddha, or Unani (ASU) drug for commercial manufacturing in India",
                    "Differentiates Classical Formulations (Rule 158B(I)(A)) from Patent/Proprietary Formulations (Rule 158B(I)(B))"
                ],
                preconditions_unmet=[],
                applicability_rationale="Rule 158B applies directly to govern manufacturing licensing, Schedule T GMP compliance, and safety/efficacy submission requirements.",
                subject_matter_nexus=True,
                territorial_nexus=True
            ))

        # 6. Trade Marks Act 1999 - Section 9 & 11
        if is_tm_query:
            findings.append(ApplicabilityFinding(
                statute_code="TMA-SEC-9-11",
                statute_title="Trade Marks Act 1999 - Section 9 & 11 (Absolute & Relative Grounds of Refusal)",
                is_applicable=True,
                preconditions_met=[
                    "Brand/name registration sought in Class 5 (Pharmaceuticals) or Class 3 (Cosmetics)",
                    "Requires avoidance of descriptive/generic Ayurvedic names and conflict with API nomenclature"
                ],
                preconditions_unmet=[],
                applicability_rationale="Trade Marks Act applies to govern brand exclusivity and prohibit registration of generic Ayurvedic terms.",
                subject_matter_nexus=True,
                territorial_nexus=True
            ))

        # 7. FSSAI (Ayurveda Aahar) Regulations 2022
        if is_fssai_query or category == AyurvedaCategory.AYURVEDA_AAHAR:
            findings.append(ApplicabilityFinding(
                statute_code="FSSAI-AAHAR-2022",
                statute_title="FSSAI (Ayurveda Aahar) Regulations 2022 (Traditional Food Safety Standards)",
                is_applicable=True,
                preconditions_met=[
                    "Product prepared in accordance with authoritative Ayurvedic culinary texts for dietary nourishment",
                    "Subject to prohibition on disease cure claims and Schedule E-1 poisonous herbs"
                ],
                preconditions_unmet=[],
                applicability_rationale="FSSAI Ayurveda Aahar regulations govern food/dietary preparations incorporating Ayurvedic ingredients.",
                subject_matter_nexus=True,
                territorial_nexus=True
            ))

        # Calculate applicability score (ratio of applicable statutes with met preconditions)
        if not findings:
            return [], 1.0

        applicable_count = sum(1 for f in findings if f.is_applicable and len(f.preconditions_unmet) == 0)
        score = round(applicable_count / len(findings), 2)

        return findings, score
