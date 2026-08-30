"""
Layer 8: Confidence & Human Escalation Layer
Calculates multi-factor confidence, handles safe refusals,
and generates structured legal escalation dossiers when professional human review is required.
"""

from .confidence_engine import ConfidenceEngine

__all__ = ["ConfidenceEngine"]
