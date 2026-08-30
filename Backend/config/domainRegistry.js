/**
 * House of Cards / IP-SAKTI — Decoupled Domain Registry
 * Self-contained, pluggable domain packages providing strict state isolation,
 * whitelist-based source retrieval, dynamic ground-truth prompt injection,
 * and parameterized verifier assertions.
 */

export const DOMAIN_REGISTRY = {
  EU_COSMETIC_REGULATORY: {
    id: "EU_COSMETIC_REGULATORY",
    label: "EU Cosmetic Regulation (EC) No 1223/2009",
    jurisdiction: "EU",
    squad: [
      { name: "EU Cosmetic Regulatory Lead", role: "EU REGULATORY LEAD", desc: "EU Cosmetic Regulation & Strategy" },
      { name: "Safety Assessor (CPSR)", role: "SAFETY ASSESSOR (CPSR)", desc: "Article 10 & Annex I CPSR Safety Dossiers" },
      { name: "CPNP Specialist", role: "CPNP SPECIALIST", desc: "Article 13 CPNP Notification & Nanomaterials" },
      { name: "Responsible Person (RP)", role: "RESPONSIBLE PERSON / RP", desc: "Article 4 RP Mandate & Article 23 SUE Vigilance" },
      { name: "EU Statutory Verifier", role: "STATUTORY VERIFIER", desc: "Regulation 1223/2009 3-Tier Verifier" }
    ],
    allowedSourcePrefixes: ["eu-reg-1223-2009-"],
    forbiddenTerms: [
      "Biological Diversity Act", "Section 6(1)", "NBA", "Rule 158B", 
      "Patents Act 1970", "Section 3(p)", "Section 3(d)", "Form 25D", "Schedule T"
    ],
    statutoryMappings: `
- Responsible Person (RP): Article 4 (Mandatory EU legal/natural person; DO NOT cite Article 8 or Article 1(3))
- Safety Assessment & CPSR (Part A/B): Article 10 & Annex I (Conducted by qualified safety assessor)
- Product Information File (PIF): Article 11 (Maintained at RP address for 10 years, NOT submitted proactively)
- Pre-market Notification (CPNP): Article 13 (Electronic notification prior to market placement)
- Nanomaterials (6-Month Prior Notice): Article 16
- Serious Undesirable Effects (SUE) / Cosmetovigilance: Article 23 (DO NOT cite Article 11 or Article 10)
- Foreign Law Exclusions: Strictly prohibited from citing Indian statutes (Patents Act, BDA Sec 6(1), Rule 158B)
    `,
    verifierAssertions: [
      { regex: /Responsible Person.*Article\s*(?:[1-35-9]|1\(3\)|8)\b/i, error: "Responsible Person misattributed (must be Article 4)" },
      { regex: /(?:Adverse Reaction|SUE|Cosmetovigilance).*Article\s*(?:[1-9]|1[0-2]|1[4-9]|2[0-24-9])\b/i, error: "SUE / Adverse Reactions misattributed (must be Article 23)" },
      { regex: /Nanomaterial.*Article\s*(?:[1-9]|1[0-5]|1[7-9]|2[0-9])\b/i, error: "Nanomaterials misattributed (must be Article 16)" },
      { regex: /(?:PIF|Product Information File).*Article\s*(?:[1-9]|10|1[2-9]|2[0-9])\b/i, error: "PIF misattributed (must be Article 11)" }
    ]
  },

  INTERNATIONAL_TRADEMARK: {
    id: "INTERNATIONAL_TRADEMARK",
    label: "Madrid System for International Registration of Marks (WIPO)",
    jurisdiction: "International",
    squad: [
      { name: "Madrid Protocol Strategist", role: "TRADEMARK STRATEGIST", desc: "WIPO Madrid System Strategy & Class 5/3 Protection" },
      { name: "Global Brand Researcher", role: "WIPO MADRID SPECIALIST", desc: "WIPO Global Brand Database & Nice Classification" },
      { name: "IP Trademark Attorney", role: "IP ATTORNEY", desc: "Basic Home Application & Single Filing Management" },
      { name: "Portfolio Manager", role: "PORTFOLIO MANAGER", desc: "Multi-Jurisdiction Designation & MM2 Filings" },
      { name: "Statutory Trademark Verifier", role: "STATUTORY VERIFIER", desc: "Madrid Protocol & National Office Verifier" }
    ],
    allowedSourcePrefixes: ["intl-wipo-madrid", "in-tm-act-1999"],
    forbiddenTerms: [
      "Biological Diversity Act", "Section 6(1)", "Rule 158B", "CPSR", 
      "CPNP", "Cosmetovigilance", "Annex I", "Charaka Samhita"
    ],
    statutoryMappings: `
- Basic Application / Base Mark: National IP Office of Origin (Section 18 / Form TM-A in India)
- International Application: Madrid Protocol Article 2 & Article 3 via WIPO International Bureau (Form MM2)
- Designation of Contracting Parties: Madrid Protocol Article 3bis across designated member states
- Central Attack / Dependency Period: 5 years under Madrid Protocol Article 6 (dependent on basic mark)
    `,
    verifierAssertions: [
      { regex: /(?:Biological Diversity Act|Section 6\(1\)|NBA)/i, error: "NBA approval is not applicable to Trademark applications." },
      { regex: /(?:CPSR|PIF|CPNP|SUE)/i, error: "Cosmetic regulatory artifacts cannot appear in Trademark dossiers." }
    ]
  },

  AYURVEDA_PATENT: {
    id: "AYURVEDA_PATENT",
    label: "Indian Patents Act 1970 & Traditional Knowledge Clearance",
    jurisdiction: "India",
    squad: [
      { name: "Registered Patent Attorney", role: "PATENT STRATEGIST", desc: "Indian Patents Act & Prior-Art Architecture" },
      { name: "TKDL Prior-Art Researcher", role: "PRIOR ART RESEARCHER", desc: "CSIR TKDL Database & Classical Treatise Search" },
      { name: "Synergy & Claims Architect", role: "CLAIMS ARCHITECT", desc: "Section 3(d)/3(e) Synergistic Data Formulation" },
      { name: "ABS Compliance Agent", role: "ABS COMPLIANCE AGENT", desc: "Biological Diversity Act Section 6(1) Clearance" },
      { name: "Statutory Patentability Verifier", role: "STATUTORY VERIFIER", desc: "Section 3(p) Traditional Knowledge Bar Verifier" }
    ],
    allowedSourcePrefixes: ["in-patents-act-", "in-bd-act-", "in-tkdl", "intl-wipo-pct", "intl-pct-"],
    forbiddenTerms: [
      "EU Regulation 1223/2009", "CPNP", "CPSR", "Responsible Person under Article 4", 
      "21 CFR 312", "21 CFR 111", "THMPD Directive 2004/24/EC"
    ],
    statutoryMappings: `
- Traditional Knowledge Bar: Section 3(p) of Patents Act 1970 (Bars patenting aggregations of known traditional Ayurvedic properties without synergy)
- Enhanced Efficacy Requirement: Section 3(d) of Patents Act 1970 (Requires significantly enhanced therapeutic efficacy for derivatives)
- Mere Admixture Bar: Section 3(e) of Patents Act 1970 (Requires empirical proof of non-obvious synergistic interaction)
- Mandatory Prior NBA Approval: Section 6(1) of Biological Diversity Act 2002 (Form III approval before grant/foreign filing)
    `,
    verifierAssertions: [
      { regex: /(?:EU Regulation 1223\/2009|CPNP|CPSR|Annex I CPSR)/i, error: "EU cosmetic rules cannot appear in Indian Patent dossiers." },
      { regex: /(?:21 CFR 312|21 CFR 111|DSHEA)/i, error: "US FDA drug/supplement rules cannot appear in Indian Patent dossiers." }
    ]
  },

  AYUSH_MANUFACTURING: {
    id: "AYUSH_MANUFACTURING",
    label: "Indian AYUSH / ASU Manufacturing Licensing (Drugs & Cosmetics Rules — Rule 158B)",
    jurisdiction: "India",
    squad: [
      { name: "AYUSH Regulatory Strategist", role: "AYUSH REGULATORY LEAD", desc: "Drugs & Cosmetics Act & SLA Strategy" },
      { name: "First Schedule Samhita Researcher", role: "SAMHITA RESEARCHER", desc: "Authoritative Ayurvedic Pharmacopoeia Treatise Verification" },
      { name: "Form 25D Licensing Architect", role: "DOSSIER ARCHITECT", desc: "Rule 158B(I)(A) Classical vs 158B(I)(B) Proprietary Pathways" },
      { name: "SLA Application Executor", role: "APPLICATION EXECUTOR", desc: "State Licensing Authority Dossier Assembly" },
      { name: "Schedule T GMP Verifier", role: "STATUTORY VERIFIER", desc: "Schedule T GMP & Quality Assurance Verifier" }
    ],
    allowedSourcePrefixes: ["in-dc-rules-158b", "in-dc-act-1940", "in-magic-remedies-act-"],
    forbiddenTerms: [
      "EU Regulation 1223/2009", "CPNP", "CPSR", "21 CFR 312", 
      "21 CFR 111", "Madrid Protocol", "WIPO"
    ],
    statutoryMappings: `
- Classical ASU Formulations: Rule 158B(I)(A) allows Form 25D manufacturing licenses without clinical trials based strictly on First Schedule authoritative texts
- Patent or Proprietary ASU Medicines: Rule 158B(I)(B) governs novel recipes/extractions requiring safety and pilot toxicity study dossiers
- Good Manufacturing Practices: Schedule T compliance under Chapter IV-A of Drugs & Cosmetics Act 1940
- Claims Restriction: Drugs and Magic Remedies (Objectionable Advertisements) Act 1954 bars cure claims for 54 scheduled diseases
    `,
    verifierAssertions: [
      { regex: /(?:EU Regulation 1223\/2009|CPNP|CPSR)/i, error: "EU cosmetic rules cannot appear in AYUSH manufacturing dossiers." },
      { regex: /(?:21 CFR 312|21 CFR 111)/i, error: "US FDA rules cannot appear in Indian AYUSH manufacturing dossiers." }
    ]
  },

  FOOD_FSSAI: {
    id: "FOOD_FSSAI",
    label: "FSSAI (Ayurveda Aahar) Regulations, 2022 & Food Safety Compliance",
    jurisdiction: "India",
    squad: [
      { name: "FSSAI Compliance Strategist", role: "FSSAI STRATEGIST", desc: "Food Safety & Standards Act 2006 & Ayurveda Aahar Regulations" },
      { name: "Ayurvedic Culinary Text Researcher", role: "CULINARY RESEARCHER", desc: "First Schedule Authoritative Culinary Text Search" },
      { name: "Food Safety & Additives Architect", role: "FOOD SAFETY ARCHITECT", desc: "Permissible Additives & Heavy Metal Safety Limits" },
      { name: "FSSAI Licensing Dossier Executor", role: "LICENSING EXECUTOR", desc: "Food Business Operator (FBO) Form B Submission" },
      { name: "Non-Curative Labeling Verifier", role: "STATUTORY VERIFIER", desc: "Prohibited Curative Claims & DMR(OA) Act Verifier" }
    ],
    allowedSourcePrefixes: ["in-fssai-ayurveda-aahar", "in-fssai-", "in-magic-remedies-act-"],
    forbiddenTerms: [
      "EU Regulation 1223/2009", "CPNP", "CPSR", "21 CFR 312", 
      "Patent Cooperation Treaty", "Rule 158B"
    ],
    statutoryMappings: `
- Recipe Authentication: FSSAI (Ayurveda Aahar) Regulations 2022 mandate formulation in accordance with recognized Ayurvedic texts
- Strict Bar on Curative Claims: Ayurveda Aahar products cannot claim to cure, prevent, or treat any disease or disorder
- Safety & Additives: Strict compliance with microbiological criteria and permissible food additives; Schedule E-1 toxic botanicals strictly barred
- Statutory Warning: Mandatory Ayurveda Aahar logo and advisory warning on all retail packaging
    `,
    verifierAssertions: [
      { regex: /(?:cure|curing|treat|treatment|heal|eradicate|eliminate)\s+(?:severe|clinical|chronic)?\s*(?:depression|cancer|diabetes|anxiety|disease)/i, error: "Curative disease claims are strictly barred under FSSAI Ayurveda Aahar Regulations." },
      { regex: /(?:EU Regulation 1223\/2009|CPNP|CPSR)/i, error: "EU cosmetic rules cannot appear in FSSAI food dossiers." }
    ]
  },

  ABS_BIODIVERSITY: {
    id: "ABS_BIODIVERSITY",
    label: "Biological Diversity Act 2002/2023 & Access and Benefit Sharing (ABS)",
    jurisdiction: "India",
    squad: [
      { name: "National Biodiversity Authority Counsel", role: "NBA SENIOR COUNSEL", desc: "Biological Diversity Act 2002/2023 Statutory Strategy" },
      { name: "Biological Resource Access Researcher", role: "SBB RESEARCHER", desc: "State Biodiversity Board Intimation & SBB Rules" },
      { name: "Benefit-Sharing Agreement Architect", role: "ABS ARCHITECT", desc: "0.1% to 0.5% Benefit-Sharing Valuation & MAT Terms" },
      { name: "NBA Form I/III Application Executor", role: "APPLICATION EXECUTOR", desc: "Form I (Foreign Access) & Form III (IPR Prior Approval)" },
      { name: "Biological Diversity Statutory Verifier", role: "STATUTORY VERIFIER", desc: "Section 3/6(1)/7 Statutory Compliance Verifier" }
    ],
    allowedSourcePrefixes: ["in-bd-act-2002", "intl-cbd-nagoya", "in-patents-act-"],
    forbiddenTerms: [
      "EU Regulation 1223/2009", "CPNP", "CPSR", "21 CFR 312", 
      "21 CFR 111", "Rule 158B"
    ],
    statutoryMappings: `
- Foreign Entity Access: Section 3 of BDA 2002 mandates prior NBA approval (Form I) for non-citizens, NRIs, and foreign-controlled entities accessing Indian bio-resources
- Mandatory IPR Prior Clearance: Section 6(1) of BDA 2002 mandates prior approval (Form III) before applying for patents outside India or before grant in India
- Benefit Sharing: Standard benefit sharing payment of 0.1% - 0.5% of ex-factory sale value under ABS Guidelines
- International Framework: Compliant with Nagoya Protocol on Prior Informed Consent (PIC) and Mutually Agreed Terms (MAT)
    `,
    verifierAssertions: [
      { regex: /(?:EU Regulation 1223\/2009|CPNP|CPSR)/i, error: "EU cosmetic rules cannot appear in NBA biodiversity dossiers." }
    ]
  },

  US_FDA_DRUG: {
    id: "US_FDA_DRUG",
    label: "US FDA Botanical Drug Development / IND Pathway (21 CFR Part 312)",
    jurisdiction: "US",
    squad: [
      { name: "US FDA Botanical Regulatory Specialist", role: "FDA BOTANICAL STRATEGIST", desc: "US FDA CDER Botanical Drug Regulatory Architecture" },
      { name: "IND Clinical Protocol Lead", role: "IND PROTOCOL LEAD", desc: "21 CFR 312 Investigational New Drug Protocols & Phase I-III" },
      { name: "Botanical CMC Authentication Architect", role: "CMC ARCHITECT", desc: "Batch-to-Batch Fingerprinting & Raw Material QC" },
      { name: "FDA 21 CFR 312 Submission Executor", role: "SUBMISSION EXECUTOR", desc: "FDA Form 1571 IND Filing & Pre-IND Meeting Briefing" },
      { name: "US Regulatory Citation Verifier", role: "STATUTORY VERIFIER", desc: "FDA Statutory & Clinical Risk Verifier" }
    ],
    allowedSourcePrefixes: ["us-fda-21cfr312", "us-fda-", "us-uspto-"],
    forbiddenTerms: [
      "EU Regulation 1223/2009", "CPNP", "CPSR", "Rule 158B", 
      "Form 25D", "Schedule T", "Ayurveda Aahar"
    ],
    statutoryMappings: `
- Investigational New Drug (IND): 21 CFR § 312 mandates IND submission (Form FDA 1571) prior to commencing US clinical trials
- Chemistry, Manufacturing & Controls (CMC): Rigorous batch-to-batch consistency and spectroscopic fingerprinting for complex botanical mixtures
- Clinical Progression: Sequential Phase I (safety/pharmacology), Phase II (dose-ranging efficacy), and Phase III (pivotal confirmatory) trials leading to NDA under Section 505(b)
    `,
    verifierAssertions: [
      { regex: /(?:Rule 158B|Form 25D|Schedule T)/i, error: "Indian AYUSH licensing rules cannot appear in US FDA drug dossiers." },
      { regex: /(?:EU Regulation 1223\/2009|CPNP|CPSR)/i, error: "EU cosmetic rules cannot appear in US FDA drug dossiers." }
    ]
  },

  US_FDA_DIETARY_SUPPLEMENT: {
    id: "US_FDA_DIETARY_SUPPLEMENT",
    label: "US FDA Dietary Supplement Compliance & cGMP (21 CFR Part 111 & DSHEA 1994)",
    jurisdiction: "US",
    squad: [
      { name: "US Dietary Supplement Strategist", role: "DSHEA STRATEGIST", desc: "Dietary Supplement Health and Education Act (DSHEA 1994)" },
      { name: "Structure/Function Claims Researcher", role: "CLAIMS RESEARCHER", desc: "Permissible Structure/Function vs Impermissible Disease Claims" },
      { name: "21 CFR Part 111 cGMP Architect", role: "CGMP ARCHITECT", desc: "Current Good Manufacturing Practices for Supplements" },
      { name: "FDA Facility & Labeling Executor", role: "LABELING EXECUTOR", desc: "Supplement Facts Panel & 30-Day Notification" },
      { name: "FDA Disclaimer & Safety Verifier", role: "STATUTORY VERIFIER", desc: "Mandatory FDA Disclaimer & NDI Notification Verifier" }
    ],
    allowedSourcePrefixes: ["us-fda-21cfr111", "us-fda-", "in-dc-rules-158b"],
    forbiddenTerms: [
      "EU Regulation 1223/2009", "CPNP", "CPSR", "21 CFR 312 IND", "Form 25D"
    ],
    statutoryMappings: `
- Current Good Manufacturing Practice (cGMP): 21 CFR Part 111 mandates manufacturing, holding, and distribution quality standards
- Structure/Function Claims: Permitted with mandatory disclaimer: 'This statement has not been evaluated by the FDA. This product is not intended to diagnose, treat, cure, or prevent any disease.'
- 30-Day Notification: Claims must be notified to FDA within 30 days of first marketing under DSHEA § 6
- New Dietary Ingredients (NDI): Pre-market notification under 21 CFR § 190.6 required for post-1994 botanicals
    `,
    verifierAssertions: [
      { regex: /(?:cure|curing|prevent|preventing|treat|treating)\s+(?:disease|disorder|cancer|diabetes)/i, error: "Disease cure/treatment claims are illegal for dietary supplements under DSHEA 1994." },
      { regex: /(?:EU Regulation 1223\/2009|CPNP|CPSR)/i, error: "EU cosmetic rules cannot appear in US Dietary Supplement dossiers." }
    ]
  },

  EU_THMPD: {
    id: "EU_THMPD",
    label: "EU Traditional Herbal Medicinal Products Directive (Directive 2004/24/EC & THMPD)",
    jurisdiction: "EU",
    squad: [
      { name: "EU Herbal Medicines Regulatory Lead", role: "EU THMPD STRATEGIST", desc: "Directive 2004/24/EC & Directive 2001/83/EC Strategy" },
      { name: "30-Year Traditional Use Researcher", role: "TRADITIONAL USE RESEARCHER", desc: "Bibliographical Evidence & 15-Year EU Usage Nexus" },
      { name: "EMA / HMPC Community Monograph Architect", role: "HMPC MONOGRAPH ARCHITECT", desc: "HMPC Monograph Alignment & Quality Dossier (Module 3)" },
      { name: "EU National Authority Dossier Executor", role: "DOSSIER EXECUTOR", desc: "National Simplified Registration Application" },
      { name: "EU Statutory Directive Verifier", role: "STATUTORY VERIFIER", desc: "Directive 2004/24/EC Precondition Verifier" }
    ],
    allowedSourcePrefixes: ["eu-directive-2004-24-ec", "eu-ema-hmpc-", "eu-"],
    forbiddenTerms: [
      "CPNP", "Annex I CPSR", "Responsible Person under Article 4", 
      "Rule 158B", "Section 3(p)", "21 CFR 312"
    ],
    statutoryMappings: `
- Simplified Traditional Registration: Directive 2004/24/EC provides registration without clinical trials for herbal medicinal products
- Traditional Use Precondition: Requires proof of 30 years continuous traditional medicinal use, including at least 15 years within the European Union
- Safety & Quality Standards: Full Module 3 quality dossier conforming to European Pharmacopoeia and EU GMP Directive 2003/94/EC
- Well-Established Use Alternative: Products with 10+ years established EU clinical use can apply under Article 10a of Directive 2001/83/EC using HMPC monographs
    `,
    verifierAssertions: [
      { regex: /(?:CPNP|Annex I CPSR)/i, error: "Cosmetic Regulation artifacts cannot appear in THMPD medicinal dossiers." },
      { regex: /(?:Rule 158B|Form 25D)/i, error: "Indian AYUSH licensing rules cannot appear in EU THMPD dossiers." }
    ]
  },

  INTERNATIONAL_PATENT: {
    id: "INTERNATIONAL_PATENT",
    label: "WIPO Patent Cooperation Treaty (PCT) & GRATK Treaty 2024",
    jurisdiction: "International",
    squad: [
      { name: "WIPO PCT Patent Strategist", role: "PCT STRATEGIST", desc: "PCT International Phase & National Phase Entry" },
      { name: "ISA Prior-Art Search Researcher", role: "ISA RESEARCHER", desc: "International Search Report (ISR) & Written Opinion Analysis" },
      { name: "PCT Claims Harmonization Architect", role: "CLAIMS ARCHITECT", desc: "Unity of Invention & Global Claim Drafting" },
      { name: "PCT/RO/101 Filing Executor", role: "FILING EXECUTOR", desc: "Form PCT/RO/101 & ePCT Submission" },
      { name: "WIPO GRATK Treaty Verifier", role: "STATUTORY VERIFIER", desc: "Mandatory Genetic Resource & TK Disclosure Verifier" }
    ],
    allowedSourcePrefixes: ["intl-wipo-pct", "intl-wipo-gratk-2024", "in-patents-act-", "in-cdsco-phytopharmaceutical"],
    forbiddenTerms: [
      "EU Regulation 1223/2009", "CPNP", "CPSR", "Rule 158B", "Form 25D"
    ],
    statutoryMappings: `
- Unified International Filing: Single PCT application preserves priority across 158 contracting states under Articles 1-64
- Priority Window: 12-month Paris Convention priority window and 30/31-month National Phase entry deadline
- Mandatory Genetic Resource Disclosure: WIPO GRATK Treaty 2024 (Article 3) mandates explicit disclosure of country of origin for genetic resources / TK
- Indian Nexus: Inventions originating from India require foreign filing license under Section 39 or initial Indian filing under Section 6(1) of BDA
    `,
    verifierAssertions: [
      { regex: /(?:EU Regulation 1223\/2009|CPNP|CPSR)/i, error: "EU cosmetic rules cannot appear in WIPO patent dossiers." }
    ]
  },

  MULTI_DOMAIN: {
    id: "MULTI_DOMAIN",
    label: "Multi-Jurisdictional Cross-Border Compliance & Global Export",
    jurisdiction: "Both",
    squad: [
      { name: "Cross-Border Regulatory Strategist", role: "CROSS-BORDER STRATEGIST", desc: "Dual Domestic & International Regulatory Architecture" },
      { name: "Comparative Statutory Researcher", role: "STATUTORY RESEARCHER", desc: "Cross-Jurisdiction Treaty & National Law Harmonization" },
      { name: "Dual-Market Compliance Architect", role: "COMPLIANCE ARCHITECT", desc: "Combined Indian Licensing & Foreign Export Dossiers" },
      { name: "Multi-Jurisdiction Application Executor", role: "APPLICATION EXECUTOR", desc: "Dual Application Assembly & SBB/NBA Intimations" },
      { name: "Global Statutory Verifier", role: "STATUTORY VERIFIER", desc: "Cross-Border Entailment & Contradiction Verifier" }
    ],
    allowedSourcePrefixes: ["in-", "intl-", "us-", "eu-"],
    forbiddenTerms: [],
    statutoryMappings: `
- Dual Jurisdiction Governance: Harmonizes Indian domestic manufacturing/IPR compliance with target import country directives
- NBA Prior Clearance: Mandatory Section 6(1) Form III approval before foreign patent prosecution using Indian bio-resources
- Export Quality & Labeling: Complies with Chapter IV-A Rule 158B for domestic production and destination country standards (e.g. 21 CFR 111, DSHEA, EU THMPD)
    `,
    verifierAssertions: []
  }
};

