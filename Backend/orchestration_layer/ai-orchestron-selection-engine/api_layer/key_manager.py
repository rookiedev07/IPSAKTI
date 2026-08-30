"""
API Key Handling & Provider Key Management.
Automatically detects Groq HOC_KEY from environment.
"""

import os
from typing import Optional, Dict
from config import FALLBACK_PROVIDER


class KeyManager:
    def __init__(self):
        # provider name -> api key string
        self._keys: Dict[str, str] = {}
        # Auto-load HOC_KEY if present in environment
        env_hoc_key = os.getenv("HOC_KEY", "")
        if env_hoc_key:
            self._keys["Groq"] = env_hoc_key
            self._keys["Google"] = env_hoc_key

    def add_key(self, provider: str, key: str) -> None:
        if not key or not key.strip():
            raise ValueError(f"Empty API key provided for {provider}.")
        self._keys[provider] = key.strip()

    def has_key(self, provider: str) -> bool:
        return provider in self._keys and bool(self._keys[provider])

    def get_key(self, provider: str) -> Optional[str]:
        return self._keys.get(provider) or self._keys.get("Groq")

    def has_fallback_key(self) -> bool:
        return self.has_key(FALLBACK_PROVIDER) or self.has_key("Groq")

    def load_bulk(self, keys: Dict[str, str]) -> None:
        """Convenience for loading multiple keys at once."""
        for provider, key in keys.items():
            if key:
                self.add_key(provider, key)
