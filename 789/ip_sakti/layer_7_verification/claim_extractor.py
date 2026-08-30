"""
Claim Extractor and Proposition Parser
Extracts, structures, and normalizes legal/regulatory propositions from upstream agent synthesis text.
"""

import re
from typing import List
from ..core.schema import Claim, Jurisdiction, UpstreamAgentOutput


class ClaimExtractor:
    """
    Deconstructs agent draft synthesis into discrete legal, regulatory, and patent propositions.
    """

    @classmethod
    def extract_claims_from_output(cls, upstream_output: UpstreamAgentOutput) -> List[Claim]:
        # If upstream output already has extracted claims, validate and enrich them
        if upstream_output.extracted_claims and len(upstream_output.extracted_claims) > 0:
            return upstream_output.extracted_claims

        # Otherwise fallback to regex/rule-based sentence extraction
        claims: List[Claim] = []
        raw_text = upstream_output.synthesis_draft_text
        lines = [line.strip() for line in raw_text.split("\n") if line.strip()]

        claim_idx = 1
        for line in lines:
            # Skip headings
            if line.startswith("#") or len(line) < 20:
                continue

            clean_statement = re.sub(r"^\d+\.\s*", "", line)
            clean_statement = re.sub(r"^\*\*[^*]+\*\*:\s*", "", clean_statement)

            topic = cls._infer_topic(clean_statement)
            associated_cits = cls._find_citation_references(clean_statement, upstream_output)

            claims.append(
                Claim(
                    claim_id=f"CLM-EXT-{claim_idx:02d}",
                    statement=clean_statement,
                    associated_citations=associated_cits,
                    domain_topic=topic,
                    target_jurisdiction=upstream_output.target_jurisdiction
                )
            )
            claim_idx += 1

        return claims

    @staticmethod
    def _infer_topic(statement: str) -> str:
        s_lower = statement.lower()
        if any(k in s_lower for k in ["patent", "novelty", "inventive step", "section 3(p)", "section 3(d)", "35 u.s.c"]):
            return "Patentability"
        elif any(k in s_lower for k in ["license", "rule 158b", "form 25d", "gmp", "schedule t", "ayush"]):
            return "Manufacturing License"
        elif any(k in s_lower for k in ["nba", "sbb", "biodiversity", "abs", "biological resource", "section 6"]):
            return "ABS Compliance"
        elif any(k in s_lower for k in ["clinical", "trial", "toxicity", "safety", "cdsco"]):
            return "Clinical Trials"
        elif any(k in s_lower for k in ["trademark", "gi", "geographical indication"]):
            return "Trademarks & GI"
        return "General Regulatory"

    @staticmethod
    def _find_citation_references(statement: str, upstream_output: UpstreamAgentOutput) -> List[str]:
        cit_ids = []
        for cit in upstream_output.citations_referenced:
            # Look for Section/Rule references or Act names in the statement
            sec = cit.section_or_rule.lower()
            if sec and sec in statement.lower():
                cit_ids.append(cit.citation_id)
        return cit_ids
