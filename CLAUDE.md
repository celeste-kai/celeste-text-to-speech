# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`celeste-text-to-speech` is a domain-specific package within the Celeste AI framework that provides text-to-speech generation capabilities. It follows the standardized Celeste package architecture with provider abstraction, centralized voice management, and comprehensive language support.

## Development Commands

### Environment Setup
```bash
uv sync                    # Install dependencies and set up development environment
```

### Code Quality
```bash
uv run ruff check .        # Run linting
uv run ruff format .       # Apply code formatting
```

### Running Examples
```bash
uv run example.py          # Run the Streamlit TTS demo application
uv run streamlit run example.py  # Alternative way to run Streamlit demo
```

### Package Development
```bash
uv add <package>           # Add new dependency (never use pip install)
uv run -m celeste_text_to_speech  # Run package as module if applicable
```

## Architecture

### Core Components

**Provider System**: Follows Celeste's standardized provider pattern where:
- `mapping.py`: Defines capability (`TEXT_TO_SPEECH`) and maps providers to implementation classes
- `providers/`: Contains provider-specific implementations (currently Google TTS)
- All providers inherit from `BaseTTSClient` in `celeste-core`

**Voice Management**: Centralized voice catalog and registry system:
- `voice_catalog.py`: Static catalog of all available voices with metadata (languages, descriptions, display names)
- `voice_registry.py`: Runtime registry for voice lookup and filtering
- `core/voice.py`: Voice data model with language support checking
- `core/language.py`: Comprehensive language enum using BCP-47 codes

**Client Interface**: `GoogleTTSClient` provides async speech generation with:
- Voice selection from registered voice catalog
- Configurable sample rates (16kHz to 44.1kHz)
- Returns `AudioArtifact` objects with audio data and metadata

### Key Patterns

**Voice Registration**: Voices are automatically loaded from `VOICE_CATALOG` into `VOICE_REGISTRY` on module import, enabling runtime queries by provider, language, or voice characteristics.

**Language Support**: Each voice defines supported languages using the `Language` enum. The system provides filtering capabilities to find voices that support specific languages or providers.

**Provider Integration**: Google TTS integration uses the `google-genai` client with proper authentication via `settings.google.api_key` from `celeste-core` configuration.

## File Structure

```
src/celeste_text_to_speech/
├── __init__.py              # Public API exports
├── mapping.py               # Provider-to-implementation mapping
├── voice_catalog.py         # Static voice definitions
├── voice_registry.py        # Runtime voice management
├── core/
│   ├── language.py          # BCP-47 language codes enum
│   └── voice.py            # Voice data model
└── providers/
    ├── __init__.py
    └── google.py           # Google TTS client implementation
```

## Important Notes

- Always use `uv add` instead of `pip install` for dependency management
- Voice catalog contains 10 Google TTS voices (Zephyr, Puck, Charon, etc.) supporting 23 languages each
- All TTS operations are async and return `AudioArtifact` objects
- The package depends on `celeste-core` for base classes, enums, and configuration
- Ruff is configured with line length 88, Python 3.13 target, and specific lint rules
- Voice characteristics include descriptions like "Bright", "Firm", "Excitable" for UI selection