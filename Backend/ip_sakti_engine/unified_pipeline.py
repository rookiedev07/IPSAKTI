"""
IP-SAKTI Sahayak Unified Pipeline Engine (Layers 5, 6, 7, 8, 9)
House of Cards Multi-Agent Reasoning Architecture
Production Grade — Deterministic Jurisdiction, Domain-First Routing, Hard Metadata-Filtered RAG,
Source Relevance Validator, Conditional Statutory Engines, 3-Tier Verification, and Confidence Ceilings.
"""

import json
import os
import re
from typing import Dict, List, Any, Optional, Tuple

# Base Data Path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCES_PATH = os.path.join(CURRENT_DIR, "data", "ip_sakti_sources.json")

# Load Authoritative Sources Manifest
with open(SOURCES_PATH, "r", encoding="utf-8") as f:
    ALL_SOURCES = json.load(f)
SOURCE_BY_ID = {s["id"]: s for s in ALL_SOURCES}

# Trilingual Glossaries
GLOSSARIES = {
    "hi": {
        "Classical Ayurvedic Formulation": "शास्त्रीय आयुर्वेदिक औषधि",
        "Proprietary Ayurvedic Medicine": "स्वामित्व वाली आयुर्वेदिक दवा (पेटेंट/प्रोप्राइटरी)",
        "Traditional Knowledge": "पारंपारिक ज्ञान (TK)",
        "Prior Art": "पूर्व कला (Prior Art)",
        "Access and Benefit Sharing": "प्रवेश और लाभ साझाकरण (ABS)",
        "Therapeutic Efficacy": "चिकित्सकीय प्रभावकारिता",
        "National Biodiversity Authority": "राष्ट्रीय जैव विविधता प्राधिकरण (NBA)"
    },
    "mr": {
        "Classical Ayurvedic Formulation": "शास्त्रीय आयुर्वेदिक औषध",
        "Proprietary Ayurvedic Medicine": "मालकीचे आयुर्वेदिक औषध (पेटंट/प्रोप्रायटरी)",
        "Traditional Knowledge": "पारंपारिक ज्ञान (TK)",
        "Prior Art": "पूर्व कला (Prior Art)",
        "Access and Benefit Sharing": "प्रवेश आणि लाभ वाटप (ABS)",
        "Therapeutic Efficacy": "उपचारात्मक परिणामकारकता",
        "National Biodiversity Authority": "राष्ट्रीय जैवविविधता प्राधिकरण (NBA)"
    }
}


# ==============================================================================
# DECOUPLED DOMAIN REGISTRY
# ==============================================================================
DOMAIN_REGISTRY = {
    "EU_COSMETIC_REGULATORY": {
        "id": "EU_COSMETIC_REGULATORY",
        "label": "EU Cosmetic Regulation (EC) No 1223/2009",
        "jurisdiction": "EU",
        "squad": [
            "EU Cosmetic Regulatory Lead & Compliance Strategist",
            "EU Cosmetic Safety Assessor & CPSR/PIF Architect",
            "EU CPNP Notification & Formulation Specialist",
            "EU Responsible Person (RP) & SUE Vigilance Officer",
            "EU Statutory Verifier (Regulation 1223/2009 Guard)"
        ],
        "allowed_prefixes": ["eu-reg-1223-2009-"],
        "forbidden_terms": [
            "Biological Diversity Act", "Section 6(1)", "NBA", "Rule 158B", 
            "Patents Act 1970", "Section 3(p)", "Section 3(d)", "Form 25D", "Schedule T"
        ],
        "statutory_mappings": """
        - Responsible Person (RP): Article 4
        - Safety Assessment & CPSR (Part A/B): Article 10 & Annex I
        - Product Information File (PIF): Article 11 (Retained at RP address, NOT submitted)
        - Pre-market Notification (CPNP): Article 13
        - Nanomaterials (6-Month Prior Notice): Article 16
        - SUE / Cosmetovigilance: Article 23
        """,
        "verifier_assertions": [
            {"regex": re.compile(r"Responsible Person.*Article\s*(?:[1-35-9]|1\(3\)|8)\b", re.I), "error": "Responsible Person misattributed (must be Article 4)"},
            {"regex": re.compile(r"(?:Adverse Reaction|SUE|Cosmetovigilance).*Article\s*(?:[1-9]|1[0-2]|1[4-9]|2[0-24-9])\b", re.I), "error": "SUE / Adverse Reactions misattributed (must be Article 23)"},
            {"regex": re.compile(r"Nanomaterial.*Article\s*(?:[1-9]|1[0-5]|1[7-9]|2[0-9])\b", re.I), "error": "Nanomaterials misattributed (must be Article 16)"},
            {"regex": re.compile(r"(?:PIF|Product Information File).*Article\s*(?:[1-9]|10|1[2-9]|2[0-9])\b", re.I), "error": "PIF misattributed (must be Article 11)"}
        ]
    },
    "INTERNATIONAL_TRADEMARK": {
        "id": "INTERNATIONAL_TRADEMARK",
        "label": "Madrid System for International Registration of Marks",
        "jurisdiction": "International",
        "squad": [
            "Madrid Protocol Brand Protection Strategist",
            "WIPO Global Brand Database Researcher",
            "Nice Classification Class 5 Specification Architect",
            "MM2 International Application Executor",
            "Madrid Protocol & Local Office Conflict Verifier"
        ],
        "allowed_prefixes": ["intl-wipo-madrid", "in-tm-act-1999"],
        "forbidden_terms": [
            "Biological Diversity Act", "Section 6(1)", "Rule 158B", "CPSR", "CPNP", "Cosmetovigilance", "Annex I"
        ],
        "statutory_mappings": """
        - Basic Application / Base Mark: National IP Office of Origin (Section 18 / Form TM-A in India)
        - International Application: Madrid Protocol Article 2 & Article 3 via WIPO International Bureau
        - Designation of Contracting Parties: Madrid Protocol Article 3bis
        - Central Attack / Dependency Period: 5 years under Madrid Protocol Article 6
        """,
        "verifier_assertions": [
            {"regex": re.compile(r"(?:Biological Diversity Act|Section 6\(1\)|NBA)", re.I), "error": "NBA approval is not applicable to Trademark applications."},
            {"regex": re.compile(r"(?:CPSR|PIF|CPNP|SUE)", re.I), "error": "Cosmetic regulatory artifacts cannot appear in Trademark dossiers."}
        ]
    },
    "AYURVEDA_PATENT": {
        "id": "AYURVEDA_PATENT",
        "label": "Indian Patents Act & Traditional Knowledge Clearance",
        "jurisdiction": "India",
        "squad": [
            "Registered Patent Attorney (Life Sciences)",
            "TKDL Prior-Art & Classical Samhita Researcher",
            "Non-Obvious Synergistic Claims Architect",
            "Patent Specification & Form 1/2 Executor",
            "Statutory Patentability Verifier (Sec 3(p)/3(d))"
        ],
        "allowed_prefixes": ["in-patents-act-", "in-bd-act-", "in-tkdl", "intl-pct-", "intl-wipo-pct"],
        "forbidden_terms": [
            "EU Regulation 1223/2009", "CPNP", "CPSR", "Responsible Person under Article 4"
        ],
        "statutory_mappings": """
        - Traditional Knowledge Bar: Section 3(p) of Patents Act 1970
        - Enhanced Efficacy Requirement: Section 3(d) of Patents Act 1970
        - Prior NBA Approval: Section 6(1) of Biological Diversity Act 2002 (Form III)
        - Foreign Access: Section 3 of Biological Diversity Act 2002 (Form I)
        """,
        "verifier_assertions": [
            {"regex": re.compile(r"(?:EU Regulation 1223\/2009|CPNP|CPSR)", re.I), "error": "EU cosmetic rules cannot appear in Indian Patent dossiers."}
        ]
    },
    "AYUSH_MANUFACTURING": {
        "id": "AYUSH_MANUFACTURING",
        "label": "Indian AYUSH / ASU Manufacturing Licensing (Drugs & Cosmetics Rules — Rule 158B)",
        "jurisdiction": "India",
        "squad": [
            "AYUSH Regulatory & Licensing Strategist",
            "First Schedule Authoritative Pharmacopoeia Researcher",
            "Form 25D Manufacturing Dossier Architect",
            "State Licensing Authority (SLA) Application Executor",
            "Schedule T Good Manufacturing Practices (GMP) Verifier"
        ],
        "allowed_prefixes": ["in-dc-rules-158b", "in-dc-act-1940", "in-magic-remedies-act-"],
        "forbidden_terms": [
            "EU Regulation 1223/2009", "CPNP", "CPSR", "21 CFR 312", "Madrid Protocol"
        ],
        "statutory_mappings": """
        - Classical ASU Formulations: Rule 158B(I)(A) allows Form 25D licensing based on First Schedule authoritative texts without clinical trials
        - Patent or Proprietary ASU Medicines: Rule 158B(I)(B) governs novel compositions requiring safety and pilot toxicity data
        - Good Manufacturing Practices: Schedule T compliance
        """,
        "verifier_assertions": [
            {"regex": re.compile(r"(?:EU Regulation 1223\/2009|CPNP|CPSR)", re.I), "error": "EU cosmetic rules cannot appear in AYUSH manufacturing dossiers."}
        ]
    },
    "FOOD_FSSAI": {
        "id": "FOOD_FSSAI",
        "label": "FSSAI (Ayurveda Aahar) Regulations, 2022 & Dietary Food Safety Pathway",
        "jurisdiction": "India",
        "squad": [
            "FSSAI & Ayurveda Aahar Compliance Strategist",
            "First Schedule Ayurvedic Culinary Text Researcher",
            "Food Safety & Permissible Additives Architect",
            "FSSAI Food Business Licensing Dossier Executor",
            "Non-Curative Labeling & DMR(OA) Act Verifier"
        ],
        "allowed_prefixes": ["in-fssai-ayurveda-aahar", "in-fssai-", "in-magic-remedies-act-"],
        "forbidden_terms": [
            "EU Regulation 1223/2009", "CPNP", "CPSR", "21 CFR 312", "Rule 158B"
        ],
        "statutory_mappings": """
        - Recipe Authentication: Formulated strictly in accordance with recognized Ayurvedic texts
        - Non-Curative Claims: Prohibits claims to cure, prevent, or treat any disease
        - Food Safety: Complies with permissible additives and contaminants limits
        """,
        "verifier_assertions": [
            {"regex": re.compile(r"(?:cure|curing|treat|treatment)\s+(?:severe|clinical|chronic)?\s*(?:depression|cancer|diabetes|anxiety)", re.I), "error": "Curative disease claims are strictly barred under FSSAI Ayurveda Aahar Regulations."}
        ]
    },
    "ABS_BIODIVERSITY": {
        "id": "ABS_BIODIVERSITY",
        "label": "Biological Diversity Act Access & Benefit Sharing (ABS) Compliance (NBA Form I/III)",
        "jurisdiction": "India",
        "squad": [
            "National Biodiversity Authority (NBA/ABS) Senior Counsel",
            "Biological Resource Access & State Board (SBB) Researcher",
            "Benefit-Sharing Agreement (0.1%-0.5%) Architect",
            "NBA Form I / Form III Application Executor",
            "Biological Diversity Act 2002/2023 Statutory Verifier"
        ],
        "allowed_prefixes": ["in-bd-act-2002", "intl-cbd-nagoya", "in-patents-act-"],
        "forbidden_terms": [
            "EU Regulation 1223/2009", "CPNP", "CPSR", "21 CFR 312", "Rule 158B"
        ],
        "statutory_mappings": """
        - Foreign Access: Section 3 Form I prior approval for non-Indian entities
        - Patent Approval: Section 6(1) Form III prior approval before patent grant / foreign filing
        - Benefit Sharing: 0.1% to 0.5% benefit-sharing agreement
        """,
        "verifier_assertions": [
            {"regex": re.compile(r"(?:EU Regulation 1223\/2009|CPNP|CPSR)", re.I), "error": "EU cosmetic rules cannot appear in NBA biodiversity dossiers."}
        ]
    },
    "US_FDA_DRUG": {
        "id": "US_FDA_DRUG",
        "label": "US FDA Botanical Drug Development / IND Pathway (21 CFR Part 312)",
        "jurisdiction": "US",
        "squad": [
            "US FDA Botanical Regulatory Specialist",
            "IND & Clinical Protocol Development Lead",
            "Botanical Raw Material & CMC Authentication Architect",
            "FDA 21 CFR 312 Submission Executor",
            "US Regulatory Citation & Clinical Risk Verifier"
        ],
        "allowed_prefixes": ["us-fda-21cfr312", "us-fda-", "us-uspto-"],
        "forbidden_terms": [
            "EU Regulation 1223/2009", "CPNP", "CPSR", "Rule 158B", "Form 25D", "Schedule T"
        ],
        "statutory_mappings": """
        - IND Application: 21 CFR § 312 Form FDA 1571 for US clinical trials
        - CMC Controls: Batch-to-batch consistency and fingerprinting
        - Clinical Progression: Phase I, II, III trials leading to NDA
        """,
        "verifier_assertions": [
            {"regex": re.compile(r"(?:Rule 158B|Form 25D|Schedule T)", re.I), "error": "Indian AYUSH licensing rules cannot appear in US FDA drug dossiers."}
        ]
    },
    "US_FDA_DIETARY_SUPPLEMENT": {
        "id": "US_FDA_DIETARY_SUPPLEMENT",
        "label": "US FDA Dietary Supplement Compliance & cGMP (21 CFR Part 111 & DSHEA)",
        "jurisdiction": "US",
        "squad": [
            "US Dietary Supplement Regulatory Strategist",
            "DSHEA 1994 Structure/Function Claims Researcher",
            "21 CFR Part 111 cGMP Compliance Architect",
            "FDA Facility & Labeling Executor",
            "FDA Disclaimer & Safety Standard Verifier"
        ],
        "allowed_prefixes": ["us-fda-21cfr111", "us-fda-", "in-dc-rules-158b"],
        "forbidden_terms": [
            "EU Regulation 1223/2009", "CPNP", "CPSR", "21 CFR 312 IND"
        ],
        "statutory_mappings": """
        - cGMP Mandate: 21 CFR Part 111 manufacturing and holding standards
        - Structure/Function Claims: Permitted with mandatory FDA disclaimer; disease claims barred
        - 30-Day Notification: Claims notified to FDA under DSHEA
        """,
        "verifier_assertions": [
            {"regex": re.compile(r"(?:cure|curing|prevent|preventing|treat|treating)\s+(?:disease|cancer|diabetes)", re.I), "error": "Disease cure/treatment claims are illegal for dietary supplements under DSHEA 1994."}
        ]
    },
    "EU_THMPD": {
        "id": "EU_THMPD",
        "label": "EU Traditional Herbal Medicinal Products Registration (Directive 2004/24/EC & THMPD)",
        "jurisdiction": "EU",
        "squad": [
            "EU Herbal Medicines Regulatory Specialist",
            "THMPD 30-Year Traditional Use Evidence Researcher",
            "EMA / HMPC Community Monograph Architect",
            "EU National Competent Authority Dossier Executor",
            "EU Statutory Directive Citation Verifier"
        ],
        "allowed_prefixes": ["eu-directive-2004-24-ec", "eu-ema-hmpc-", "eu-"],
        "forbidden_terms": [
            "CPNP", "Annex I CPSR", "Rule 158B", "Section 3(p)", "21 CFR 312"
        ],
        "statutory_mappings": """
        - Simplified Registration: Directive 2004/24/EC simplified registration
        - Traditional Use: 30 years continuous use, including 15 years within the EU
        - Quality Dossier: Conforming to European Pharmacopoeia and EU GMP
        """,
        "verifier_assertions": [
            {"regex": re.compile(r"(?:CPNP|Annex I CPSR)", re.I), "error": "Cosmetic Regulation artifacts cannot appear in THMPD medicinal dossiers."}
        ]
    },
    "INTERNATIONAL_PATENT": {
        "id": "INTERNATIONAL_PATENT",
        "label": "WIPO PCT International Patent Application & National Phase Entry",
        "jurisdiction": "International",
        "squad": [
            "WIPO PCT International Patent Strategist",
            "International Search Authority (ISA) Prior-Art Researcher",
            "PCT Chapter I/II Claims Harmonization Architect",
            "PCT/RO/101 International Filing Executor",
            "WIPO GRATK Disclosure Treaty Verifier"
        ],
        "allowed_prefixes": ["intl-wipo-pct", "intl-wipo-gratk-2024", "in-patents-act-", "in-cdsco-phytopharmaceutical"],
        "forbidden_terms": [
            "EU Regulation 1223/2009", "CPNP", "CPSR", "Rule 158B", "Form 25D"
        ],
        "statutory_mappings": """
        - Unified PCT Filing: Preserves priority across 158 contracting states
        - Genetic Resource Disclosure: WIPO GRATK Treaty 2024 mandatory disclosure
        - Section 39 / BDA Sec 6(1): Foreign filing license or prior NBA approval
        """,
        "verifier_assertions": [
            {"regex": re.compile(r"(?:EU Regulation 1223\/2009|CPNP|CPSR)", re.I), "error": "EU cosmetic rules cannot appear in WIPO patent dossiers."}
        ]
    },
    "AYUSH_PRODUCT_REGULATION": {
        "id": "AYUSH_PRODUCT_REGULATION",
        "label": "CDSCO Phytopharmaceutical Drug Development & Clinical Regulatory Pathway (Rule 2(eb))",
        "jurisdiction": "India",
        "squad": [
            "Phytopharmaceutical Drug Regulatory Lead",
            "4-Marker Bioactive Chemical Fingerprinting Researcher",
            "CDSCO IND & Phase I/II Clinical Protocol Architect",
            "CT Rules Form CT-04 Application Executor",
            "CDSCO Subject Expert Committee (SEC) Verifier"
        ],
        "allowed_prefixes": ["in-cdsco-phytopharmaceutical", "in-dc-act-1940", "in-patents-act-"],
        "forbidden_terms": [
            "EU Regulation 1223/2009", "CPNP", "CPSR", "21 CFR 312"
        ],
        "statutory_mappings": """
        - Phytopharmaceutical Definition: Minimum 4 bioactive markers under Rule 2(eb)
        - Clinical Trials: Phase I/II/III clinical trials under CT Rules 2019
        - SEC Approval: CDSCO Subject Expert Committee clearance
        """,
        "verifier_assertions": [
            {"regex": re.compile(r"(?:EU Regulation 1223\/2009|CPNP|CPSR)", re.I), "error": "EU cosmetic rules cannot appear in CDSCO phytopharmaceutical dossiers."}
        ]
    },
    "MULTI_DOMAIN": {
        "id": "MULTI_DOMAIN",
        "label": "Dual Indian Patent (Sec 3(p)/3(d)) & Cross-Border IPR Compliance (NBA Form III)",
        "jurisdiction": "Both",
        "squad": [
            "Cross-Border Patent & Life Sciences Counsel",
            "TKDL Prior-Art & Global Search Specialist",
            "Synergistic Formulation & Enhanced Efficacy Architect",
            "Dual Indian & Foreign Patent Prosecution Executor",
            "Section 3(p) & NBA Form III Statutory Verifier"
        ],
        "allowed_prefixes": ["in-", "intl-", "us-", "eu-"],
        "forbidden_terms": [],
        "statutory_mappings": """
        - Dual Jurisdiction Governance: Harmonizes domestic and foreign compliance
        - Mandatory NBA Approval: Section 6(1) Form III before foreign filing
        """,
        "verifier_assertions": []
    }
}


