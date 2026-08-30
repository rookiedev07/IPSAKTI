"""
This is the CONTRACT with Teammate 1 (Prompt Matching Engine).
This is what YOU expect to receive from their module.

This is a mock/best-guess schema for now -- once Teammate 1 finalizes their
real output format, only this file should need to change. Nothing in
engine/ or api_layer/ should ever import raw dicts directly; always go
through PromptInput so the rest of your code stays stable.
"""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class UserPreferences(BaseModel):
    # "auto"  -> engine decides the best model on its own
    # "manual" -> user wants to browse/pick from the 50-model list themselves
    mode: str = Field(default="auto", description="'auto' or 'manual'")

    # Optional hint from the user on what matters most to them.
    # One of: "quality", "cost", "speed", "context"
    priority: Optional[str] = None

    # If mode == "manual" and the user already picked a model id directly.
    manual_model_id: Optional[str] = None


class PromptInput(BaseModel):
    prompt_id: str
    original_prompt: str

    # The best-matched, pre-engineered prompt from Teammate 1's matching engine.
    matched_prompt: str

    # Detected task category, e.g. "coding", "creative_writing", "research",
    # "reasoning", "cheap_fast", "general". Falls back to "general" if absent.
    category: Optional[str] = None

    # Any extra tags Teammate 1's engine attaches (freeform, optional).
    tags: List[str] = Field(default_factory=list)

    user_preferences: UserPreferences = Field(default_factory=UserPreferences)

    # Passthrough bucket for anything else Teammate 1 sends that you don't
    # use yet -- keeps you from breaking if their schema grows.
    extra: Dict = Field(default_factory=dict)
