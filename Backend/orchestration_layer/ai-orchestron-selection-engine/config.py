"""
Central config for the AI Selection & Decision Engine.
Configured for Groq-powered high-speed LPU inference.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODELS_LIST_PATH = os.path.join(BASE_DIR, "data", "models_list.json")

# The default fallback model on Groq
FALLBACK_MODEL_ID = "groq/compound-mini"
FALLBACK_PROVIDER = "Groq"

# Tier -> numeric score used by the scoring engine
QUALITY_TIER_SCORES = {
    "frontier": 1.0,
    "high": 0.80,
    "medium": 0.55,
    "budget": 0.30,
}

# Cost is inverted: very_low cost = 1.0
COST_TIER_SCORES = {
    "very_low": 1.0,
    "low": 0.8,
    "medium": 0.6,
    "high": 0.4,
    "very_high": 0.2,
}

SPEED_TIER_SCORES = {
    "very_fast": 1.0,
    "fast": 0.85,
    "medium": 0.60,
    "slow": 0.30,
}

# Weight profiles per card role / prompt category
CRITERIA_WEIGHTS = {
    # Ace ♠ (Strategist): Heavy quality & reasoning emphasis
    "reasoning":         {"quality": 0.55, "cost": 0.10, "speed": 0.15, "context": 0.20},
    # 2 ♥ (Researcher): Heavy context window & retrieval speed emphasis
    "research":          {"quality": 0.35, "cost": 0.10, "speed": 0.25, "context": 0.30},
    # 3 ♦ (Architect): Balanced frontier architecture & schema design
    "general":           {"quality": 0.50, "cost": 0.10, "speed": 0.20, "context": 0.20},
    # 4 ♣ (Executor): Algorithmic code synthesis & high quality
    "coding":            {"quality": 0.55, "cost": 0.10, "speed": 0.25, "context": 0.10},
    # 5 ♠ (Verifier): Ultra-fast validation, assertions & lightweight QA
    "cheap_fast":        {"quality": 0.15, "cost": 0.35, "speed": 0.45, "context": 0.05},
    # Security / Guardrails
    "security":          {"quality": 0.45, "cost": 0.15, "speed": 0.30, "context": 0.10},
}

DEFAULT_CATEGORY = "general"

# Context window normalization cap (tokens) — 131k is standard on Groq
CONTEXT_WINDOW_CAP = 131_072

# Real API call settings for Groq
ENABLE_REAL_GROQ_CALLS = True
DEFAULT_GROQ_MODEL = "qwen/qwen3.6-27b"
