"""
Core Data Models and Schema Definitions for IP-SAKTI Sahayak (Layers 7, 8, 9)
House of Cards Multi-Agent Framework
"""

from typing import List, Dict, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field


class AyurvedaCategory(str, Enum):
    CLASSICAL = "Classical Ayurvedic Medicine"
    PROPRIETARY = "Proprietary Ayurvedic Medicine"
    PHYTOPHARMACEUTICAL = "Phytopharmaceutical Drug"
    AYURVEDA_AAHAR = "Ayurveda Aahar / Nutraceutical"
    COSMETIC = "Ayurvedic Cosmetic"
    NEW_HERBAL_ENTITY = "New / Non-Classical Herbal Drug"


class Jurisdiction(str, Enum):
    INDIA = "India"
    US = "United States (USPTO)"
    EPO = "Europe (EPO)"
    WIPO_PCT = "International (WIPO PCT)"
    MULTI = "Multi-Jurisdictional"


class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    REFUSAL = "REFUSAL"


class LanguageCode(str, Enum):
    EN = "en"
    HI = "hi"
    MR = "mr"


class EvidenceSourceType(str, Enum):
    STATUTE = "Statute / Act"
    RULE = "Statutory Rule / Regulation"
    OFFICIAL_GUIDELINE = "Official Government Guideline"
    TKDL = "Traditional Knowledge Digital Library"
    PATENT_DB = "Patent Database / Prior Art"
    AYURVEDIC_TEXT = "Classical Ayurvedic Text (First Schedule)"
    CASE_LAW = "Judicial Precedent / Order"


class EvidenceChunk(BaseModel):
    id: str = Field(..., description="Unique chunk identifier")
    title: str = Field(..., description="Title of reference or act")
    source_type: EvidenceSourceType = Field(..., description="Type of legal/regulatory authority")
    act_or_regulation: str = Field(..., description="E.g., Patents Act 1970, Biological Diversity Act 2002, Drugs & Cosmetics Act 1940")
    section_or_rule: str = Field(..., description="E.g., Section 3(p), Rule 158B, Section 6(1)")
    jurisdiction: Jurisdiction = Field(default=Jurisdiction.INDIA)
    content: str = Field(..., description="Exact textual excerpt from the legal/scientific authority")
    url_or_ref: Optional[str] = Field(None, description="Official portal URL or Gazette ref")
    relevance_score: float = Field(default=1.0, ge=0.0, le=1.0)


class Citation(BaseModel):
    citation_id: str
    act_or_text: str
    section_or_rule: str
    jurisdiction: Jurisdiction = Jurisdiction.INDIA
    summary_of_statute: str
    is_authoritative: bool = True
    gazette_or_source_link: Optional[str] = None


class Claim(BaseModel):
    claim_id: str
    statement: str
    associated_citations: List[str] = Field(default_factory=list, description="IDs of cited authorities")
    domain_topic: str = Field(..., description="e.g. Patentability, Manufacturing License, ABS Clearance, Clinical Trials")
    target_jurisdiction: Jurisdiction = Jurisdiction.INDIA


# ==========================================
# UPSTREAM INTERMEDIATE OUTPUT (Layers 1-6)
# ==========================================
class UpstreamAgentOutput(BaseModel):
    """
    Synthesized intermediate output coming from Layers 1 to 6
    (Classification Agent, IP/RAG Agent, Prior-Art Agent, Jurisdiction & Citation Layers)
    """
    query_id: str
    raw_user_query: str
    product_name: str
    detected_category: AyurvedaCategory
    botanical_and_herbal_ingredients: List[str] = Field(default_factory=list)
    proposed_use_or_claim: str
    target_jurisdiction: Jurisdiction = Jurisdiction.INDIA
    synthesis_draft_text: str
    extracted_claims: List[Claim] = Field(default_factory=list)
    citations_referenced: List[Citation] = Field(default_factory=list)
    retrieved_evidence: List[EvidenceChunk] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ==========================================
# LAYER 7: VERIFICATION MODELS
# ==========================================
class ClaimVerificationStatus(str, Enum):
    FULLY_VERIFIED = "FULLY_VERIFIED"
    PARTIALLY_VERIFIED = "PARTIALLY_VERIFIED"
    UNSUBSTANTIATED = "UNSUBSTANTIATED"
    CONTRADICTS_STATUTE = "CONTRADICTS_STATUTE"
    JURISDICTION_MISMATCH = "JURISDICTION_MISMATCH"


class VerifiedClaimItem(BaseModel):
    claim: Claim
    status: ClaimVerificationStatus
    supporting_evidence_ids: List[str] = Field(default_factory=list)
    groundedness_score: float = Field(default=0.0, ge=0.0, le=1.0)
    verification_notes: str = ""


class CitationValidationResult(BaseModel):
    citation: Citation
    is_valid_statute: bool
    is_active_law: bool
    notes: str


# ==========================================
# 3-TIER VERIFICATION MODELS (CITATION -> APPLICABILITY -> CONCLUSION)
# ==========================================
class ApplicabilityFinding(BaseModel):
    statute_code: str
    statute_title: str
    is_applicable: bool
    preconditions_met: List[str] = Field(default_factory=list)
    preconditions_unmet: List[str] = Field(default_factory=list)
    applicability_rationale: str
    subject_matter_nexus: bool = True
    territorial_nexus: bool = True


