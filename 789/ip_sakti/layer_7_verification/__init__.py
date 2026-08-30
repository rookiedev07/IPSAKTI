"""
Layer 7: Verification Agent
Ensures claims are substantiated by verified citations, statutory rules,
jurisdiction context, and free of contradictions and hallucinations.
"""

from .verification_agent import VerificationAgent

__all__ = ["VerificationAgent"]