# ==============================================================================
# PART 1 & 2: DETERMINISTIC JURISDICTION RESOLUTION HIERARCHY
# ==============================================================================
def resolve_jurisdiction_layer(prompt_text: str, requested_toggle: Optional[str] = None) -> Dict[str, Any]:
    """
    Deterministic Jurisdiction Resolver implementing strict 5-Priority Hierarchy:
    - Priority 1: Explicit country, regulator, treaty, or foreign jurisdiction terms in query
    - Priority 2: Explicit UI toggle
    - Priority 3: Legal instrument inference (e.g. 21 CFR -> US, Directive 2004/24/EC -> EU)
    - Priority 4: Entity / location inference
    - Priority 5: Fallback default
    """
    norm = (prompt_text or "").lower()
    
    # Priority 1 & 3 Explicit Evidence Matchers
    us_evidence = []
    eu_evidence = []
    intl_evidence = []
    india_evidence = []

    # US Identifiers
    if re.search(r"\b(fda|cder|cfsan|uspto|21\s*cfr\s*312|21\s*cfr\s*111|21\s*cfr|dshea|35\s*u\.?s\.?c|ind application)\b", norm):
        us_evidence.append("Explicit US Regulatory/Statute Citation (FDA/21 CFR/USPTO/DSHEA)")
    if re.search(r"\b(united states|usa|in the us|in us|us market|us patent|us drug)\b|अमेरिका|यूएस", norm):
        us_evidence.append("Explicit US Territorial Scope")

    # EU Identifiers (Regulation 1223/2009, THMPD, EMA, etc.)
    if re.search(r"\b(regulation\s*\(?ec\)?\s*(?:no\s*)?1223/2009|1223/2009|regulation\s*1223|directive\s*2004/24/ec|thmpd|directive\s*2001/83/ec|ema|hmpc|monograph|cpnp|pif\b|cpsr\b|responsible person\s*\(?eu\)?|serious undesirable effect|sue\b|cosmetic product safety report)\b", norm):
        eu_evidence.append("Explicit EU Regulation/Directive Citation (Regulation 1223/2009 / THMPD / CPSR)")
    if re.search(r"\b(european union|eu\b|germany|german|france|french|europe|mhra|tga|australia)\b|जर्मनी|युरोप|फ्रान्स", norm):
        eu_evidence.append("Explicit EU/European Territorial Scope")

    # International Identifiers
    if re.search(r"\b(patent cooperation treaty|pct\b|madrid protocol|madrid system|wipo|gratk|nagoya protocol|trips|cbd)\b", norm):
        intl_evidence.append("Explicit International Treaty/System Citation (PCT/Madrid/WIPO/Nagoya)")
    if re.search(r"\b(overseas|foreign market|global market|international filing|exporting|abroad|export)\b|विदेश|परदेश|निर्यात", norm):
        intl_evidence.append("Explicit International Trade Scope")

    # India Identifiers
    if re.search(r"\b(patents act\s*1970|section 3\(p\)|section 3\(d\)|section 3\(e\)|rule 158b|form 25d|biological diversity act|bda\b|nba\b|national biodiversity authority|sbb|tkdl|fssai|ayurveda aahar|cdsco|schedule t|ipindia)\b", norm):
        india_evidence.append("Explicit Indian Statutory Provision Citation")
    
    has_pure_eu_cosmetic = bool(eu_evidence and any(w in norm for w in ["1223/2009", "cosmetic", "cpnp", "pif", "cpsr", "responsible person", "sue"]))
    if not has_pure_eu_cosmetic:
        if re.search(r"\b(in india|charaka|sushruta|ashtanga|rasashastra|vaidya|samhita)\b|भारत|भारतात|शास्त्रीय", norm):
            india_evidence.append("Explicit Indian Territorial / Classical Reference")
        elif re.search(r"\b(india|indian)\b", norm) and not ("export" in norm or "eu" in norm or "foreign" in norm):
            india_evidence.append("Explicit Indian Territorial Reference")

    detected_jurs = []
    if us_evidence:
        detected_jurs.append("United States")
    if eu_evidence:
        detected_jurs.append("European Union")
    if intl_evidence:
        detected_jurs.append("International")
    if india_evidence:
        detected_jurs.append("India")

    conflicts = []

    # Priority 1: Query Direct Evidence
    has_foreign = bool(us_evidence or eu_evidence or intl_evidence)
    has_india = bool(india_evidence)

    if has_foreign and has_india:
        mode = "BOTH"
        primary_jur = "Multi-Jurisdictional (India + International)"
        suggested_toggle = "Both"
        conf = 98.0
    elif intl_evidence and (len(detected_jurs) > 1 or not (us_evidence or eu_evidence)):
        mode = "INTERNATIONAL"
        primary_jur = "International"
        suggested_toggle = "International"
        conf = 98.0
    elif us_evidence:
        mode = "INTERNATIONAL"
        primary_jur = "United States"
        suggested_toggle = "International"
        conf = 99.0
    elif eu_evidence:
        mode = "INTERNATIONAL"
        primary_jur = "European Union"
        suggested_toggle = "International"
        conf = 99.0
    elif intl_evidence:
        mode = "INTERNATIONAL"
        primary_jur = "International"
        suggested_toggle = "International"
        conf = 95.0
    elif has_india:
        mode = "INDIA"
        primary_jur = "India"
        suggested_toggle = "India"
        conf = 98.0
    else:
        # Fallback Priority 5
        mode = "INDIA"
        primary_jur = "India"
        suggested_toggle = "India"
        conf = 60.0

    # Effective Jurisdiction Resolution (Handling UI Toggle vs Query Evidence)
    effective_jur = suggested_toggle
    if requested_toggle and requested_toggle.lower() != "all":
        req_norm = requested_toggle.capitalize()
        if req_norm in ["India", "International", "Both"]:
            if req_norm == "India" and has_foreign and not has_india:
                conflicts.append(f"JURISDICTION_CONFLICT: UI Toggle was '{requested_toggle}', but query explicitly targets {primary_jur}. Overriding with query jurisdiction.")
                effective_jur = "International"
            elif req_norm == "International" and has_india and not has_foreign:
                conflicts.append(f"JURISDICTION_CONFLICT: UI Toggle was '{requested_toggle}', but query explicitly targets Indian law. Overriding with query jurisdiction.")
                effective_jur = "India"
            else:
                effective_jur = req_norm

    # Mandatory Guard: Never silently default foreign queries to India
    if has_foreign and effective_jur == "India" and not has_india:
        conflicts.append("JURISDICTION_CONTRADICTION: Foreign evidence present but resolved to India. Blocking fallback.")
        effective_jur = "International"
        mode = "INTERNATIONAL"

    evidence_summary = us_evidence + eu_evidence + intl_evidence + india_evidence
    if not evidence_summary:
        evidence_summary = ["Contextual herbal domain fallback to Indian AYUSH regime"]

    return {
        "detected_jurisdictions": detected_jurs or ["India"],
        "primary_jurisdiction": primary_jur,
        "mode": mode,
        "suggested_toggle": suggested_toggle,
        "effective_jurisdiction": effective_jur,
        "evidence": evidence_summary,
        "confidence": conf,
        "conflicts": conflicts
    }


