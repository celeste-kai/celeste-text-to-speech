from __future__ import annotations

from celeste_core.enums.providers import Provider

from .core.language import Language
from .core.voice import Voice
from .voice_catalog import VOICE_CATALOG

# Central registry mapping (provider, voice_id) to voice metadata.
VOICE_REGISTRY: dict[tuple[Provider, str], Voice] = {}


def register_voice(voice: Voice) -> None:
    """Register or update a voice entry in the registry."""
    VOICE_REGISTRY[(voice.provider, voice.id)] = voice


def clear_voice_registry() -> None:
    """Clear all registered voices."""
    VOICE_REGISTRY.clear()


def get_voice(provider: Provider, voice_id: str) -> Voice | None:
    """Get a specific voice by provider and ID."""
    return VOICE_REGISTRY.get((provider, voice_id))


def list_voices(*, provider: Provider | None = None, language: Language | None = None) -> list[Voice]:
    """List voices, optionally filtered by provider and/or language support."""
    voices = list(VOICE_REGISTRY.values())

    if provider is not None:
        voices = [v for v in voices if v.provider == provider]

    if language is not None:
        voices = [v for v in voices if v.supports_language(language)]

    return voices


def list_voice_providers(*, language: Language | None = None) -> list[Provider]:
    """Return distinct providers, optionally filtered by language support."""
    if language is None:
        return sorted(
            {provider for (provider, _voice_id) in VOICE_REGISTRY},
            key=lambda p: p.value,
        )

    supported_voices = list_voices(language=language)
    providers = {v.provider for v in supported_voices}
    return sorted(providers, key=lambda p: p.value)


def voice_supports_language(provider: Provider, voice_id: str, language: Language) -> bool:
    """Check if a specific voice supports a language."""
    voice = get_voice(provider, voice_id)
    return bool(voice and voice.supports_language(language))


# -----------------------------
# Seed registry with known voices
# -----------------------------


def reload_voice_catalog() -> None:
    """Reload the built-in voice catalog into the registry."""
    clear_voice_registry()
    for voice in VOICE_CATALOG:
        register_voice(voice)


__all__ = [
    "VOICE_REGISTRY",
    "get_voice",
    "list_voices",
    "list_voice_providers",
    "voice_supports_language",
    "register_voice",
    "clear_voice_registry",
    "reload_voice_catalog",
]

# Load built-in catalog on import so the registry is usable by default.
reload_voice_catalog()
