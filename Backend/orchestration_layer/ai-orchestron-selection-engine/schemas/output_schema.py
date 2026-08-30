"""
This is the CONTRACT with Teammate 2 (Output structuring / main-screen card).
This is what YOU promise to send them.

Matches Task 4 (problem / solution / AIs used in detail) and Task 5
(main-screen card needs to know which AI was used) from the project brief.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ModelSummary(BaseModel):
    id: str
    name: str
    provider: str
    quality_tier: str
    cost_tier: str
    speed_tier: str


class AlternativeChoice(BaseModel):
    model: ModelSummary
    score: float
    reason_not_chosen: Optional[str] = None


class SelectionOutput(BaseModel):
    prompt_id: str

    # For Task 4's "output structure": what was the problem, what's the solution
    problem: str
    solution: str

    # The model actually used to answer (after fallback resolution, if any)
    selected_model: ModelSummary

    # Why this model was picked -- shown in the detailed output view
    reasoning: str

    # Score breakdown is optional so the schema is safe for anyone consuming
    # the API in the future.
    score: float

    # Raw quality/cost/speed/context contribution (0-1 each, before weighting) --
    # what the UI's mixer-bar visualization is built from.
    score_breakdown: dict = Field(default_factory=dict)

    # Runner-up models the engine considered
    alternatives: List[AlternativeChoice] = Field(default_factory=list)

    # True if the originally chosen model had no API key and Gemini was used instead
    fallback_used: bool = False

    # "ok", "missing_key", "fallback_missing_key" etc.
    api_key_status: str = "ok"

    # Raw response text from the AI (mocked until real API calls are wired in)
    response_text: str = ""