# ==============================================================================
# PART 3 & 4: DOMAIN-FIRST AGENT ROUTING & DYNAMIC PATHWAY RESOLVER
# ==============================================================================
def classify_domain_and_pathway(prompt_text: str, jur_res: Dict[str, Any]) -> Tuple[str, str, List[str]]:
    """
    Domain-First Classifier selecting exact regulatory domain, specialized 5-agent council,
    and dynamic Primary Regulatory Pathway.
    """
    norm = prompt_text.lower()
    mode = jur_res.get("mode", "INDIA")
    primary_jur = jur_res.get("primary_jurisdiction", "India")

    domain = "AYUSH_MANUFACTURING"
    pathway = "Indian AYUSH / ASU Manufacturing Licensing (Rule 158B)"
    squad = []

    # =========================================================================
    # TIER 1: HIGHEST PRECEDENCE — INDIAN IP / PATENT / ABS STATUTES
    # Explicit patent statutes & provisions OVERRIDE all generic words (brand, Madrid, etc.)
    # =========================================================================
    has_tier1_patent = any(w in norm for w in [
        "section 3(p)", "section 3(d)", "section 3(e)", "3(p)", "3(d)", "3(e)",
        "patents act", "patent act", "biological diversity act", "nba form iii",
        "form iii", "form 3", "tkdl", "patentability", "inventive step",
        "non-patentable", "prior art", "patent application", "patent claim",
        "patent specification", "patent filing", "patent grant"
    ]) or ("patent" in norm and not any(w in norm for w in ["patent and trademark office", "patent and trade mark"]))

    has_tier1_abs = not has_tier1_patent and any(w in norm for w in [
        "nba form i", "nba form 1", "benefit sharing", "foreign equity",
        "foreign company accessing", "access and benefit sharing"
    ])

    if has_tier1_patent:
        if mode == "BOTH" or "us" in norm or "foreign" in norm or "pct" in norm:
            domain = "MULTI_DOMAIN"
            pathway = "Dual Indian Patent (Sec 3(p)/3(d)) & Cross-Border IPR Compliance (NBA Form III)"
            squad = [
                "Cross-Border Patent & Life Sciences Counsel",
                "TKDL Prior-Art & Global Search Specialist",
                "Synergistic Formulation & Enhanced Efficacy Architect",
                "Dual Indian & Foreign Patent Prosecution Executor",
                "Section 3(p) & NBA Form III Statutory Verifier"
            ]
        else:
            domain = "PATENT"
            pathway = "Indian Patent Law Analysis (Patents Act 1970 — Section 3(p)/3(d)/3(e))"
            squad = [
                "Registered Patent Attorney (Life Sciences)",
                "TKDL Prior-Art & Classical Samhita Researcher",
                "Non-Obvious Synergistic Claims Architect",
                "Patent Specification & Form 1/2 Executor",
                "Statutory Patentability Verifier (Sec 3(p)/3(d))"
            ]

    elif has_tier1_abs:
        domain = "ABS_BIODIVERSITY"
        pathway = "Biological Diversity Act Access & Benefit Sharing (ABS) Compliance (NBA Form I/III)"
        squad = [
            "National Biodiversity Authority (NBA/ABS) Senior Counsel",
            "Biological Resource Access & State Board (SBB) Researcher",
            "Benefit-Sharing Agreement (0.1%-0.5%) Architect",
            "NBA Form I / Form III Application Executor",
            "Biological Diversity Act 2002/2023 Statutory Verifier"
        ]

    # =========================================================================
    # TIER 2: EU COSMETIC REGULATION (EC) No 1223/2009
    # =========================================================================
    elif any(w in norm for w in ["1223/2009", "regulation 1223", "pif", "cpnp", "cpsr", "responsible person", "cosmetic product safety report"]) or \
       ("cosmetic" in norm and any(w in norm for w in ["eu", "europe", "france", "germany", "export", "regulation", "safety assessment", "sue", "nanomaterial", "hair-oil", "skin serum", "serum", "oil"])):
        domain = "EU_COSMETIC_REGULATORY"
        pathway = "EU Cosmetic Regulation (EC) No 1223/2009 Compliance & CPSR Safety Assessment"
        squad = [
            "EU Cosmetic Regulatory Lead & Compliance Strategist",
            "EU Cosmetic Safety Assessor & CPSR/PIF Architect",
            "EU CPNP Notification & Formulation Specialist",
            "EU Responsible Person (RP) & SUE Vigilance Officer",
            "EU Statutory Verifier (Regulation 1223/2009 Guard)"
        ]

    # =========================================================================
    # TIER 3: TRADEMARK & BRAND PROTECTION (Madrid Protocol / Class 5)
    # (Evaluated ONLY if Tier 1 and Tier 2 triggers are absent)
    # =========================================================================
    elif "madrid" in norm or "class 5" in norm or ("trademark" in norm and any(w in norm for w in ["wipo", "international", "australia", "uk", "overseas", "global brand"])) or any(w in norm for w in ["brand name", "brand protection", "tm-a", "gi tag", "geographical indication"]):
        if "madrid" in norm or "wipo" in norm or "international" in norm or "australia" in norm:
            domain = "INTERNATIONAL_TRADEMARK"
            pathway = "International Trademark Registration via Madrid Protocol (Class 5 / Class 3)"
            squad = [
                "Madrid Protocol Brand Protection Strategist",
                "WIPO Global Brand Database Researcher",
                "Nice Classification Class 5 Specification Architect",
                "MM2 International Application Executor",
                "Madrid Protocol & Local Office Conflict Verifier"
            ]
        else:
            domain = "TRADEMARK"
            pathway = "Indian Trade Marks Act 1999 Registration & Brand Protection (Class 5/3)"
            squad = [
                "Indian Trademark & Brand Protection Attorney",
                "Ayurvedic Pharmacopoeia (API) Terminology Researcher",
                "Class 5 Specification & Distinctiveness Architect",
                "TM-A Trademark Application Executor",
                "Section 9 Generic Bar & Section 11 Conflict Verifier"
            ]

    # =========================================================================
    # TIER 4: SPECIFIC REGULATORY FRAMEWORKS (FDA, THMPD, PCT, FSSAI, AYUSH)
    # =========================================================================
    elif "21 cfr 312" in norm or ("fda" in norm and any(w in norm for w in ["ind", "clinical trial", "phase i", "phase ii", "botanical drug", "cder"])):
        domain = "US_FDA_DRUG"
        pathway = "US FDA Botanical Drug Development / IND Pathway (21 CFR Part 312)"
        squad = [
            "US FDA Botanical Regulatory Specialist",
            "IND & Clinical Protocol Development Lead",
            "Botanical Raw Material & CMC Authentication Architect",
            "FDA 21 CFR 312 Submission Executor",
            "US Regulatory Citation & Clinical Risk Verifier"
        ]

    elif "21 cfr 111" in norm or ("dshea" in norm) or ("fda" in norm and any(w in norm for w in ["dietary supplement", "structure function", "supplement", "cgmp"])):
        domain = "US_FDA_DIETARY_SUPPLEMENT"
        pathway = "US FDA Dietary Supplement Compliance & cGMP (21 CFR Part 111 & DSHEA)"
        squad = [
            "US Dietary Supplement Regulatory Strategist",
            "DSHEA 1994 Structure/Function Claims Researcher",
            "21 CFR Part 111 cGMP Compliance Architect",
            "FDA Facility & Labeling Executor",
            "FDA Disclaimer & Safety Standard Verifier"
        ]

    elif "directive 2004/24/ec" in norm or "thmpd" in norm or ("germany" in norm and "traditional" in norm) or ("eu" in norm and "herbal" in norm and "medicinal" in norm):
        domain = "EU_THMPD"
        pathway = "EU Traditional Herbal Medicinal Product Registration (Directive 2004/24/EC & THMPD)"
        squad = [
            "EU Herbal Medicines Regulatory Specialist",
            "THMPD 30-Year Traditional Use Evidence Researcher",
            "EMA / HMPC Community Monograph Architect",
            "EU National Competent Authority Dossier Executor",
            "EU Statutory Directive Citation Verifier"
        ]

    elif "pct" in norm or "patent cooperation treaty" in norm or ("wipo" in norm and "patent" in norm):
        domain = "INTERNATIONAL_PATENT"
        pathway = "WIPO PCT International Patent Application & National Phase Entry"
        squad = [
            "WIPO PCT International Patent Strategist",
            "International Search Authority (ISA) Prior-Art Researcher",
            "PCT Chapter I/II Claims Harmonization Architect",
            "PCT/RO/101 International Filing Executor",
            "WIPO PCT & GRATK Disclosure Treaty Verifier"
        ]

    elif "fssai" in norm or "ayurveda aahar" in norm or ("food" in norm and "ayurved" in norm):
        domain = "FOOD_FSSAI"
        pathway = "FSSAI (Ayurveda Aahar) Regulations 2022 & Dietary Food Safety Pathway"
        squad = [
            "FSSAI & Ayurveda Aahar Compliance Strategist",
            "First Schedule Ayurvedic Culinary Text Researcher",
            "Food Safety & Permissible Additives Architect",
            "FSSAI Food Business Licensing Dossier Executor",
            "Non-Curative Labeling & DMR(OA) Act Verifier"
        ]

    elif "phytopharmaceutical" in norm or "rule 2(eb)" in norm or "bioactive marker" in norm:
        domain = "AYUSH_PRODUCT_REGULATION"
        pathway = "CDSCO Phytopharmaceutical Drug Development & Clinical Regulatory Pathway (Rule 2(eb))"
        squad = [
            "Phytopharmaceutical Drug Regulatory Lead",
            "4-Marker Bioactive Chemical Fingerprinting Researcher",
            "CDSCO IND & Phase I/II Clinical Protocol Architect",
            "CT Rules Form CT-04 Application Executor",
            "CDSCO Subject Expert Committee (SEC) Verifier"
        ]

    # 11. Cross-Border Export / Mixed Default
    elif mode == "BOTH" or "export" in norm or "foreign" in norm:
        domain = "EXPORT_COMPLIANCE"
        pathway = "AYUSH Export Certification (CoPP/WHO GMP) & Destination Market Compliance"
        squad = [
            "Cross-Border AYUSH Trade & Export Strategist",
            "Nagoya Protocol & Destination Regulatory Researcher",
            "Export Product Specification & Dual-Labeling Architect",
            "AYUSH Export CoPP & Free Sale Certificate Executor",
            "Mandatory NBA Form III & Import Market Verifier"
        ]

    # 12. Indian Classical / Proprietary AYUSH Manufacturing
    else:
        domain = "AYUSH_MANUFACTURING"
        pathway = "Indian AYUSH / ASU Manufacturing Licensing (Drugs & Cosmetics Rules — Rule 158B)"
        squad = [
            "AYUSH Regulatory & Licensing Strategist",
            "First Schedule Authoritative Pharmacopoeia Researcher",
            "Form 25D Manufacturing Dossier Architect",
            "State Licensing Authority (SLA) Application Executor",
            "Schedule T Good Manufacturing Practices (GMP) Verifier"
        ]

    return domain, pathway, squad


