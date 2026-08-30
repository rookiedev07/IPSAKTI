"""
Mock Upstream Simulator (Layers 1 to 6)
Simulates outputs from:
- User Problem & Prompt Matcher
- Joker Multi-Agent Router
- Classification Agent
- IP/RAG Agent
- Prior-Art & TKDL Agent
- Jurisdiction & Citation/Evidence Layers
"""

from typing import Dict, List, Optional
from .schema import (
    UpstreamAgentOutput,
    AyurvedaCategory,
    Jurisdiction,
    Claim,
    Citation,
    EvidenceChunk,
    EvidenceSourceType,
)


def get_mock_scenario(scenario_id: str) -> UpstreamAgentOutput:
    """
    Retrieves a pre-configured realistic upstream agent scenario.
    """
    scenarios = {
        "classical_chyawanprash": _build_classical_chyawanprash_scenario(),
        "novel_phytopharmaceutical": _build_novel_phytopharmaceutical_scenario(),
        "unsubstantiated_haldi_patent": _build_unsubstantiated_haldi_scenario(),
        "international_pct_export": _build_international_pct_scenario()
    }
    if scenario_id not in scenarios:
        raise ValueError(f"Unknown scenario_id: {scenario_id}. Available: {list(scenarios.keys())}")
    return scenarios[scenario_id]


def list_mock_scenarios() -> List[Dict[str, str]]:
    return [
        {
            "id": "classical_chyawanprash",
            "name": "Classical Chyawanprash Formulation (Patentability vs Rule 158B)",
            "description": "User wants to patent and license standard Chyawanprash formulation. Tests Section 3(p) TKDL bar & Rule 158B classical textual evidence."
        },
        {
            "id": "novel_phytopharmaceutical",
            "name": "Novel Standardized Giloy Phytopharmaceutical Fraction",
            "description": "Purified cordifolioside fraction with synergistic compound for metabolic disorder. Tests patentability, NBA Section 6 ABS approval, and Schedule Y/Rule 158B clinical validation."
        },
        {
            "id": "unsubstantiated_haldi_patent",
            "name": "Hallucinated Turmeric-Pepper Simple Admixture",
            "description": "Claims standard Curcumin + Piperine mixture is completely novel and patentable without NBA clearance. Tests hallucination guard, critical contradiction detection, and safe refusal."
        },
        {
            "id": "international_pct_export",
            "name": "International Patent & Export Formulation (India -> US/EPO)",
            "description": "Proprietary polyherbal extract filing in USPTO/EPO using Indian biodiversity. Tests multi-jurisdictional compliance and NBA Form III cross-border rules."
        }
    ]


