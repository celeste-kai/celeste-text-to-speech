"""Celeste Text-to-Speech: Convert text to natural speech audio."""

from .core.language import Language
from .core.voice import Voice
from .mapping import CAPABILITY, PROVIDER_MAPPING
from .providers.google import GoogleTTSClient
from .voice_registry import (
    get_voice,
    list_voice_providers,
    list_voices,
    voice_supports_language,
)

__all__ = [
    "GoogleTTSClient",
    "CAPABILITY",
    "PROVIDER_MAPPING",
    "Voice",
    "Language",
    "get_voice",
    "list_voices",
    "list_voice_providers",
    "voice_supports_language",
]