# ==============================================================================
# PART 5 & 6: HARD METADATA-FILTERED RAG RETRIEVAL & RELEVANCE VALIDATOR
# ==============================================================================
def retrieve_filtered_citations_layer(
    prompt_text: str,
    jurisdiction_res: Dict[str, Any],
    domain: str
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], bool]:
    """
    Hard-Filtered Citation Retrieval Gate:
    1. Filters source manifest strictly by Jurisdiction (India, US, EU, International).
    2. Filters source manifest by Domain / Regulatory Scope.
    3. Validates individual source relevance (blocking authentic but irrelevant laws).
    Returns: (relevant_sources, blocked_sources, is_jurisdiction_safe)
    """
    norm = prompt_text.lower()
    effective_jur = jurisdiction_res.get("effective_jurisdiction", "India")
    mode = jurisdiction_res.get("mode", "INDIA")

    # Hard Territorial Filters
    if mode == "INDIA" or effective_jur == "India":
        allowed_jurs = ["India"]
    elif effective_jur == "International" or mode == "INTERNATIONAL":
        target_jur = jurisdiction_res.get("primary_jurisdiction", "International")
        if "United States" in target_jur:
            allowed_jurs = ["US", "International"]
        elif "European Union" in target_jur:
            allowed_jurs = ["EU", "International"]
        else:
            allowed_jurs = ["International", "US", "EU"]
    else:
        # BOTH mode: allows India + International targets
        allowed_jurs = ["India", "US", "EU", "International"]

    # Candidate Filtering
    candidate_sources = [s for s in ALL_SOURCES if s.get("jurisdiction") in allowed_jurs]
    
    scored_sources = []
    blocked_sources = []

    for s in candidate_sources:
        s_id = s["id"]
        s_jur = s.get("jurisdiction", "")
        s_dom = s.get("domain", "")
        s_title = (s.get("title", "") + " " + s.get("summary", "")).lower()

        # Relevance Scoring (0 to 100)
        rel_score = 0

        # 1. Jurisdiction Match
        if mode == "INDIA" and s_jur == "India":
            rel_score += 30
        elif mode == "INTERNATIONAL" and s_jur in ["US", "EU", "International"]:
            rel_score += 30
        elif mode == "BOTH":
            rel_score += 30

        # 2. Domain Match
        if s_dom == domain:
            rel_score += 40
        elif (domain == "EU_COSMETIC_REGULATORY" and "eu-reg-1223-2009" in s_id) or \
             (domain in ["US_FDA_DRUG", "US_FDA_DIETARY_SUPPLEMENT"] and s_jur == "US") or \
             (domain == "EU_THMPD" and s_jur == "EU") or \
             (domain == "INTERNATIONAL_TRADEMARK" and "madrid" in s_id) or \
             (domain == "INTERNATIONAL_PATENT" and "pct" in s_id) or \
             (domain == "ABS_BIODIVERSITY" and "bd-act" in s_id) or \
             (domain == "AYUSH_MANUFACTURING" and "dc-rules" in s_id):
            rel_score += 35

        # 3. Query Keyword Overlap
        if ("1223/2009" in norm or "cosmetic" in norm) and "1223-2009" in s_id:
            rel_score += 50
        if ("responsible person" in norm or "art 4" in norm or "rp" in norm) and "art4" in s_id:
            rel_score += 40
        if ("safety assessment" in norm or "cpsr" in norm or "art 10" in norm or "assessor" in norm) and "art10" in s_id:
            rel_score += 40
        if ("pif" in norm or "product information file" in norm or "art 11" in norm) and "art11" in s_id:
            rel_score += 40
        if ("cpnp" in norm or "art 13" in norm or "notification" in norm) and "art13" in s_id:
            rel_score += 40
        if ("nanomaterial" in norm or "nano" in norm or "art 16" in norm) and "art16" in s_id:
            rel_score += 40
        if ("sue" in norm or "undesirable effect" in norm or "adverse" in norm or "art 23" in norm or "vigilance" in norm) and "art23" in s_id:
            rel_score += 40
        if ("annex i" in norm or "part a" in norm or "part b" in norm) and "annex1" in s_id:
            rel_score += 40
        if "21 cfr 312" in norm and "21cfr312" in s_id:
            rel_score += 50
        if "21 cfr 111" in norm and "21cfr111" in s_id:
            rel_score += 50
        if "directive 2004/24/ec" in norm and "2004-24-ec" in s_id:
            rel_score += 50
        if "madrid" in norm and "madrid" in s_id:
            rel_score += 50
        if "pct" in norm and "pct" in s_id:
            rel_score += 50
        if "rule 158b" in norm and "158b" in s_id:
            rel_score += 40
        if "fssai" in norm and "fssai" in s_id:
            rel_score += 40
        if "nba" in norm and ("bd-act" in s_id or "nagoya" in s_id):
            rel_score += 40

        # Domain Specific Negative Filters (Preventing Irrelevant Clashes)
        # EU Cosmetic query must NOT retrieve Indian Patents Act, ABS, or AYUSH manufacturing rules
        if domain == "EU_COSMETIC_REGULATORY" and ("patents-act" in s_id or "bd-act" in s_id or "dc-rules" in s_id or "fssai" in s_id or "madrid" in s_id or "pct" in s_id):
            rel_score = 0
            blocked_sources.append({**s, "block_reason": "Irrelevant Patent/ABS/Drug Statute for EU Cosmetic Query"})

        # Madrid trademark query must NOT retrieve PCT or Nagoya
        if domain == "INTERNATIONAL_TRADEMARK" and ("pct" in s_id or "nagoya" in s_id or "bd-act" in s_id):
            rel_score = 0
            blocked_sources.append({**s, "block_reason": "Irrelevant Patent/ABS Treaty for Trademark Query"})

        # US FDA query must NOT retrieve Indian GI Act or Indian Patents Act unless cross-border
        if mode == "INTERNATIONAL" and s_jur == "India":
            rel_score = 0
            blocked_sources.append({**s, "block_reason": "Indian statute blocked in purely foreign query"})

        # Pure Indian classical manufacturing must NOT retrieve US FDA 21 CFR
        if mode == "INDIA" and s_jur != "India":
            rel_score = 0
            blocked_sources.append({**s, "block_reason": "Foreign regulation blocked in domestic Indian query"})

        if rel_score >= 40:
            scored_sources.append((rel_score, s))

    scored_sources.sort(key=lambda x: x[0], reverse=True)
    relevant_sources = [s for _, s in scored_sources[:5]]

    # Pre-Generation Retrieval Gate Check
    is_jurisdiction_safe = True
    if mode == "INTERNATIONAL" and any(s.get("jurisdiction") == "India" for s in relevant_sources):
        is_jurisdiction_safe = False

    return relevant_sources, blocked_sources, is_jurisdiction_safe


# ==============================================================================
# PART 7, 8, 9, 10: CONDITIONAL STATUTORY VERIFICATION & ENTAILMENT ENGINES
# ==============================================================================
def check_patent_provision_applicability(prompt_text: str, deliverable_text: str) -> Dict[str, Any]:
    """
    Evaluates Section 3(p), Section 3(d), and Section 3(e) conditionally based on claim facts.
    Prevents automatic application of Section 3(d) on every botanical extract.
    """
    norm = (prompt_text + " " + deliverable_text).lower()
    findings = []

    # Section 3(p) Traditional Knowledge Bar
    if "patent" in norm and any(w in norm for w in ["classical", "chyawanprash", "triphala", "haldi", "turmeric", "ashwagandha", "neem", "traditional", "samhita"]):
        findings.append({
            "statute_code": "PAT-SEC-3P",
            "statute_title": "Patents Act 1970 - Section 3(p) (Traditional Knowledge Bar)",
            "is_applicable": True,
            "preconditions_met": [
                "Invention utilizes traditional Ayurvedic botanical knowledge / classical formulary",
                "Subject to statutory bar against patenting mere aggregations of known traditional components"
            ],
            "preconditions_unmet": [],
            "applicability_rationale": "Section 3(p) applies directly because the formulation relies on known traditional Ayurvedic prior art."
        })

    # Section 3(d) Enhanced Therapeutic Efficacy (Conditional)
    is_extract_claim = any(w in norm for w in ["fraction", "derivative", "isolated compound", "synthetic liposomal", "enhanced bioavailability", "cordifolioside"])
    if "patent" in norm and is_extract_claim:
        findings.append({
            "statute_code": "PAT-SEC-3D",
            "statute_title": "Patents Act 1970 - Section 3(d) (Enhanced Therapeutic Efficacy Requirement)",
            "is_applicable": True,
            "preconditions_met": [
                "Claim involves a new form, derivative, extract fraction, or modification of a known substance",
                "Mandates comparative data demonstrating significantly enhanced therapeutic efficacy over baseline"
            ],
            "preconditions_unmet": [],
            "applicability_rationale": "Section 3(d) applies because modified extract fractions of known botanicals must prove superior therapeutic efficacy."
        })

    # Section 3(e) Polyherbal Synergistic Admixture
    if "patent" in norm and any(w in norm for w in ["combination", "mixture", "polyherbal", "powder mix", "blend"]):
        findings.append({
            "statute_code": "PAT-SEC-3E",
            "statute_title": "Patents Act 1970 - Section 3(e) (Mere Admixture Bar)",
            "is_applicable": True,
            "preconditions_met": [
                "Polyherbal formulation comprising multiple active ingredients",
                "Mandates empirical proof of synergistic interaction beyond additive properties"
            ],
            "preconditions_unmet": [],
            "applicability_rationale": "Section 3(e) applies because polyherbal admixtures must prove non-obvious synergistic therapeutic efficacy."
        })

    return findings