def _build_classical_chyawanprash_scenario() -> UpstreamAgentOutput:
    ev1 = EvidenceChunk(
        id="EV-PAT-3P",
        title="Patents Act 1970 - Section 3(p)",
        source_type=EvidenceSourceType.STATUTE,
        act_or_regulation="The Patents Act, 1970",
        section_or_rule="Section 3(p)",
        jurisdiction=Jurisdiction.INDIA,
        content="Section 3(p) explicitly bars from patentability an invention which in effect is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components.",
        url_or_ref="https://ipindia.gov.in/patents-act-1970.htm"
    )
    ev2 = EvidenceChunk(
        id="EV-DCA-158B-CLASSICAL",
        title="Drugs & Cosmetics Rules 1945 - Rule 158B",
        source_type=EvidenceSourceType.RULE,
        act_or_regulation="Drugs and Cosmetics Rules, 1945",
        section_or_rule="Rule 158B(I)(A)",
        jurisdiction=Jurisdiction.INDIA,
        content="For classical Ayurvedic medicines mentioned in authoritative books specified in the First Schedule, proof of safety and efficacy is substantiated by citation of textual reference from the authoritative text. Clinical trials are not required for manufacturing license under Form 25D.",
        url_or_ref="https://ayush.gov.in/dca-rules-158b"
    )
    ev3 = EvidenceChunk(
        id="EV-TKDL-CHYAWAN",
        title="TKDL Classical Reference - Charaka Samhita Chikitsa Sthana 1:1",
        source_type=EvidenceSourceType.TKDL,
        act_or_regulation="Charaka Samhita",
        section_or_rule="Chikitsa Sthana Adhyaya 1, Verses 62-74",
        jurisdiction=Jurisdiction.INDIA,
        content="Chyawanprash formulation composed of Amalaki, Dashamoola, Pippali, Ghee, Honey, and 40+ herbs detailed as Rasayana for longevity and immunity.",
        url_or_ref="TKDL ID: CS/1042"
    )
    ev4 = EvidenceChunk(
        id="EV-BDA-SEC7",
        title="Biological Diversity Act 2002 - Section 7",
        source_type=EvidenceSourceType.STATUTE,
        act_or_regulation="The Biological Diversity Act, 2002",
        section_or_rule="Section 7",
        jurisdiction=Jurisdiction.INDIA,
        content="Prior intimation to State Biodiversity Board (SBB) is mandatory for Indian citizens and commercial entities obtaining biological resources for commercial utilization.",
        url_or_ref="https://nbaindia.org"
    )

    cit1 = Citation(
        citation_id="CIT-PAT-3P",
        act_or_text="The Patents Act, 1970",
        section_or_rule="Section 3(p)",
        jurisdiction=Jurisdiction.INDIA,
        summary_of_statute="Prohibits patenting of traditional knowledge and known properties of traditional herbal ingredients."
    )
    cit2 = Citation(
        citation_id="CIT-DCA-158B",
        act_or_text="Drugs and Cosmetics Rules, 1945",
        section_or_rule="Rule 158B(I)(A)",
        jurisdiction=Jurisdiction.INDIA,
        summary_of_statute="Governs licensing for classical ASU medicines via textual references from First Schedule texts."
    )
    cit3 = Citation(
        citation_id="CIT-BDA-SEC7",
        act_or_text="The Biological Diversity Act, 2002",
        section_or_rule="Section 7",
        jurisdiction=Jurisdiction.INDIA,
        summary_of_statute="Mandates prior intimation to State Biodiversity Board for commercial utilization of biological resources."
    )

    claims = [
        Claim(
            claim_id="CLM-01",
            statement="Classical Chyawanprash cannot be patented as a product in India due to statutory exclusion of traditional knowledge under Section 3(p).",
            associated_citations=["CIT-PAT-3P"],
            domain_topic="Patentability",
            target_jurisdiction=Jurisdiction.INDIA
        ),
        Claim(
            claim_id="CLM-02",
            statement="Manufacturing license for Classical Chyawanprash requires compliance with Rule 158B(I)(A) via textual reference to Charaka Samhita or AFI, without requiring mandatory clinical trials.",
            associated_citations=["CIT-DCA-158B"],
            domain_topic="Manufacturing License",
            target_jurisdiction=Jurisdiction.INDIA
        ),
        Claim(
            claim_id="CLM-03",
            statement="Commercial production of Chyawanprash requires prior intimation to the concerned State Biodiversity Board (SBB) under Section 7 of the Biological Diversity Act.",
            associated_citations=["CIT-BDA-SEC7"],
            domain_topic="ABS Compliance",
            target_jurisdiction=Jurisdiction.INDIA
        )
    ]

    draft_text = (
        "### Product Classification & IP Analysis: Classical Chyawanprash\n\n"
        "1. **Classification**: The product is categorized as a **Classical Ayurvedic Medicine** governed under Section 3(a) of the Drugs & Cosmetics Act 1940 and First Schedule (Charaka Samhita).\n"
        "2. **Patentability Assessment**: Classical Chyawanprash is directly barred from product patent grant in India under Section 3(p) of the Indian Patents Act, 1970 as it is codified Traditional Knowledge in TKDL.\n"
        "3. **Licensing & Regulatory Pathway**: An AYUSH Form 25D manufacturing license can be obtained under Rule 158B(I)(A) of Drugs & Cosmetics Rules 1945 by citing authoritative textual references (e.g., Charaka Samhita Chikitsa Sthana or Ayurvedic Formulary of India).\n"
        "4. **Biodiversity & ABS Obligations**: Under Section 7 of the Biological Diversity Act 2002, prior intimation to the State Biodiversity Board (SBB) is required for commercial sourcing of Indian herbal ingredients."
    )

    return UpstreamAgentOutput(
        query_id="QRY-2026-CHY-001",
        raw_user_query="Can I patent our Chyawanprash formulation in India and what are the licensing requirements?",
        product_name="Chyawanprash Awaleha",
        detected_category=AyurvedaCategory.CLASSICAL,
        botanical_and_herbal_ingredients=["Phyllanthus emblica (Amalaki)", "Piper longum (Pippali)", "Dashamoola", "Ghee", "Honey"],
        proposed_use_or_claim="Immunity booster and respiratory tonic based on Charaka Samhita",
        target_jurisdiction=Jurisdiction.INDIA,
        synthesis_draft_text=draft_text,
        extracted_claims=claims,
        citations_referenced=[cit1, cit2, cit3],
        retrieved_evidence=[ev1, ev2, ev3, ev4],
        metadata={"prior_art_found": True, "tkdl_match_confidence": 0.98}
    )


