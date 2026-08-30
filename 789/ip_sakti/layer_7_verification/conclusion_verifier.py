"""
Tier 3: Legal Conclusion & Justification Verifier
Evaluates: 'Does this law actually justify the conclusion the AI reached?'
Checks whether the legal conclusion logically and statutorily follows from the cited statutes.
"""

from typing import List, Tuple
from ..core.schema import (
    UpstreamAgentOutput,
    ConclusionValidationFinding,
    ApplicabilityFinding
)


class ConclusionVerifier:
    """
    Tier 3 Verification Engine:
    Validates the logical and statutory bridge between the applicable law and the final AI conclusion.
    """

    @classmethod
    def verify_conclusions(
        cls,
        upstream_output: UpstreamAgentOutput,
        applicability_findings: List[ApplicabilityFinding]
    ) -> Tuple[List[ConclusionValidationFinding], float]:
        findings: List[ConclusionValidationFinding] = []

        norm_claim = (upstream_output.proposed_use_or_claim or "").lower()
        norm_synthesis = (upstream_output.synthesis_draft_text or "").lower()
        full_text = f"{norm_claim} {norm_synthesis} {upstream_output.product_name.lower()}"

        applicable_codes = {f.statute_code for f in applicability_findings if f.is_applicable}

        # Check 1: Classical Formulation Patentability Conclusion
        if "PAT-SEC-3P" in applicable_codes:
            claims_patentable_without_synergy = (
                any(w in full_text for w in [
                    "patentable as novel", "grant patent", "novel ayurvedic composition",
                    "file patent immediately", "immediately file a product patent", "file a product patent",
                    "file a patent", "patent this new formula", "directly patentable", "completely novel"
                ]) and
                not any(w in full_text for w in ["synergy", "synergistic", "combination index", "surpass traditional", "novel extraction matrix", "statutory bar"])
            )
            acknowledges_section_3p_bar = (
                any(w in full_text for w in ["section 3(p)", "traditional knowledge bar", "cannot patent", "mere aggregation", "synergy required", "form 25d"])
            )

            if claims_patentable_without_synergy and not acknowledges_section_3p_bar:
                findings.append(ConclusionValidationFinding(
                    conclusion_statement="AI concludes that classical herbal formulation is directly patentable as a novel composition.",
                    statutory_basis="Patents Act 1970 - Section 3(p)",
                    is_justified=False,
                    logical_status="STATUTORY_BAR_CONTRADICTION",
                    legal_analysis="Section 3(p) bars patenting of traditional knowledge and mere aggregations. Citing patent law does not justify granting a patent on classical formulations without empirical synergistic data.",
                    correct_statutory_verdict="Non-patentable under Section 3(p) unless quantifiable synergistic therapeutic efficacy over individual classical ingredients is proven."
                ))
            else:
                findings.append(ConclusionValidationFinding(
                    conclusion_statement="AI correctly analyzes Section 3(p) Traditional Knowledge bar and identifies that classical formulation requires synergy proof or classical licensing.",
                    statutory_basis="Patents Act 1970 - Section 3(p)",
                    is_justified=True,
                    logical_status="VALID_JUSTIFIED_DEDUCTION",
                    legal_analysis="Conclusion is legally sound. Classical formulations require proof of synergistic interaction or should pursue Rule 158B classical licensing.",
                    correct_statutory_verdict="Legally justified: Section 3(p) restriction correctly applied."
                ))

        # Check 2: Foreign Patent Filing without NBA Clearance Conclusion
        if "BDA-SEC-6-1" in applicable_codes:
            omits_nba_clearance = (
                any(w in full_text for w in ["file pct", "file in uspto", "file in epo", "us patent", "no biodiversity", "no nba or sbb", "no nba"]) and
                any(w in full_text for w in ["no approval needed", "file immediately", "nba exempt", "skip nba", "no nba or sbb filings are needed", "no biodiversity board"])
            )
            requires_nba_approval = (
                any(w in full_text for w in ["form iii", "nba approval", "national biodiversity authority", "section 6(1)", "bda clearance"])
            )

            if omits_nba_clearance and not requires_nba_approval:
                findings.append(ConclusionValidationFinding(
                    conclusion_statement="AI suggests foreign patent prosecution or commercialization can proceed without National Biodiversity Authority (NBA) approval.",
                    statutory_basis="Biological Diversity Act 2002 - Section 6(1)",
                    is_justified=False,
                    logical_status="UNAUTHORIZED_EXEMPTION",
                    legal_analysis="Section 6(1) explicitly prohibits applying for foreign IPR or commercializing on Indian biological resources without prior approval from NBA.",
                    correct_statutory_verdict="Form III application to NBA is mandatory prior to patent grant/filing under Section 6(1) to avoid penal liability under Section 55."
                ))
            else:
                findings.append(ConclusionValidationFinding(
                    conclusion_statement="AI correctly identifies that prior NBA Form III approval is a mandatory pre-condition before filing or granting foreign IPR.",
                    statutory_basis="Biological Diversity Act 2002 - Section 6(1)",
                    is_justified=True,
                    logical_status="VALID_JUSTIFIED_DEDUCTION",
                    legal_analysis="Conclusion is statutorily justified. Section 6(1) mandates prior approval for Indian bio-resources.",
                    correct_statutory_verdict="Legally justified: Mandatory NBA Form III compliance recognized."
                ))

        # Check 3: Rule 158B ASU Classical Licensing Exemption from Clinical Trials
        if "DCR-RULE-158B" in applicable_codes:
            if any(w in full_text for w in ["rule 158b(i)(a)", "classical", "form 25d", "authoritative text", "first schedule"]):
                findings.append(ConclusionValidationFinding(
                    conclusion_statement="AI concludes that classical Ayurvedic formulations listed in First Schedule authoritative texts are exempt from clinical trials for Form 25D licensing.",
                    statutory_basis="Drugs & Cosmetics Rules 1945 - Rule 158B(I)(A)",
                    is_justified=True,
                    logical_status="VALID_JUSTIFIED_DEDUCTION",
                    legal_analysis="Conclusion is legally justified. Rule 158B(I)(A) explicitly establishes textual reference from First Schedule books as sufficient proof of safety and efficacy.",
                    correct_statutory_verdict="Legally justified: Textual evidence from First Schedule satisfies Rule 158B(I)(A) licensing."
                ))

        # Check 4: Section 3(d) Enhanced Efficacy Conclusion
        if "PAT-SEC-3D" in applicable_codes:
            claims_patentable_without_efficacy = (
                any(w in full_text for w in ["extract is novel", "fraction patentable"]) and
                not any(w in full_text for w in ["enhanced efficacy", "efficacy data", "section 3(d)", "bioavailability", "pharmacokinetic"])
            )
            if claims_patentable_without_efficacy:
                findings.append(ConclusionValidationFinding(
                    conclusion_statement="AI concludes that herbal extract/fraction is patentable without demonstrating enhanced therapeutic efficacy.",
                    statutory_basis="Patents Act 1970 - Section 3(d)",
                    is_justified=False,
                    logical_status="STATUTORY_BAR_CONTRADICTION",
                    legal_analysis="Section 3(d) requires new forms or derivatives of known substances to prove significantly enhanced therapeutic efficacy over the baseline.",
                    correct_statutory_verdict="Enhanced therapeutic efficacy data is mandatory under Section 3(d)."
                ))
            else:
                findings.append(ConclusionValidationFinding(
                    conclusion_statement="AI correctly notes that Section 3(d) mandates comparative in-vivo/clinical efficacy enhancement data for novel fractions.",
                    statutory_basis="Patents Act 1970 - Section 3(d)",
                    is_justified=True,
                    logical_status="VALID_JUSTIFIED_DEDUCTION",
                    legal_analysis="Conclusion is statutorily justified. Section 3(d) evidentiary standard correctly cited.",
                    correct_statutory_verdict="Legally justified: Section 3(d) enhanced efficacy standard applied."
                ))

        # Calculate conclusion justification score
        if not findings:
            return [], 1.0

        justified_count = sum(1 for f in findings if f.is_justified)
        score = round(justified_count / len(findings), 2)

        return findings, score