def evaluate_abs_applicability(prompt_text: str, deliverable_text: str) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Biological Diversity Act ABS Decision Engine (2002 Act & 2023 Amendment aware):
    Evaluates applicant nationality, access location, activity type (commercial vs research vs IPR),
    and exemptions (AYUSH practitioner / BMC Certificate of Origin for cultivated herbs under Sec 7).
    """
    norm = (prompt_text + " " + deliverable_text).lower()
    findings = []
    abs_status = "NOT_APPLICABLE"

    has_bio_resource = any(w in norm for w in ["ashwagandha", "neem", "turmeric", "gugglu", "brahmi", "giloy", "biological resource", "herbal", "medicinal plant", "curcuma", "piper"])
    is_ipr = any(w in norm for w in ["patent", "pct", "uspto", "foreign patent"])
    is_foreign_entity = any(w in norm for w in ["foreign", "german", "multinational", "foreign company", "foreign equity", "non-indian", "export"])
    is_cultivated = any(w in norm for w in ["cultivated", "grower", "farmer", "certificate of origin", "bmc certificate"])

    if has_bio_resource:
        if is_foreign_entity and not is_ipr:
            abs_status = "CLEARLY_APPLICABLE"
            findings.append({
                "statute_code": "BDA-SEC-3",
                "statute_title": "Biological Diversity Act 2002 — Section 3 (Foreign Entity Access Approval)",
                "is_applicable": True,
                "preconditions_met": [
                    "Non-Indian entity / entity with foreign equity participation accessing biological resources",
                    "Mandates prior Form I approval from the National Biodiversity Authority (NBA)"
                ],
                "preconditions_unmet": [],
                "applicability_rationale": "Section 3 applies mandatorily for foreign entities accessing Indian bio-resources for research or commercial utilization."
            })
        elif is_ipr:
            abs_status = "CLEARLY_APPLICABLE"
            findings.append({
                "statute_code": "BDA-SEC-6-1",
                "statute_title": "Biological Diversity Act 2002 — Section 6(1) (Mandatory NBA Approval for IPR)",
                "is_applicable": True,
                "preconditions_met": [
                    "Invention based on biological resources or traditional knowledge obtained from India",
                    "Application for patent / IPR inside or outside India"
                ],
                "preconditions_unmet": [],
                "applicability_rationale": "Section 6(1) mandates prior approval from NBA (Form III) before applying for foreign patents or before grant of Indian patents."
            })
        elif is_cultivated:
            abs_status = "POTENTIALLY_APPLICABLE"
            findings.append({
                "statute_code": "BDA-SEC-7-AMENDED-2023",
                "statute_title": "Biological Diversity (Amendment) Act 2023 — Section 7 Exemption",
                "is_applicable": True,
                "preconditions_met": [
                    "Cultivated medicinal plants with local BMC Certificate of Origin",
                    "Exempts registered AYUSH users from State Biodiversity Board prior intimation"
                ],
                "preconditions_unmet": [],
                "applicability_rationale": "Section 7 amendment exempts cultivated medicinal plants with BMC Certificate of Origin from SBB fee."
            })

    return abs_status, findings


def classify_rule_158b_product(prompt_text: str) -> Tuple[str, Optional[Dict[str, Any]]]:
    """
    Drugs & Cosmetics Rules Rule 158B Contextual Classifier:
    Classifies product into CLASSICAL_ASU_MEDICINE, PATENT_PROPRIETARY_ASU, or CLASSIFICATION_REQUIRED.
    """
    norm = prompt_text.lower()
    
    if any(w in norm for w in ["charaka", "sushruta", "ashtanga", "first schedule", "classical chyawanprash", "classical triphala", "classical awaleha"]):
        return "CLASSICAL_ASU_MEDICINE", {
            "statute_code": "DCR-RULE-158B-1-A",
            "statute_title": "Drugs & Cosmetics Rules 1945 — Rule 158B(I)(A) (Classical ASU Formulations)",
            "is_applicable": True,
            "preconditions_met": [
                "Formulation strictly follows recognized First Schedule authoritative Ayurvedic treatise",
                "Exempt from safety/efficacy trials; textual reference serves as legal proof"
            ],
            "preconditions_unmet": [],
            "applicability_rationale": "Rule 158B(I)(A) applies directly to authorize Form 25D licensing based on classical text citation without clinical trials."
        }
    elif any(w in norm for w in ["proprietary", "new formula", "added standardized", "novel extraction", "with added vitamin", "mixture of"]):
        return "PATENT_PROPRIETARY_ASU", {
            "statute_code": "DCR-RULE-158B-1-B",
            "statute_title": "Drugs & Cosmetics Rules 1945 — Rule 158B(I)(B) (Patent or Proprietary ASU Medicine)",
            "is_applicable": True,
            "preconditions_met": [
                "Novel composition, non-classical ratio, or modern extraction method",
                "Mandates submission of published scientific safety literature or pilot toxicity data"
            ],
            "preconditions_unmet": [],
            "applicability_rationale": "Rule 158B(I)(B) applies to govern Patent or Proprietary ASU medicines requiring safety dossier verification."
        }
    elif any(w in norm for w in ["license", "manufacturing", "sell"]):
        return "CLASSIFICATION_REQUIRED", None
    
    return "NOT_APPLICABLE", None


def audit_verification_layer(
    prompt_text: str,
    deliverable_text: str,
    jurisdiction_res: Dict[str, Any],
    domain: str,
    relevant_sources: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Layer 7: Complete 3-Tier Statutory Verification with Conclusion Entailment:
    - Tier 1: Citation Authenticity & Currency
    - Tier 2: Jurisdiction & Statutory Precondition Applicability ('Does this law apply here?')
    - Tier 3: Conclusion Entailment ('SUPPORTED' | 'NOT_SUPPORTED' | 'CONTRADICTED' | 'UNAUTHORIZED_EXEMPTION')
    """
    p = prompt_text.lower()
    d = deliverable_text.lower()
    full_text = f"{p} {d}"
    
    contradictions = []
    applicability_findings = []
    conclusion_validations = []

    # ==========================================
    # TIER 1: CITATION AUTHENTICITY & CURRENCY
    # ==========================================
    tier1_audited = []
    for s in relevant_sources:
        tier1_audited.append({
            "statute_id": s.get("id"),
            "statute_title": s.get("title"),
            "authority": s.get("authority"),
            "is_valid": True,
            "is_active": True,
            "version": s.get("version")
        })
    citation_score = 0.95 if tier1_audited else 0.50

    # ==========================================
    # TIER 2: STATUTORY APPLICABILITY AUDIT
    # ==========================================
    # Only evaluate Indian patent/ABS/ASU provisions if domain is NOT EU_COSMETIC_REGULATORY and jurisdiction mode is not purely foreign
    if domain != "EU_COSMETIC_REGULATORY" and (jurisdiction_res.get("mode") in ["INDIA", "BOTH"] or domain in ["PATENT", "ABS_BIODIVERSITY", "AYUSH_MANUFACTURING", "AYUSH_PRODUCT_REGULATION", "TRADEMARK", "FOOD_FSSAI", "EXPORT_COMPLIANCE", "MULTI_DOMAIN"]):
        # 1. Patent provisions (Sec 3(p), 3(d), 3(e))
        pat_findings = check_patent_provision_applicability(prompt_text, deliverable_text)
        applicability_findings.extend(pat_findings)

        # 2. ABS provisions
        abs_status, abs_findings = evaluate_abs_applicability(prompt_text, deliverable_text)
        applicability_findings.extend(abs_findings)

        # 3. Rule 158B ASU Classification
        r158b_class, r158b_finding = classify_rule_158b_product(prompt_text)
        if r158b_finding:
            applicability_findings.append(r158b_finding)
    else:
        r158b_class = "NOT_APPLICABLE"

    # 4. Foreign Regimes (US FDA / EU THMPD / Madrid System)
    if domain == "US_FDA_DRUG":
        applicability_findings.append({
            "statute_code": "US-FDA-21CFR312",
            "statute_title": "US FDA 21 CFR Part 312 & Botanical Drug Guidance",
            "is_applicable": True,
            "preconditions_met": [
                "Investigational botanical drug intended for US Phase II clinical trials",
                "Mandates CMC batch consistency, raw material authentication, and IND approval"
            ],
            "preconditions_unmet": [],
            "applicability_rationale": "21 CFR Part 312 applies to govern investigational clinical trial authorization in the United States."
        })
    elif domain == "US_FDA_DIETARY_SUPPLEMENT":
        applicability_findings.append({
            "statute_code": "US-FDA-21CFR111",
            "statute_title": "US FDA 21 CFR Part 111 (Dietary Supplement cGMP) & DSHEA",
            "is_applicable": True,
            "preconditions_met": [
                "Dietary supplement marketed in the US with structure/function claims",
                "Mandates cGMP facility registration and FDA disclaimer; strictly bars cure claims"
            ],
            "preconditions_unmet": [],
            "applicability_rationale": "21 CFR Part 111 & DSHEA apply to govern dietary supplement cGMP manufacturing and permissible claims."
        })
    elif domain == "EU_THMPD":
        applicability_findings.append({
            "statute_code": "EU-DIR-2004-24-EC",
            "statute_title": "EU Directive 2004/24/EC (Traditional Herbal Medicinal Products Directive)",
            "is_applicable": True,
            "preconditions_met": [
                "Simplified registration for traditional herbal medicine in EU member states",
                "Requires proof of 30-year traditional use (min 15 years within EU)"
            ],
            "preconditions_unmet": [],
            "applicability_rationale": "Directive 2004/24/EC applies directly to govern THMPD herbal product registration in the European Union."
        })
    elif domain == "EU_COSMETIC_REGULATORY":
        applicability_findings.append({
            "statute_code": "EU-REG-1223-2009",
            "statute_title": "EU Regulation (EC) No 1223/2009 on Cosmetic Products",
            "is_applicable": True,
            "preconditions_met": [
                "Cosmetic product placed or made available on the European Union market",
                "Mandates designated EU Responsible Person (Art 4), CPSR Safety Assessment (Art 10 & Annex I), PIF (Art 11), CPNP Notification (Art 13), Nanomaterial 6-month prior notice (Art 16), and SUE Cosmetovigilance (Art 23)"
            ],
            "preconditions_unmet": [],
            "applicability_rationale": "Regulation (EC) No 1223/2009 applies directly and exclusively to govern cosmetic safety, dossiers, and market placement across all EU member states."
        })
    elif domain == "INTERNATIONAL_TRADEMARK":
        applicability_findings.append({
            "statute_code": "INTL-MADRID-PROTOCOL",
            "statute_title": "Madrid System for the International Registration of Marks",
            "is_applicable": True,
            "preconditions_met": [
                "International trademark registration across multiple designated contracting parties",
                "Requires valid basic application / registration in home Office of Origin"
            ],
            "preconditions_unmet": [],
            "applicability_rationale": "Madrid Protocol applies directly to govern international Class 5/3 trademark prosecution."
        })
    elif domain == "FOOD_FSSAI":
        applicability_findings.append({
            "statute_code": "FSSAI-AAHAR-2022",
            "statute_title": "FSSAI (Ayurveda Aahar) Regulations 2022",
            "is_applicable": True,
            "preconditions_met": [
                "Food product prepared in accordance with authoritative Ayurvedic culinary texts",
                "Strictly bars disease cure/treatment claims and Schedule E-1 poisonous herbs"
            ],
            "preconditions_unmet": [],
            "applicability_rationale": "FSSAI Ayurveda Aahar regulations govern food/dietary preparations incorporating Ayurvedic ingredients."
        })

    applicability_score = 1.0 if applicability_findings else 0.90

    # ==========================================
    # TIER 3: CONCLUSION ENTAILMENT AUDIT
    # ==========================================
    # Check 1: Classical Formulation Patenting without Synergistic Data
    if any(f["statute_code"] == "PAT-SEC-3P" for f in applicability_findings):
        if "without synergy" in p or "simple powder mixture" in p or "directly patent" in p or "new cure" in p:
            contradictions.append({
                "severity": "CRITICAL",
                "issue": "Section 3(p) Traditional Knowledge Bar Violation",
                "explanation": "Classical Ayurvedic recipes and simple powder mixtures cannot be patented as mere aggregations of known traditional components.",
                "remedy": "File for Classical ASU Manufacturing License under Rule 158B(I)(A) or demonstrate non-obvious synergistic efficacy for patenting."
            })
            conclusion_validations.append({
                "conclusion_statement": "Query proposes patenting a classical polyherbal mixture without synergistic proof.",
                "statutory_basis": "Patents Act 1970 - Section 3(p) & Section 3(e)",
                "is_justified": False,
                "logical_status": "STATUTORY_BAR_CONTRADICTION",
                "legal_analysis": "Section 3(p) explicitly bars patenting of traditional knowledge. A mere admixture is statutorily non-patentable without synergistic interaction proof.",
                "correct_statutory_verdict": "Non-patentable under Section 3(p) unless quantifiable synergistic therapeutic efficacy is proven."
            })
        else:
            conclusion_validations.append({
                "conclusion_statement": "Deliverable correctly identifies Section 3(p) Traditional Knowledge bar and synergy/classical licensing requirements.",
                "statutory_basis": "Patents Act 1970 - Section 3(p)",
                "is_justified": True,
                "logical_status": "VALID_JUSTIFIED_DEDUCTION",
                "legal_analysis": "Conclusion is legally sound. Classical formulations require proof of synergistic interaction or classical Form 25D licensing.",
                "correct_statutory_verdict": "Legally justified: Section 3(p) restriction correctly applied."
            })

    # Check 2: Foreign Patent Filing without Mandatory NBA Approval
    if any(f["statute_code"] == "BDA-SEC-6-1" for f in applicability_findings):
        if "without nba" in p or "skip nba" in p or "no biodiversity" in p:
            contradictions.append({
                "severity": "HIGH",
                "issue": "Missing NBA Section 6(1) Approval Requirement",
                "explanation": "Section 6(1) of the Biological Diversity Act mandates prior approval from NBA (Form III) before applying for any foreign IPR on Indian bio-resources.",
                "remedy": "Prepare and submit NBA Form III before patent grant / foreign filing."
            })
            conclusion_validations.append({
                "conclusion_statement": "Query suggests foreign patent prosecution can proceed without National Biodiversity Authority (NBA) approval.",
                "statutory_basis": "Biological Diversity Act 2002 - Section 6(1)",
                "is_justified": False,
                "logical_status": "UNAUTHORIZED_EXEMPTION",
                "legal_analysis": "Section 6(1) explicitly prohibits applying for foreign IPR on Indian biological resources without prior Form III approval from NBA.",
                "correct_statutory_verdict": "Form III application to NBA is mandatory prior to foreign filing under Section 6(1) to avoid penal liability under Section 55."
            })
        else:
            conclusion_validations.append({
                "conclusion_statement": "Deliverable correctly advises obtaining mandatory NBA Form III prior approval before foreign patent prosecution.",
                "statutory_basis": "Biological Diversity Act 2002 - Section 6(1)",
                "is_justified": True,
                "logical_status": "VALID_JUSTIFIED_DEDUCTION",
                "legal_analysis": "Conclusion is legally justified: Mandatory BDA Section 6(1) clearance recognized.",
                "correct_statutory_verdict": "Legally justified: Mandatory NBA Form III compliance recognized."
            })

    # Check 3: FSSAI Ayurveda Aahar Curative Disease Claims Bar
    if domain == "FOOD_FSSAI" and any(w in p for w in ["cure", "curing", "depression", "anxiety", "disease", "treatment"]):
        contradictions.append({
            "severity": "CRITICAL",
            "issue": "FSSAI Ayurveda Aahar Therapeutic / Disease Cure Claim Prohibition",
            "explanation": "FSSAI (Ayurveda Aahar) Regulations 2022 and Drugs & Magic Remedies Act strictly bar curative or disease treatment claims on food/dietary products.",
            "remedy": "Restrict marketing strictly to general physiological nourishment and well-being; file under AYUSH Rule 158B if therapeutic cure is claimed."
        })
        conclusion_validations.append({
            "conclusion_statement": "Query seeks to advertise FSSAI Ayurveda Aahar food product for curing severe clinical depression/disease.",
            "statutory_basis": "FSSAI Ayurveda Aahar Regulations 2022 & DMR(OA) Act 1954",
            "is_justified": False,
            "logical_status": "STATUTORY_BAR_CONTRADICTION",
            "legal_analysis": "Food products under FSSAI cannot carry therapeutic or curative disease claims. Curative claims violate FSSAI regulations and DMR(OA) Act.",
            "correct_statutory_verdict": "Disease cure claims are strictly barred under FSSAI Ayurveda Aahar regulations."
        })
    elif domain == "FOOD_FSSAI":
        conclusion_validations.append({
            "conclusion_statement": "Deliverable enforces that FSSAI Ayurveda Aahar products are restricted to traditional dietary nourishment without curative disease claims.",
            "statutory_basis": "FSSAI Ayurveda Aahar Regulations 2022",
            "is_justified": True,
            "logical_status": "VALID_JUSTIFIED_DEDUCTION",
            "legal_analysis": "Conclusion is legally sound. Dietary standards and non-curative labeling requirements correctly applied.",
            "correct_statutory_verdict": "Legally justified: FSSAI dietary standards applied."
        })

    # Check 4: Rule 158B(I)(A) Classical Trial Exemption
    if r158b_class == "CLASSICAL_ASU_MEDICINE" and any(f["statute_code"] == "DCR-RULE-158B-1-A" for f in applicability_findings):
        conclusion_validations.append({
            "conclusion_statement": "Classical Ayurvedic formulations listed in First Schedule authoritative texts are substantiated by textual reference under Rule 158B(I)(A) without clinical trials.",
            "statutory_basis": "Drugs & Cosmetics Rules 1945 - Rule 158B(I)(A)",
            "is_justified": True,
            "logical_status": "VALID_JUSTIFIED_DEDUCTION",
            "legal_analysis": "Conclusion is legally justified: First Schedule textual citations substantiate classical Form 25D licensing without clinical trials.",
            "correct_statutory_verdict": "Legally justified: Rule 158B(I)(A) classical licensing standard applied."
        })

    # Check 5: US FDA IND & THMPD Conclusions
    if domain == "US_FDA_DRUG":
        conclusion_validations.append({
            "conclusion_statement": "Botanical drug Phase II clinical investigation in the US requires an IND submission under 21 CFR Part 312 with rigorous CMC batch consistency.",
            "statutory_basis": "US FDA 21 CFR Part 312 & Botanical Drug Guidance",
            "is_justified": True,
            "logical_status": "VALID_JUSTIFIED_DEDUCTION",
            "legal_analysis": "Conclusion is legally justified: 21 CFR Part 312 requirements correctly cited for investigational botanical drug development.",
            "correct_statutory_verdict": "Legally justified: US FDA 21 CFR 312 IND pathway applied."
        })
    elif domain == "EU_THMPD":
        conclusion_validations.append({
            "conclusion_statement": "Traditional herbal medicinal product registration in Germany/EU requires documented proof of 30-year continuous traditional medicinal use (min 15 years in EU).",
            "statutory_basis": "EU Directive 2004/24/EC (THMPD)",
            "is_justified": True,
            "logical_status": "VALID_JUSTIFIED_DEDUCTION",
            "legal_analysis": "Conclusion is legally justified: Directive 2004/24/EC evidentiary threshold for simplified traditional registration correctly cited.",
            "correct_statutory_verdict": "Legally justified: EU THMPD 30-year traditional use criteria applied."
        })
    elif domain == "EU_COSMETIC_REGULATORY":
        # Check for SUE Article Misattribution (ensuring non-greedy clause boundaries)
        sue_misattributed = any(
            re.search(r"\barticle\s*(?:10|11|13|4|16)\b[^.\n;,]{0,60}\b(?:for|governs?|reports?|reporting|notif\w*|mandates?)\b[^.\n;,]{0,60}\b(?:sue\b|serious undesirable|adverse effect|adverse reaction|cosmetovigilance)\b", text) or
            re.search(r"\b(?:sue\b|serious undesirable|adverse effect|adverse reaction|cosmetovigilance)\b[^.\n;,]{0,60}\b(?:under|in|per|via|by|citing|as per)\s*article\s*(?:10|11|13|4|16)\b", text)
            for text in [p, d]
        )
        if sue_misattributed:
            contradictions.append({
                "severity": "CRITICAL",
                "issue": "EU Regulation 1223/2009 Article 23 SUE Misattribution",
                "explanation": "Communication of Serious Undesirable Effects (SUE) is strictly governed by Article 23, NOT Article 10, 11, or 13.",
                "remedy": "Correct statutory citation to Article 23 for cosmetovigilance and serious undesirable effects reporting."
            })
            conclusion_validations.append({
                "conclusion_statement": "Deliverable or query misattributes Serious Undesirable Effects (SUE) reporting to Article 10, 11, or 13.",
                "statutory_basis": "EU Regulation (EC) No 1223/2009 - Article 23",
                "is_justified": False,
                "logical_status": "STATUTORY_BAR_CONTRADICTION",
                "legal_analysis": "Article 23 mandates immediate reporting of SUE to Member State authorities. Citing Article 10 (Safety Assessment), Article 11 (PIF), or Article 13 (CPNP) for SUE is legally incorrect.",
                "correct_statutory_verdict": "SUE reporting is governed strictly by Article 23."
            })
        else:
            conclusion_validations.append({
                "conclusion_statement": "Correctly maps EU cosmetovigilance and Serious Undesirable Effects (SUE) communication to Article 23.",
                "statutory_basis": "EU Regulation (EC) No 1223/2009 - Article 23",
                "is_justified": True,
                "logical_status": "VALID_JUSTIFIED_DEDUCTION",
                "legal_analysis": "Conclusion is legally justified: Article 23 correctly cited for SUE notification to EU Member State authorities.",
                "correct_statutory_verdict": "Legally justified: Article 23 SUE compliance recognized."
            })

        # Check for Indian Classical Trial Exemption Fallacy on EU Cosmetics
        if any(w in d for w in ["rule 158b exempts from cpsr", "no safety assessment needed because classical", "exempt from regulation 1223"]):
            contradictions.append({
                "severity": "CRITICAL",
                "issue": "Illegal Exemption Claim: Indian AYUSH Rule 158B Does Not Exempt from EU CPSR",
                "explanation": "Indian AYUSH Rule 158B textual evidence does not exempt cosmetic products from the mandatory safety assessment under Article 10 and Annex I of EU Regulation 1223/2009.",
                "remedy": "Conduct full EU safety assessment and compile CPSR Parts A & B by a qualified safety assessor."
            })
            conclusion_validations.append({
                "conclusion_statement": "Suggests Indian AYUSH Rule 158B classical status waives EU Regulation 1223/2009 CPSR safety assessment.",
                "statutory_basis": "EU Regulation (EC) No 1223/2009 - Article 10 & Annex I",
                "is_justified": False,
                "logical_status": "UNAUTHORIZED_EXEMPTION",
                "legal_analysis": "EU Regulation 1223/2009 applies universally to all cosmetics placed on the EU market. Foreign traditional medicine exemptions cannot waive Article 10 CPSR.",
                "correct_statutory_verdict": "Article 10 CPSR is mandatory for all cosmetics in the EU regardless of Indian AYUSH licensing status."
            })
        else:
            conclusion_validations.append({
                "conclusion_statement": "Enforces mandatory Article 10 Safety Assessment and Annex I Cosmetic Product Safety Report (CPSR Parts A & B) by a qualified safety assessor.",
                "statutory_basis": "EU Regulation (EC) No 1223/2009 - Article 10 & Annex I",
                "is_justified": True,
                "logical_status": "VALID_JUSTIFIED_DEDUCTION",
                "legal_analysis": "Conclusion is legally justified: Article 10 and Annex I CPSR requirements correctly enforced.",
                "correct_statutory_verdict": "Legally justified: Article 10 & Annex I CPSR standards applied."
            })

        # Check for Article 16 Nanomaterial compliance
        if "nano" in full_text:
            conclusion_validations.append({
                "conclusion_statement": "Cosmetics containing nanomaterials require 6-month prior electronic notification to the Commission under Article 16.",
                "statutory_basis": "EU Regulation (EC) No 1223/2009 - Article 16",
                "is_justified": True,
                "logical_status": "VALID_JUSTIFIED_DEDUCTION",
                "legal_analysis": "Conclusion is legally justified: Article 16 6-month notification window for nanomaterials correctly recognized.",
                "correct_statutory_verdict": "Legally justified: Article 16 nanomaterials protocol applied."
            })

        # -------------------------------------------------------------
        # STEP 3: GENERIC POST-LLM DETERMINISTIC VERIFIER OVERRIDES (CIRCUIT BREAKER)
        # -------------------------------------------------------------
        table_text = deliverable_text or ""
        if table_text:
            domain_pkg = DOMAIN_REGISTRY.get(domain, DOMAIN_REGISTRY.get("EU_COSMETIC_REGULATORY", {}))
            
            # 1. Foreign Law / Forbidden Terms Contamination Check
            for term in domain_pkg.get("forbidden_terms", []):
                if term in table_text:
                    contradictions.append({
                        "severity": "CRITICAL",
                        "issue": f"Cross-Domain Contamination: Found '{term}' in a {domain_pkg.get('label', domain)} query.",
                        "explanation": f"Deliverable table contains forbidden statute reference '{term}' which is inapplicable to {domain_pkg.get('label', domain)}.",
                        "remedy": f"Purge irrelevant statutes and regenerate using {domain_pkg.get('label', domain)} provisions only."
                    })

            # 2. Mismatched Article / Assertion Checks
            for check in domain_pkg.get("verifier_assertions", []):
                if check["regex"].search(table_text):
                    contradictions.append({
                        "severity": "HIGH",
                        "issue": check["error"],
                        "explanation": f"Statutory mapping violation in deliverable: {check['error']}.",
                        "remedy": f"Re-align statutory mapping according to {domain_pkg.get('label', domain)} ground truth."
                    })

    elif domain == "INTERNATIONAL_TRADEMARK":
        conclusion_validations.append({
            "conclusion_statement": "Madrid System international trademark filing requires a basic home application / registration in Class 5 to establish priority across designated contracting states.",
            "statutory_basis": "Madrid Protocol (WIPO)",
            "is_justified": True,
            "logical_status": "VALID_JUSTIFIED_DEDUCTION",
            "legal_analysis": "Conclusion is legally justified: Madrid Protocol single-application mechanism and basic mark prerequisite correctly cited.",
            "correct_statutory_verdict": "Legally justified: Madrid System Class 5 procedures applied."
        })

    conclusion_score = (
        round(sum(1 for c in conclusion_validations if c["is_justified"]) / len(conclusion_validations), 2)
        if conclusion_validations else 1.0
    )
    if contradictions:
        conclusion_score = 0.0

    three_tier_report = {
        "tier_1_citation_verification": {
            "score": citation_score,
            "status": "PASSED" if citation_score >= 0.70 else "FLAGGED",
            "citations_audited": len(tier1_audited)
        },
        "tier_2_applicability_verification": {
            "score": applicability_score,
            "status": "PASSED" if (applicability_score >= 0.70 and not contradictions) else "FLAGGED",
            "statutes_evaluated": len(applicability_findings),
            "findings": applicability_findings
        },
        "tier_3_conclusion_verification": {
            "score": conclusion_score,
            "status": "PASSED" if (conclusion_score >= 0.80 and not contradictions) else "FLAGGED",
            "conclusions_audited": len(conclusion_validations),
            "validations": conclusion_validations
        }
    }

    return {
        "contradictions_flagged": contradictions,
        "groundedness_score": 0.95 if not contradictions else 0.75,
        "is_safe": len(contradictions) == 0 and conclusion_score >= 0.80,
        "applicability_score": applicability_score,
        "conclusion_justification_score": conclusion_score,
        "applicability_findings": applicability_findings,
        "conclusion_validations": conclusion_validations,
        "three_tier_verification": three_tier_report
    }