class ConclusionValidationFinding(BaseModel):
    conclusion_statement: str
    statutory_basis: str
    is_justified: bool
    logical_status: str  # VALID_JUSTIFIED_DEDUCTION, STATUTORY_BAR_CONTRADICTION, NON_SEQUITUR, UNAUTHORIZED_EXEMPTION
    legal_analysis: str
    correct_statutory_verdict: str


class ContradictionSeverity(str, Enum):
    CRITICAL = "CRITICAL"  # Blatant statutory violation (e.g. patenting TK without modification)
    HIGH = "HIGH"          # Missing mandatory clearance (e.g. missing NBA approval)
    MEDIUM = "MEDIUM"      # Regulatory classification ambiguity (e.g. Proprietary vs Ayurveda-Aahar)
    LOW = "LOW"            # Procedural caveat or filing discrepancy


class ContradictionFinding(BaseModel):
    finding_id: str
    severity: ContradictionSeverity
    conflict_type: str  # e.g., "SECTION_3P_TK_CONFLICT", "BDA_NBA_APPROVAL_OMISSION", "RULE_158B_MISINTERPRETATION"
    description: str
    statutory_authority: str
    remedial_action: str


class VerificationResult(BaseModel):
    """
    Output produced by Layer 7 (Verification Agent)
    Implements 3-Tier Verification: Citation -> Applicability -> Conclusion
    """
    is_passed: bool
    overall_groundedness_score: float = Field(..., ge=0.0, le=1.0)
    citation_soundness_score: float = Field(..., ge=0.0, le=1.0)
    applicability_score: float = Field(default=1.0, ge=0.0, le=1.0)
    conclusion_justification_score: float = Field(default=1.0, ge=0.0, le=1.0)
    jurisdiction_coherence_score: float = Field(..., ge=0.0, le=1.0)
    verified_claims: List[VerifiedClaimItem] = Field(default_factory=list)
    unsubstantiated_claims: List[VerifiedClaimItem] = Field(default_factory=list)
    contradictions: List[ContradictionFinding] = Field(default_factory=list)
    citation_validations: List[CitationValidationResult] = Field(default_factory=list)
    applicability_findings: List[ApplicabilityFinding] = Field(default_factory=list)
    conclusion_validations: List[ConclusionValidationFinding] = Field(default_factory=list)
    three_tier_pipeline: Dict[str, Any] = Field(default_factory=dict)
    sanitized_synthesis_text: str
    verification_summary: str


# ==========================================
# LAYER 8: CONFIDENCE & ESCALATION MODELS
# ==========================================
class SpecialistRole(str, Enum):
    PATENT_ATTORNEY_LIFE_SCIENCES = "Patent Attorney (Life Sciences & Biotechnology)"
    AYUSH_REGULATORY_CONSULTANT = "AYUSH Regulatory & Licensing Consultant"
    NBA_ABS_COMPLIANCE_EXPERT = "National Biodiversity Authority (ABS) Legal Expert"
    TKDL_PRIOR_ART_SPECIALIST = "TKDL / Prior-Art Search Specialist"
    SENIOR_IP_COUNSEL = "Senior IP Counsel (Litigation & Enforcement)"


class EscalationTriggerReason(BaseModel):
    trigger_code: str
    severity: ContradictionSeverity
    explanation: str
    relevant_statutes: List[str] = Field(default_factory=list)


class EscalationDossier(BaseModel):
    is_escalation_required: bool
    target_specialist: Optional[SpecialistRole] = None
    urgency_level: str = "NORMAL"  # IMMEDIATE, URGENT, NORMAL, ADVISORY
    risk_summary: str
    triggers: List[EscalationTriggerReason] = Field(default_factory=list)
    brief_for_expert: str
    recommended_questions_for_counsel: List[str] = Field(default_factory=list)
    human_in_the_loop_flags: List[str] = Field(default_factory=list)


class ConfidenceScore(BaseModel):
    overall_confidence: ConfidenceLevel
    numeric_score: float = Field(..., ge=0.0, le=1.0)
    evidence_groundedness_weight: float
    citation_soundness_weight: float
    jurisdiction_coherence_weight: float
    contradiction_penalty: float
    confidence_justification: str
    is_safe_to_render: bool
    safe_refusal_text: Optional[str] = None
    escalation_dossier: EscalationDossier


# ==========================================
# LAYER 9: MULTILINGUAL MODELS
# ==========================================
class BilingualTerm(BaseModel):
    english_term: str
    local_term: str
    phonetic_or_devanagari: str
    statutory_context: str


class LocalizedSection(BaseModel):
    heading: str
    content: str


class MultilingualResponse(BaseModel):
    """
    Final Output delivered to the User after Layer 9 processing
    """
    query_id: str
    target_language: LanguageCode
    detected_input_language: LanguageCode
    
    # Core outputs in target language
    title: str
    product_classification_badge: str
    confidence_level_badge: str
    confidence_score_percent: int
    executive_summary: str
    detailed_legal_analysis: str
    key_actionable_steps: List[str] = Field(default_factory=list)
    
    # Statutory citations and verified evidence
    verified_statutory_citations: List[Dict[str, str]] = Field(default_factory=list)
    
    # Escalation notice if flagged
    escalation_notice: Optional[Dict[str, Any]] = None
    
    # Refusal notice if unsafe/invalid
    safe_refusal_notice: Optional[str] = None
    
    # Multilingual glossaries and disclaimers
    bilingual_glossary: List[BilingualTerm] = Field(default_factory=list)
    statutory_disclaimer: str
    
    # Raw verification metadata for transparency & audit
    verification_audit_trail: Dict[str, Any] = Field(default_factory=dict)
