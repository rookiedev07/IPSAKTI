"""
Contradiction & Statutory Conflict Detection Engine
Identifies irreconcilable legal, regulatory, and patent contradictions in agent outputs.
"""

from typing import List
from ..core.schema import (
    UpstreamAgentOutput,
    ContradictionFinding,
    ContradictionSeverity,
    AyurvedaCategory,
    Jurisdiction
)


class ContradictionEngine:
    """
    Scans intermediate synthesis and claims for legal inconsistencies and statutory violations.
    """

    @classmethod
    def detect_contradictions(cls, upstream_output: UpstreamAgentOutput) -> List[ContradictionFinding]:
        findings: List[ContradictionFinding] = []
        text_lower = (upstream_output.synthesis_draft_text + " " + " ".join([c.statement for c in upstream_output.extracted_claims])).lower()

        # Check 1: Classical Formulation vs Section 3(p) Patentability
        if upstream_output.detected_category == AyurvedaCategory.CLASSICAL:
            has_unrestricted_patent_claim = (
                ("can immediately file a product patent" in text_lower or "is directly patentable" in text_lower or "patentable as an entirely new" in text_lower) and
                ("3(p)" not in text_lower and "traditional knowledge" not in text_lower)
            )
            if has_unrestricted_patent_claim:
                findings.append(
                    ContradictionFinding(
                        finding_id="CONTRA-SEC-3P-001",
                        severity=ContradictionSeverity.CRITICAL,
                        conflict_type="SECTION_3P_TK_CONFLICT",
                        description=(
                            f"Product '{upstream_output.product_name}' is classified as Classical Ayurvedic Medicine, "
                            "yet the draft claims unrestricted product patentability in India without Section 3(p) disclaimer. "
                            "Under Section 3(p) of the Patents Act 1970, traditional Ayurvedic formulations are non-patentable."
                        ),
                        statutory_authority="The Patents Act, 1970 - Section 3(p) & TKDL Guidelines",
                        remedial_action="Disclaim direct product patentability; advise brand/trademark protection or focus on novel synergistic extracts/delivery systems."
                    )
                )

        # Check 2: Biological Resources vs NBA / SBB Approval Omission
        has_bio_resources = len(upstream_output.botanical_and_herbal_ingredients) > 0
        claims_no_nba_needed = (
            "no biodiversity" in text_lower or
            "no nba" in text_lower or
            "no permissions needed for commercializing" in text_lower or
            "no sbb" in text_lower
        )
        if has_bio_resources and claims_no_nba_needed:
            findings.append(
                ContradictionFinding(
                    finding_id="CONTRA-BDA-NBA-002",
                    severity=ContradictionSeverity.CRITICAL,
                    conflict_type="BDA_NBA_APPROVAL_OMISSION",
                    description=(
                        "Draft states no NBA/SBB permission is required, which violates Section 6(1) and Section 7 "
                        "of the Biological Diversity Act, 2002 for commercial utilization or IP filings utilizing Indian biological material."
                    ),
                    statutory_authority="Biological Diversity Act, 2002 - Section 6(1), Section 7 & Section 55 (Penal Provisions)",
                    remedial_action="Explicitly mandate Form III application to NBA for IP filing or Form I intimation to State Biodiversity Board."
                )
            )

        # Check 3: Unregulated Commercialization / Licensing Bypass
        claims_no_license = "direct marketing can start without ayush" in text_lower or "sell without licenses" in text_lower
        if claims_no_license:
            findings.append(
                ContradictionFinding(
                    finding_id="CONTRA-DCA-NO-LIC-003",
                    severity=ContradictionSeverity.CRITICAL,
                    conflict_type="UNLICENSED_DRUG_MANUFACTURE",
                    description=(
                        "Draft suggests manufacturing/selling without AYUSH or regulatory license. Under Section 33D of the "
                        "Drugs & Cosmetics Act 1940, manufacturing for sale without an AYUSH license is a cognizable offence."
                    ),
                    statutory_authority="Drugs and Cosmetics Act, 1940 - Chapter IV-A, Section 33D & Rule 158B",
                    remedial_action="Require Form 25D manufacturing license or FSSAI Ayurveda-Aahar license."
                )
            )

        # Check 4: Phytopharmaceutical Clinical Trial Misalignment
        if upstream_output.detected_category == AyurvedaCategory.PHYTOPHARMACEUTICAL:
            if "clinical trial" not in text_lower and "cdsco" not in text_lower:
                findings.append(
                    ContradictionFinding(
                        finding_id="CONTRA-PHYTO-CT-004",
                        severity=ContradictionSeverity.HIGH,
                        conflict_type="PHYTOPHARMACEUTICAL_REGULATORY_GAP",
                        description="Phytopharmaceutical category requires CDSCO Phase I/II/III clinical trials under Rule 2(eb), but no clinical development pathway was specified.",
                        statutory_authority="Drugs & Cosmetics Rules - GSR 918(E) / Rule 2(eb)",
                        remedial_action="Incorporate clinical study protocol and phytochemical standardization benchmarks (minimum 4 bioactive markers)."
                    )
                )

        return findings