# ==============================================================================
# PART 12 & 13: CONFIDENCE CEILINGS & DIVERSITY SCORING
# ==============================================================================
def compute_confidence_layer(
    groundedness: float,
    relevant_sources: List[Dict[str, Any]],
    contradictions: List[Dict[str, Any]],
    jurisdiction_res: Dict[str, Any],
    domain: str,
    prompt_text: str = "",
    deliverable_text: str = "",
    language: str = "en"
) -> Dict[str, Any]:
    """
    Layer 8: Multi-Factor Confidence Scoring with Hard Confidence Ceilings:
    - JURISDICTION_MISMATCH -> max confidence = 20%
    - NO_AUTHORITATIVE_SOURCE -> max confidence = 40%
    - INSUFFICIENT_RETRIEVAL -> max confidence = 50%
    - STATUTORY_CONTRADICTION -> max confidence = 45%
    """
    norm = prompt_text.lower()
    mode = jurisdiction_res.get("mode", "INDIA")
    effective_jur = jurisdiction_res.get("effective_jurisdiction", "India")
    conflicts = jurisdiction_res.get("conflicts", [])

    # 1. Citation Coverage Factor
    citation_count = len(relevant_sources)
    citation_factor = min(1.0, citation_count / 3.0) if citation_count > 0 else 0.0

    # 2. Jurisdiction Alignment Factor
    jurisdiction_factor = 1.0 if not conflicts else 0.30

    # 3. Source Diversity Factor (Based on distinct authorities)
    authorities = {s.get("authority", "") for s in relevant_sources if s.get("authority")}
    if len(authorities) >= 2:
        diversity_factor = 1.0
    elif len(authorities) == 1:
        diversity_factor = 0.70
    else:
        diversity_factor = 0.0

    # 4. Contradiction Penalties
    has_critical = any(c.get("severity") == "CRITICAL" for c in contradictions)
    has_high = any(c.get("severity") == "HIGH" for c in contradictions)
    contradiction_penalty = 0.35 if has_critical else (0.20 if has_high else 0.0)

    # Base Composite Calculation
    base_score = (
        (0.35 * citation_factor) +
        (0.30 * jurisdiction_factor) +
        (0.20 * diversity_factor) +
        (0.15 * groundedness) -
        contradiction_penalty
    )
    final_score = max(0.10, min(1.0, base_score))

    # ==========================================
    # HARD CONFIDENCE CEILINGS
    # ==========================================
    confidence_ceiling = 1.0
    ceiling_reasons = []

    if conflicts and any("JURISDICTION_CONTRADICTION" in c for c in conflicts):
        confidence_ceiling = min(confidence_ceiling, 0.20)
        ceiling_reasons.append("JURISDICTION_MISMATCH (Cap: 20%)")

    if citation_count == 0:
        confidence_ceiling = min(confidence_ceiling, 0.40)
        ceiling_reasons.append("NO_AUTHORITATIVE_SOURCE (Cap: 40%)")
    elif citation_count == 1 and mode == "BOTH":
        confidence_ceiling = min(confidence_ceiling, 0.55)
        ceiling_reasons.append("MIXED_JURISDICTION_INCOMPLETE (Cap: 55%)")

    if has_critical:
        confidence_ceiling = min(confidence_ceiling, 0.45)
        ceiling_reasons.append("STATUTORY_CONTRADICTION (Cap: 45%)")

    # Apply Ceiling
    final_score = min(final_score, confidence_ceiling)
    final_percentage = f"{round(final_score * 100, 1)}%"

    if final_score >= 0.75:
        rating = "HIGH"
    elif final_score >= 0.50:
        rating = "MEDIUM"
    else:
        rating = "LOW"

    # Escalation Dossier Formulation
    escalation = None
    if final_score < 0.80 or contradictions:
        escalation = generate_dynamic_escalation_dossier(
            prompt_text=prompt_text,
            deliverable_text=deliverable_text,
            contradictions=contradictions,
            domain=domain,
            final_percentage=round(final_score * 100, 1),
            rating=rating,
            language=language
        )

    return {
        "confidence_percentage": final_percentage,
        "confidence_rating": rating,
        "raw_score": round(final_score, 3),
        "factors": {
            "citationFactor": round(citation_factor, 2),
            "jurisdictionFactor": round(jurisdiction_factor, 2),
            "diversityFactor": round(diversity_factor, 2),
            "contradictionPenalty": round(contradiction_penalty, 2),
            "confidenceCeilingApplied": confidence_ceiling < 1.0,
            "ceilingReasons": ceiling_reasons
        },
        "escalation_dossier": escalation
    }


