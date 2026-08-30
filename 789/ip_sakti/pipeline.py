"""
IP-SAKTI Sahayak Pipeline Orchestrator (Layers 7 -> 8 -> 9)
House of Cards Multi-Agent Framework
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

from .core.schema import (
    UpstreamAgentOutput,
    VerificationResult,
    ConfidenceScore,
    MultilingualResponse,
    LanguageCode
)
from .layer_7_verification.verification_agent import VerificationAgent
from .layer_8_confidence.confidence_engine import ConfidenceEngine
from .layer_9_multilingual.localized_formatter import LocalizedFormatter


class PipelineExecutionResult(BaseModel):
    upstream_input: UpstreamAgentOutput
    layer_7_verification: VerificationResult
    layer_8_confidence: ConfidenceScore
    layer_9_response: MultilingualResponse
    execution_status: str = "SUCCESS"


class IPSaktiPipeline:
    """
    Unified Pipeline Orchestrator executing:
    - Layer 7: Verification Agent
    - Layer 8: Confidence & Escalation Engine
    - Layer 9: Multilingual Output Formatter
    """

    def __init__(self):
        self.layer_7 = VerificationAgent()
        self.layer_8 = ConfidenceEngine()
        self.layer_9 = LocalizedFormatter()

    def process(
        self,
        upstream_output: UpstreamAgentOutput,
        target_language: Optional[LanguageCode] = None
    ) -> PipelineExecutionResult:
        """
        Executes the three layers in strict sequential order.
        """
        # Step 1: Execute Layer 7 (Verification)
        verification_result = self.layer_7.verify(upstream_output)

        # Step 2: Execute Layer 8 (Confidence & Escalation)
        confidence_score = self.layer_8.evaluate_confidence(
            upstream_output=upstream_output,
            verification_result=verification_result
        )

        # Step 3: Execute Layer 9 (Multilingual Formatting & Terminology Alignment)
        multilingual_response = self.layer_9.format_response(
            upstream_output=upstream_output,
            verification_result=verification_result,
            confidence_score=confidence_score,
            forced_language=target_language
        )

        return PipelineExecutionResult(
            upstream_input=upstream_output,
            layer_7_verification=verification_result,
            layer_8_confidence=confidence_score,
            layer_9_response=multilingual_response,
            execution_status="SUCCESS"
        )