def _build_novel_phytopharmaceutical_scenario() -> UpstreamAgentOutput:
    ev1 = EvidenceChunk(
        id="EV-PAT-3D-3E",
        title="Patents Act 1970 - Section 3(d) & 3(e)",
        source_type=EvidenceSourceType.STATUTE,
        act_or_regulation="The Patents Act, 1970",
        section_or_rule="Section 3(d) and Section 3(e)",
        jurisdiction=Jurisdiction.INDIA,
        content="Section 3(d) requires demonstration of enhanced therapeutic efficacy for new derivatives or purified extracts. Section 3(e) requires proof of synergistic effect beyond mere admixture.",
        url_or_ref="https://ipindia.gov.in/patents-act-1970.htm"
    )
    ev2 = EvidenceChunk(
        id="EV-BDA-SEC-6",
        title="Biological Diversity Act 2002 - Section 6(1)",
        source_type=EvidenceSourceType.STATUTE,
        act_or_regulation="The Biological Diversity Act, 2002",
        section_or_rule="Section 6(1)",
        jurisdiction=Jurisdiction.INDIA,
        content="Section 6(1) mandates that no person shall apply for any IPR in or outside India for any invention based on biological resources obtained from India without obtaining prior approval of the National Biodiversity Authority (NBA) before patent grant.",
        url_or_ref="https://nbaindia.org/act-rules"
    )
    ev3 = EvidenceChunk(
        id="EV-DCA-PHYTO-2015",
        title="Drugs & Cosmetics Rules - Phytopharmaceutical Drug Definition",
        source_type=EvidenceSourceType.RULE,
        act_or_regulation="Drugs and Cosmetics Rules (GSR 918(E))",
        section_or_rule="Rule 2(eb)",
        jurisdiction=Jurisdiction.INDIA,
        content="Phytopharmaceutical drug means a purified and standardized fraction with defined minimum four bioactive or phytochemical marker compounds of an extract of a medicinal plant or its part, for internal or external use on human beings or animals for diagnosis, treatment, mitigation or prevention of any disease, requiring Phase I/II/III clinical trials under CDSCO.",
        url_or_ref="https://cdsco.gov.in"
    )

    cit1 = Citation(
        citation_id="CIT-PAT-3D",
        act_or_text="The Patents Act, 1970",
        section_or_rule="Section 3(d) & 3(e)",
        jurisdiction=Jurisdiction.INDIA,
        summary_of_statute="Requires demonstration of enhanced therapeutic efficacy and synergistic novelty over known prior art."
    )
    cit2 = Citation(
        citation_id="CIT-BDA-SEC6",
        act_or_text="The Biological Diversity Act, 2002",
        section_or_rule="Section 6(1)",
        jurisdiction=Jurisdiction.INDIA,
        summary_of_statute="Mandates prior approval from National Biodiversity Authority (NBA) before patent grant for biological resources."
    )

    claims = [
        Claim(
            claim_id="CLM-PHYTO-01",
            statement="A purified standardized cordifolioside fraction with synergistic action is patentable under the Indian Patents Act provided enhanced therapeutic efficacy under Section 3(d) and synergistic interaction under Section 3(e) are established.",
            associated_citations=["CIT-PAT-3D"],
            domain_topic="Patentability",
            target_jurisdiction=Jurisdiction.INDIA
        ),
        Claim(
            claim_id="CLM-PHYTO-02",
            statement="Patent applicant must obtain mandatory approval from the National Biodiversity Authority (NBA) under Section 6(1) of the Biological Diversity Act 2002 prior to patent grant.",
            associated_citations=["CIT-BDA-SEC6"],
            domain_topic="ABS Compliance",
            target_jurisdiction=Jurisdiction.INDIA
        ),
        Claim(
            claim_id="CLM-PHYTO-03",
            statement="If registered as a Phytopharmaceutical Drug under CDSCO Rule 2(eb), safety, toxicity, and Phase I/II clinical trial evidence are mandatory.",
            associated_citations=[],
            domain_topic="Clinical Trials",
            target_jurisdiction=Jurisdiction.INDIA
        )
    ]

    draft_text = (
        "### IP & Regulatory Strategy: Standardized Giloy Bioactive Fraction\n\n"
        "1. **Classification**: Categorized as a **Phytopharmaceutical Drug** (CDSCO Rule 2(eb)) or **Proprietary Ayurvedic Medicine** (Rule 158B(II)) depending on purification depth.\n"
        "2. **Patentability (Novelty & Inventive Step)**: Patentable as an extraction process and synergistic formulation provided comparative efficacy data over raw Giloy is filed under Sections 3(d) and 3(e).\n"
        "3. **Biodiversity / NBA Mandatory Approval**: Because Indian *Tinospora cordifolia* is utilized, filing Form III with the National Biodiversity Authority (NBA) under Section 6(1) is legally required before patent grant.\n"
        "4. **Clinical Efficacy**: Requires standardized chemical profiling (HPLC fingerprinting with 4+ markers) and CDSCO-approved clinical trials."
    )

    return UpstreamAgentOutput(
        query_id="QRY-2026-PHYTO-002",
        raw_user_query="We developed a novel purified Giloy cordifolioside extract that shows 3x antidiabetic potency. How do we protect and license it?",
        product_name="CordifoMet-Bio Extract",
        detected_category=AyurvedaCategory.PHYTOPHARMACEUTICAL,
        botanical_and_herbal_ingredients=["Tinospora cordifolia (Giloy / Guduchi) standardized cordifolioside fraction"],
        proposed_use_or_claim="Enhanced glycaemic regulation and metabolic control",
        target_jurisdiction=Jurisdiction.INDIA,
        synthesis_draft_text=draft_text,
        extracted_claims=claims,
        citations_referenced=[cit1, cit2],
        retrieved_evidence=[ev1, ev2, ev3],
        metadata={"novelty_confidence": 0.89, "phytopharmaceutical_markers_defined": True}
    )