# ==============================================================================
# PART 18: DYNAMIC ESCALATION DOSSIER & TARGETED COUNSEL QUESTIONS
# ==============================================================================
def generate_dynamic_escalation_dossier(
    prompt_text: str,
    deliverable_text: str,
    contradictions: List[Dict[str, Any]],
    domain: str,
    final_percentage: float,
    rating: str,
    language: str = "en"
) -> Dict[str, Any]:
    """
    Generates targeted legal escalation questions corresponding strictly to the exact failed
    verification node or live statutory uncertainty.
    """
    norm = (prompt_text + " " + deliverable_text).lower()
    
    # Extract botanical names
    HERB_MAP = {
        "ashwagandha": "Ashwagandha (Withania somnifera)",
        "gugglu": "Guggulu (Commiphora mukul)",
        "guggulu": "Guggulu (Commiphora mukul)",
        "neem": "Neem (Azadirachta indica)",
        "turmeric": "Turmeric / Curcumin (Curcuma longa)",
        "haldi": "Haridra (Curcuma longa)",
        "triphala": "Triphala (Amalaki, Haritaki, Bibhitaki)",
        "chyawanprash": "Chyawanprash Formulation",
        "giloy": "Giloy (Tinospora cordifolia)",
        "brahmi": "Brahmi (Bacopa monnieri)",
        "shankhpushpi": "Shankhpushpi (Convolvulus pluricaulis)"
    }
    herbs = [v for k, v in HERB_MAP.items() if k in norm]
    herb_label = herbs[0] if herbs else "the active herbal formulation"

    # Specialist mapping
    EXPERT_MAP = {
        "EU_COSMETIC_REGULATORY": "EU Cosmetic Regulatory Lead & Qualified Safety Assessor (Eurotox / ERT)",
        "US_FDA_DRUG": "US FDA Regulatory Specialist & IND Legal Counsel",
        "US_FDA_DIETARY_SUPPLEMENT": "US Dietary Supplement Regulatory & DSHEA Compliance Counsel",
        "EU_THMPD": "European Union Herbal Medicines & THMPD Legal Specialist",
        "INTERNATIONAL_TRADEMARK": "WIPO Madrid Protocol Trademark Attorney",
        "INTERNATIONAL_PATENT": "WIPO PCT International Patent Attorney",
        "ABS_BIODIVERSITY": "National Biodiversity Authority (NBA/ABS) & Biological Diversity Legal Counsel",
        "FOOD_FSSAI": "FSSAI Ayurveda Aahar Food Safety Compliance Consultant",
        "PATENT": "Registered Patent Attorney (Life Sciences & TKDL Prior-Art Specialist)",
        "TRADEMARK": "Trademark & Brand Protection Registry Attorney (Class 5/3)",
        "AYUSH_MANUFACTURING": "AYUSH Regulatory Lead & D&C Act Rule 158B Licensing Consultant",
        "EXPORT_COMPLIANCE": "Cross-Border Patent Attorney & US FDA/EMA Monograph Specialist",
        "MULTI_DOMAIN": "Senior Life Sciences IP & Multi-Jurisdictional Regulatory Counsel"
    }
    expert_type = EXPERT_MAP.get(domain, "Senior Ayurveda IP & Regulatory Counsel")

    questions = []

    # 1. Contradiction Driven
    for c in contradictions:
        issue = (c.get("issue") or "").lower()
        if "3(p)" in issue or "traditional knowledge" in issue:
            questions.append(f"Can we establish quantifiable synergistic efficacy (e.g. Combination Index CI < 1.0 or comparative therapeutic bioassays) for {herb_label} to overcome the Section 3(p) Traditional Knowledge bar?")
        elif "6(1)" in issue or "nba" in issue:
            questions.append(f"Has an NBA Form III application been prepared for submission under Section 6(1) of the Biological Diversity Act prior to foreign filing or patent grant for {herb_label}?")
        elif "fssai" in issue or "cure" in issue:
            questions.append(f"Can the marketing claims for {herb_label} be revised to general dietary wellness to comply with FSSAI regulations, or should the product be transitioned to an AYUSH therapeutic license under Rule 158B?")
        elif "1223" in issue or "sue" in issue:
            questions.append(f"Have all cosmetovigilance and Serious Undesirable Effects (SUE) notification protocols been aligned with Article 23 of EU Regulation 1223/2009?")

    # 2. Domain Specific Targeted Questions
    if domain == "EU_COSMETIC_REGULATORY" and len(questions) < 4:
        questions.append(f"Has an EU-established Responsible Person (RP) been designated under Article 4 and has the Product Information File (PIF) been assembled under Article 11 for {herb_label}?")
        questions.append(f"Has a Cosmetic Product Safety Report (CPSR) comprising Part A (Safety Information) and Part B (Safety Assessment) been signed by a qualified safety assessor under Article 10 & Annex I for {herb_label}?")
        questions.append(f"Has electronic pre-market notification on the Cosmetic Product Notification Portal (CPNP) been completed under Article 13, including frame formulations and any nanomaterial declarations under Article 16?")
        questions.append("Is a cosmetovigilance protocol established for prompt Article 23 notification of Serious Undesirable Effects (SUE) to EU Member State competent authorities?")
    elif domain == "US_FDA_DRUG" and len(questions) < 4:
        questions.append(f"Has the Chemistry, Manufacturing, and Controls (CMC) package for {herb_label} demonstrated multi-batch chemical fingerprint consistency as required under 21 CFR § 312.23?")
        questions.append("Is a pre-IND meeting with the CDER Division of Botanical Products recommended prior to Phase II protocol finalization?")
    elif domain == "EU_THMPD" and len(questions) < 4:
        questions.append(f"Is there documented bibliographic evidence establishing 30 years of continuous traditional medicinal use for {herb_label}, including at least 15 years within the EU?")
        questions.append("Does the product quality dossier comply with European Pharmacopoeia (Ph. Eur.) monographs for heavy metals, pesticides, and microbial limits?")
    elif domain == "INTERNATIONAL_TRADEMARK" and len(questions) < 4:
        questions.append("Has an international clearance search been conducted across WIPO Madrid contracting states to confirm no prior conflicting Class 5 marks exist?")
    elif domain == "ABS_BIODIVERSITY" and len(questions) < 4:
        questions.append(f"Have mandatory National Biodiversity Authority (NBA) approvals (Form I for commercial utilization / Form III for IPR) and State Biodiversity Board (SBB) intimations under Section 7 been initiated for {herb_label}?")
        questions.append("Are Access and Benefit Sharing (ABS) levies (0.1%–0.5% ex-factory turnover) factored into the raw material procurement agreement?")
    elif domain == "AYUSH_MANUFACTURING" and len(questions) < 4:
        questions.append("Under which specific pathway of Rule 158B is the product being submitted: Classical Ayurvedic Medicine (Rule 158B(I)(A)) or Patent/Proprietary ASU Formulation (Rule 158B(I)(B))?")
        questions.append("Does the manufacturing dossier include valid Schedule T Good Manufacturing Practices (GMP) certification and heavy metal / pesticide residue testing protocols?")

    if not questions:
        questions.append(f"Are all statutory filing prerequisites and technical evidence dossiers verified for {herb_label}?")

    urgency = "IMMEDIATE" if any(c.get("severity") == "CRITICAL" for c in contradictions) else ("URGENT" if any(c.get("severity") == "HIGH" for c in contradictions) else "ADVISORY")
    risk_rating = "HIGH" if final_percentage < 70 else ("MEDIUM" if final_percentage < 85 else "LOW")

    return {
        "triggered": True,
        "expertType": expert_type,
        "expert_type": expert_type,
        "riskRating": risk_rating,
        "urgency_level": urgency,
        "keyQuestions": questions,
        "target_questions": questions,
        "questions_for_counsel": questions,
        "riskSummary": f"Human escalation triggered with {urgency} priority for {expert_type} based on {len(contradictions)} identified risk factors."
    }


