from __future__ import annotations

from typing import List

from celeste_core.enums.providers import Provider
from pydantic import BaseModel

from .language import Language


class Voice(BaseModel):
    """Represents a TTS voice with its characteristics."""

    id: str
    provider: Provider
    languages: List[Language]  # Supported languages using Language enum
    description: str  # Voice characteristics (e.g., "Firm", "Bright", "Excitable")
    display_name: str  # Human-readable name for UI

    def supports_language(self, language: Language) -> bool:
        """Check if voice supports a specific language."""
        return language in self.languages
