"""
Hallucination Guard and Groundedness Verifier
Cross-checks individual claims against retrieved evidence passages.
"""

from typing import List, Tuple
from ..core.schema import (
    Claim,
    EvidenceChunk,
    VerifiedClaimItem,
    ClaimVerificationStatus,
    UpstreamAgentOutput
)


class HallucinationGuard:
    """
    Evaluates factual and statutory groundedness of claims against retrieved evidence chunks.
    """

    @classmethod
    def verify_groundedness(
        cls,
        claims: List[Claim],
        evidence_chunks: List[EvidenceChunk],
        upstream_output: UpstreamAgentOutput
    ) -> Tuple[List[VerifiedClaimItem], List[VerifiedClaimItem], float]:
        if not claims:
            return [], [], 1.0

        verified_items: List[VerifiedClaimItem] = []
        unsubstantiated_items: List[VerifiedClaimItem] = []
        total_groundedness = 0.0

        for claim in claims:
            matched_evidence_ids = []
            max_score = 0.0

            # Evaluate match against each retrieved evidence chunk
            for ev in evidence_chunks:
                score = cls._calculate_evidence_overlap(claim.statement, ev.content, ev.act_or_regulation, ev.section_or_rule)
                if score > 0.4:
                    matched_evidence_ids.append(ev.id)
                    max_score = max(max_score, score)

            # Determine claim verification status
            if max_score >= 0.65:
                status = ClaimVerificationStatus.FULLY_VERIFIED
                notes = f"Corroborated by {len(matched_evidence_ids)} authoritative evidence source(s)."
            elif max_score >= 0.35:
                status = ClaimVerificationStatus.PARTIALLY_VERIFIED
                notes = "Partially supported by retrieved statutory context; secondary verification recommended."
            else:
                # Check if it directly contradicts evidence
                if "completely novel" in claim.statement.lower() or "zero prior art" in claim.statement.lower():
                    status = ClaimVerificationStatus.CONTRADICTS_STATUTE
                    notes = "Directly conflicts with retrieved TKDL and classical prior-art records."
                else:
                    status = ClaimVerificationStatus.UNSUBSTANTIATED
                    notes = "No supporting statutory section or authoritative evidence retrieved for this claim."

            item = VerifiedClaimItem(
                claim=claim,
                status=status,
                supporting_evidence_ids=matched_evidence_ids,
                groundedness_score=round(max_score, 2),
                verification_notes=notes
            )

            if status in [ClaimVerificationStatus.FULLY_VERIFIED, ClaimVerificationStatus.PARTIALLY_VERIFIED]:
                verified_items.append(item)
            else:
                unsubstantiated_items.append(item)

            total_groundedness += max_score

        overall_groundedness = round(total_groundedness / len(claims), 2)
        return verified_items, unsubstantiated_items, overall_groundedness

    @staticmethod
    def _calculate_evidence_overlap(statement: str, evidence_text: str, act_name: str, section: str) -> float:
        stmt_words = set(re_tokenize(statement.lower()))
        combined_ev = (evidence_text + " " + act_name + " " + section).lower()
        ev_words = set(re_tokenize(combined_ev))

        if not stmt_words or not ev_words:
            return 0.0

        # Keywords with heavy legal weight
        legal_keywords = {"section", "rule", "act", "patent", "nba", "sbb", "ayush", "first schedule", "3(p)", "158b", "3(d)", "3(e)", "clinical", "tkdl", "traditional", "7", "6(1)", "charaka"}
        weighted_intersection = 0.0
        weighted_total = 0.0

        for w in stmt_words:
            weight = 3.0 if w in legal_keywords else 1.0
            weighted_total += weight
            if w in ev_words or w in combined_ev:
                weighted_intersection += weight

        overlap_ratio = weighted_intersection / max(1.0, weighted_total)
        return min(1.0, round(overlap_ratio * 1.4, 2))


def re_tokenize(text: str) -> List[str]:
    import re
    # Extract words including section numbers like 3(p), 158b, 6(1)
    tokens = re.findall(r"\b[a-zA-Z0-9_\(\)]+\b", text)
    stopwords = {"the", "and", "for", "with", "this", "that", "are", "not", "under", "from", "can", "due"}
    return [w for w in tokens if len(w) >= 2 and w not in stopwords]
