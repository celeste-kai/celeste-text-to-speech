from celeste_core.enums.capability import Capability
from celeste_core.enums.providers import Provider

# Capability for this domain package
CAPABILITY: Capability = Capability.TEXT_TO_SPEECH

# Provider wiring for text-to-speech clients
PROVIDER_MAPPING: dict[Provider, tuple[str, str]] = {
    Provider.GOOGLE: (".providers.google", "GoogleTTSClient"),
}

__all__ = ["CAPABILITY", "PROVIDER_MAPPING"]