def _build_unsubstantiated_haldi_scenario() -> UpstreamAgentOutput:
    # Intentionally flawed upstream output: claims simple turmeric+black pepper is 100% novel and needs no NBA approval
    ev1 = EvidenceChunk(
        id="EV-TKDL-TURMERIC",
        title="TKDL - Haridra and Maricha in Inflammatory Disorders",
        source_type=EvidenceSourceType.TKDL,
        act_or_regulation="Ashtanga Hridaya",
        section_or_rule="Sutrasthana Adhyaya 15",
        jurisdiction=Jurisdiction.INDIA,
        content="Haridra (Curcuma longa) and Maricha (Piper nigrum) documented extensively for Shotha (inflammation) and metabolic agni deepana.",
        url_or_ref="TKDL Ref: AH/542"
    )

    claims = [
        Claim(
            claim_id="CLM-FLAWED-01",
            statement="Turmeric and Black Pepper simple powder mix is an entirely new composition with zero prior art and is directly patentable in India.",
            associated_citations=[],
            domain_topic="Patentability",
            target_jurisdiction=Jurisdiction.INDIA
        ),
        Claim(
            claim_id="CLM-FLAWED-02",
            statement="No Biodiversity Board or NBA permission is needed for commercializing Indian turmeric products.",
            associated_citations=[],
            domain_topic="ABS Compliance",
            target_jurisdiction=Jurisdiction.INDIA
        )
    ]

    draft_text = (
        "### IP Advisory: Turmeric-Pepper Health Powder\n\n"
        "1. **Patentability**: You can immediately file a product patent in India for Turmeric + Black Pepper mixture as it is completely novel.\n"
        "2. **Biodiversity**: No NBA or SBB filings are needed for Indian companies.\n"
        "3. **Licensing**: Direct marketing can start without AYUSH or FSSAI regulatory clearances."
    )

    return UpstreamAgentOutput(
        query_id="QRY-2026-FLAWED-003",
        raw_user_query="I mixed turmeric powder and black pepper. Can I patent this new formula in India and sell without licenses?",
        product_name="Haldi-Mirch Power Mix",
        detected_category=AyurvedaCategory.CLASSICAL,
        botanical_and_herbal_ingredients=["Curcuma longa (Haridra)", "Piper nigrum (Maricha)"],
        proposed_use_or_claim="Instant cure for joint pain",
        target_jurisdiction=Jurisdiction.INDIA,
        synthesis_draft_text=draft_text,
        extracted_claims=claims,
        citations_referenced=[],
        retrieved_evidence=[ev1],
        metadata={"flagged_by_rag": True, "high_prior_art_overlap": True}
    )