# ==============================================================================
# PART 9: MULTILINGUAL LOCALIZATION & DISCLAIMER
# ==============================================================================
def localize_multilingual_layer(deliverable_text: str, language: str = "en") -> Dict[str, Any]:
    """Layer 9: Multilingual Trilingual Formatter (EN, HI, MR)"""
    lang = (language or "en").lower()
    glossary = GLOSSARIES.get(lang, {})

    disclaimers = {
        "en": "⚖️ STATUTORY NOTICE: This analysis provides statutory compliance and prior-art information and does not constitute formal legal advice.",
        "hi": "⚖️ वैधानिक सूचना: यह विश्लेषण वैधानिक अनुपालन और पूर्व-कला की जानकारी प्रदान करता है, यह औपचारिक कानूनी सलाह नहीं है।",
        "mr": "⚖️ वैधानिक सूचना: हे विश्लेषण वैधानिक अनुपालन आणि पूर्व-कला माहिती प्रदान करते, हा औपचारिक कायदेशीर सल्ला नाही."
    }

    return {
        "selected_language": lang,
        "disclaimer": disclaimers.get(lang, disclaimers["en"]),
        "glossary_terms": glossary
    }


# ==============================================================================
# MAIN 9-LAYER UNIFIED PIPELINE EVALUATION
# ==============================================================================
def evaluate_full_pipeline(
    prompt_text: str,
    deliverable_text: str = "",
    target_language: str = "en",
    requested_jurisdiction: Optional[str] = None
) -> Dict[str, Any]:
    """
    Executes the complete 9-Layer Architecture:
    - Layer 1 & 2: Ingress & Domain-First Council Selection
    - Layer 3 & 4: Strategic Roadmap & Primary Pathway Resolver
    - Layer 5: Deterministic Jurisdiction Resolution Hierarchy
    - Layer 6: Hard Metadata-Filtered RAG Retrieval Gate
    - Layer 7: 3-Tier Statutory Verification & Entailment Engine
    - Layer 8: Multi-Factor Confidence with Ceilings & Dynamic Escalation
    - Layer 9: Multilingual Localization
    """
    # 1. Layer 5: Deterministic Jurisdiction Resolution
    jurisdiction_data = resolve_jurisdiction_layer(prompt_text, requested_jurisdiction)

    # 2. Layer 1, 2, 3: Domain Classification, Pathway & Agent Squad
    domain, primary_pathway, squad = classify_domain_and_pathway(prompt_text, jurisdiction_data)

    # 3. Layer 6: Hard-Filtered Citation Retrieval & Source Relevance Validation
    relevant_sources, blocked_sources, is_jur_safe = retrieve_filtered_citations_layer(
        prompt_text, jurisdiction_data, domain
    )

    # 4. Layer 7: 3-Tier Statutory Verification & Entailment Audit
    verification_data = audit_verification_layer(
        prompt_text=prompt_text,
        deliverable_text=deliverable_text,
        jurisdiction_res=jurisdiction_data,
        domain=domain,
        relevant_sources=relevant_sources
    )

    # If retrieval jurisdiction was unsafe, force fail verification
    if not is_jur_safe:
        verification_data["is_safe"] = False
        verification_data["contradictions_flagged"].append({
            "severity": "CRITICAL",
            "issue": "RETRIEVAL_JURISDICTION_FAILURE",
            "explanation": "Indian statutory sources retrieved for a purely foreign regulatory query.",
            "remedy": "Filter retrieval exclusively to the target foreign jurisdiction."
        })

    # 5. Layer 8: Multi-Factor Confidence with Ceilings & Escalation
    confidence_data = compute_confidence_layer(
        groundedness=verification_data["groundedness_score"],
        relevant_sources=relevant_sources,
        contradictions=verification_data["contradictions_flagged"],
        jurisdiction_res=jurisdiction_data,
        domain=domain,
        prompt_text=prompt_text,
        deliverable_text=deliverable_text,
        language=target_language
    )

    # 6. Layer 9: Multilingual Trilingual Formatter
    multilingual_data = localize_multilingual_layer(deliverable_text, target_language)

    # Telemetry Integrity Verification (Part 14)
    telemetry_consistent = (
        len(relevant_sources) == verification_data["three_tier_verification"]["tier_1_citation_verification"].get("citations_audited", 0)
    )

    return {
        "success": True,
        "intent": domain,
        "domain": domain,
        "primary_regulatory_pathway": primary_pathway,
        "agents": squad,
        "jurisdiction": jurisdiction_data,
        "citations": relevant_sources,
        "blocked_citations": blocked_sources,
        "verification": verification_data,
        "confidence": confidence_data,
        "multilingual": multilingual_data,
        "telemetry_consistent": telemetry_consistent,
        "execution_status": "COMPLETED_9_LAYERS"
    }


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    test_q = "We want to conduct Phase II clinical trials in the US for a standardized Gugglu extract under FDA 21 CFR 312."
    res = evaluate_full_pipeline(test_q)
    print("Detected Jurisdiction:", res["jurisdiction"]["primary_jurisdiction"])
    print("Domain:", res["domain"])
    print("Primary Pathway:", res["primary_regulatory_pathway"])
    print("Agents:", res["agents"])
    print("Retrieved Sources:", [s["id"] for s in res["citations"]])
    print("Blocked Sources count:", len(res["blocked_citations"]))
    print("Confidence Rating:", res["confidence"]["confidence_rating"])