/**
 * Resolves the active domain package from DOMAIN_REGISTRY.
 * Automatically falls back to AYURVEDA_PATENT if unrecognized.
 */
export function getDomainPackage(domainId) {
  if (!domainId) return DOMAIN_REGISTRY.AYURVEDA_PATENT;
  const canonicalId = domainId.toUpperCase().trim();
  return DOMAIN_REGISTRY[canonicalId] || DOMAIN_REGISTRY.AYURVEDA_PATENT;
}

/**
 * Deterministic Domain Classifier mapping prompt text and jurisdiction to canonical domain ID.
 */
export function detectDomainId(promptText, jurisdiction = null) {
  const norm = (promptText || "").toLowerCase();
  const jNorm = (jurisdiction || "").toLowerCase();

  // =========================================================================
  // TIER 1: HIGHEST PRECEDENCE — INDIAN IP / PATENT / ABS STATUTES
  // Explicit patent statutes & provisions OVERRIDE all generic words (brand, Madrid, etc.)
  // =========================================================================
  const hasTier1PatentTriggers = (
    norm.includes("section 3(p)") || norm.includes("section 3(d)") || norm.includes("section 3(e)") ||
    norm.includes("3(p)") || norm.includes("3(d)") || norm.includes("3(e)") ||
    norm.includes("patents act") || norm.includes("patent act") ||
    norm.includes("biological diversity act") || norm.includes("nba form iii") || norm.includes("form iii") ||
    norm.includes("form 3") || norm.includes("tkdl") || norm.includes("patentability") ||
    norm.includes("inventive step") || norm.includes("non-patentable") || norm.includes("prior art") ||
    norm.includes("patent application") || norm.includes("patent claim") || norm.includes("patent specification") ||
    norm.includes("patent filing") || norm.includes("patent grant") ||
    (norm.includes("patent") && !norm.includes("patent and trademark office") && !norm.includes("patent and trade mark"))
  );

  const hasTier1AbsTriggers = (
    !hasTier1PatentTriggers && (
      norm.includes("nba form i") || norm.includes("nba form 1") || /\bform i\b/.test(norm) ||
      norm.includes("foreign equity") || norm.includes("foreign company accessing") ||
      (norm.includes("biological diversity") && norm.includes("access")) ||
      (norm.includes("access and benefit sharing") && !norm.includes("patent"))
    )
  );

  if (hasTier1PatentTriggers) {
    if (jNorm === "both" || norm.includes("foreign filing license") || (norm.includes("us") && norm.includes("patent") && norm.includes("nba"))) {
      return "MULTI_DOMAIN";
    }
    return "AYURVEDA_PATENT";
  }

  if (hasTier1AbsTriggers) {
    return "ABS_BIODIVERSITY";
  }

  // =========================================================================
  // TIER 2: EU COSMETIC REGULATION (EC) No 1223/2009
  // =========================================================================
  const hasTier2EUCosmeticTriggers = (
    norm.includes("1223/2009") || norm.includes("regulation 1223") || 
    norm.includes("pif") || norm.includes("cpnp") || norm.includes("cpsr") || 
    norm.includes("cosmetic product safety report") ||
    (norm.includes("cosmetic") && (norm.includes("eu") || norm.includes("europe") || norm.includes("france") || norm.includes("germany") || norm.includes("responsible person") || norm.includes("sue") || norm.includes("nanomaterial") || norm.includes("hair-oil") || norm.includes("skin serum") || norm.includes("serum") || norm.includes("oil")))
  );

  if (hasTier2EUCosmeticTriggers) {
    return "EU_COSMETIC_REGULATORY";
  }

  // =========================================================================
  // TIER 3: TRADEMARK & BRAND PROTECTION (Madrid Protocol / Class 5)
  // (Evaluated ONLY if Tier 1 and Tier 2 triggers are absent)
  // =========================================================================
  const hasTier3TrademarkTriggers = (
    norm.includes("madrid") || norm.includes("class 5") ||
    norm.includes("trademark") || norm.includes("trade mark") ||
    norm.includes("brand name") || norm.includes("brand protection") ||
    norm.includes("tm-a") || norm.includes("gi tag") || norm.includes("geographical indication")
  );

  if (hasTier3TrademarkTriggers) {
    return "INTERNATIONAL_TRADEMARK";
  }

  // =========================================================================
  // TIER 4: SPECIFIC DOMAIN FRAMEWORKS (FDA, THMPD, PCT, FSSAI, AYUSH)
  // =========================================================================
  // 4a. US FDA Drug IND
  if (norm.includes("21 cfr 312") || (norm.includes("fda") && (norm.includes("ind") || norm.includes("clinical trial") || norm.includes("phase i") || norm.includes("botanical drug") || norm.includes("cder")))) {
    return "US_FDA_DRUG";
  }

  // 4b. US FDA Dietary Supplement / DSHEA
  if (norm.includes("21 cfr 111") || norm.includes("dshea") || (norm.includes("fda") && (norm.includes("dietary supplement") || norm.includes("structure function") || norm.includes("supplement") || norm.includes("cgmp")))) {
    return "US_FDA_DIETARY_SUPPLEMENT";
  }

  // 4c. EU THMPD
  if (norm.includes("directive 2004/24/ec") || norm.includes("thmpd") || (norm.includes("germany") && norm.includes("traditional")) || (norm.includes("eu") && norm.includes("herbal") && norm.includes("medicinal"))) {
    return "EU_THMPD";
  }

  // 4d. International Patent / WIPO PCT
  if (norm.includes("pct") || norm.includes("patent cooperation treaty") || (norm.includes("wipo") && norm.includes("patent"))) {
    return "INTERNATIONAL_PATENT";
  }

  // 4e. Food / FSSAI Ayurveda Aahar
  if (norm.includes("fssai") || norm.includes("ayurveda aahar") || (norm.includes("food") && norm.includes("ayurved"))) {
    return "FOOD_FSSAI";
  }

  // 4f. Classical / Proprietary Manufacturing (Rule 158B)
  if (norm.includes("rule 158b") || norm.includes("form 25d") || norm.includes("schedule t") || norm.includes("manufacturing license") || norm.includes("classical") || norm.includes("chyawanprash")) {
    return "AYUSH_MANUFACTURING";
  }

  // Default multi-jurisdiction or fallback
  if (jNorm === "international" || norm.includes("export") || norm.includes("global")) {
    return "MULTI_DOMAIN";
  }

  return "AYURVEDA_PATENT";
}