def _build_international_pct_scenario() -> UpstreamAgentOutput:
    ev1 = EvidenceChunk(
        id="EV-BDA-SEC-3",
        title="Biological Diversity Act 2002 - Section 3 & Section 6",
        source_type=EvidenceSourceType.STATUTE,
        act_or_regulation="The Biological Diversity Act, 2002",
        section_or_rule="Section 3 and Section 6(1)",
        jurisdiction=Jurisdiction.INDIA,
        content="Section 6(1) states no person shall apply for any intellectual property right outside India for any invention based on biological resources obtained from India without prior approval of NBA. Section 3 regulates non-Indian commercial access.",
        url_or_ref="https://nbaindia.org"
    )
    ev2 = EvidenceChunk(
        id="EV-USPTO-101",
        title="35 U.S. Code § 101 - Subject Matter Eligibility",
        source_type=EvidenceSourceType.STATUTE,
        act_or_regulation="35 U.S.C. § 101",
        section_or_rule="Section 101 / Mayo Collaborative v. Prometheus",
        jurisdiction=Jurisdiction.US,
        content="Laws of nature, natural phenomena, and abstract ideas are not patentable. Natural herbal extracts must be structurally modified or combined with non-natural synthetic delivery matrices to establish eligibility.",
        url_or_ref="https://www.uspto.gov"
    )

    cit1 = Citation(
        citation_id="CIT-BDA-SEC3-6",
        act_or_text="The Biological Diversity Act, 2002",
        section_or_rule="Section 3 & Section 6(1)",
        jurisdiction=Jurisdiction.INDIA,
        summary_of_statute="Requires NBA approval for foreign patent filings utilizing Indian biological material."
    )
    cit2 = Citation(
        citation_id="CIT-USPTO-101",
        act_or_text="35 U.S. Code § 101",
        section_or_rule="Section 101",
        jurisdiction=Jurisdiction.US,
        summary_of_statute="Governs natural product patent eligibility under US patent laws."
    )

    claims = [
        Claim(
            claim_id="CLM-INT-01",
            statement="Filing a foreign patent application (USPTO/EPO/PCT) for an invention using Indian Ashwagandha requires mandatory prior approval (Form III) from India's National Biodiversity Authority (NBA) under Section 6(1).",
            associated_citations=["CIT-BDA-SEC3-6"],
            domain_topic="ABS Clearance",
            target_jurisdiction=Jurisdiction.MULTI
        ),
        Claim(
            claim_id="CLM-INT-02",
            statement="For USPTO filing under 35 U.S.C. § 101, natural herbal extracts require demonstration of marked difference in characteristics or novel formulation matrix to overcome natural product exclusions.",
            associated_citations=["CIT-USPTO-101"],
            domain_topic="US Patentability",
            target_jurisdiction=Jurisdiction.US
        )
    ]

    draft_text = (
        "### Cross-Border IP & Regulatory Advisory: Ashwagandha Nanoparticulate Formulation\n\n"
        "1. **Indian Biodiversity Clearance (Mandatory Pre-requisite)**: Under Section 6(1) of the Biological Diversity Act, you must file Form III with the National Biodiversity Authority (NBA) in India prior to filing or prosecuting the patent application in the US or Europe.\n"
        "2. **USPTO 35 U.S.C. § 101 Compliance**: To satisfy USPTO natural product guidelines, the specification must emphasize the novel nanoparticle carrier matrix and pharmacokinetic bioavailability enhancement.\n"
        "3. **Export & Regulatory Compliance**: Export of bulk herbal extracts requires DGFT export clearance and US FDA Dietary Supplement (NDI/GRAS) or Cosmetic compliance."
    )

    return UpstreamAgentOutput(
        query_id="QRY-2026-PCT-004",
        raw_user_query="We want to file a US patent and export our Ashwagandha nano-formulation from India. What are the key IP and regulatory checkpoints?",
        product_name="AshwaNano Bio-Complex",
        detected_category=AyurvedaCategory.PROPRIETARY,
        botanical_and_herbal_ingredients=["Withania somnifera (Ashwagandha) standardized withanolides", "Liposomal lipid carrier"],
        proposed_use_or_claim="Neuroprotective and stress adaptation bio-enhanced delivery",
        target_jurisdiction=Jurisdiction.MULTI,
        synthesis_draft_text=draft_text,
        extracted_claims=claims,
        citations_referenced=[cit1, cit2],
        retrieved_evidence=[ev1, ev2],
        metadata={"cross_border": True, "target_jurisdictions": ["India", "US", "EPO"]}
    )
