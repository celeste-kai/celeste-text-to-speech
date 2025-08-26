from __future__ import annotations

from enum import Enum


class Language(str, Enum):
    """Supported languages for TTS with BCP-47 codes."""

    ARABIC_EGYPT = "ar-EG"  # Arabic (Egypt)
    GERMAN_GERMANY = "de-DE"  # German (Germany)
    ENGLISH_US = "en-US"  # English (United States)
    SPANISH_US = "es-US"  # Spanish (United States)
    FRENCH_FRANCE = "fr-FR"  # French (France)
    HINDI_INDIA = "hi-IN"  # Hindi (India)
    INDONESIAN_INDONESIA = "id-ID"  # Indonesian (Indonesia)
    ITALIAN_ITALY = "it-IT"  # Italian (Italy)
    JAPANESE_JAPAN = "ja-JP"  # Japanese (Japan)
    KOREAN_KOREA = "ko-KR"  # Korean (Korea)
    PORTUGUESE_BRAZIL = "pt-BR"  # Portuguese (Brazil)
    RUSSIAN_RUSSIA = "ru-RU"  # Russian (Russia)
    DUTCH_NETHERLANDS = "nl-NL"  # Dutch (Netherlands)
    POLISH_POLAND = "pl-PL"  # Polish (Poland)
    THAI_THAILAND = "th-TH"  # Thai (Thailand)
    TURKISH_TURKEY = "tr-TR"  # Turkish (Turkey)
    VIETNAMESE_VIETNAM = "vi-VN"  # Vietnamese (Vietnam)
    ROMANIAN_ROMANIA = "ro-RO"  # Romanian (Romania)
    UKRAINIAN_UKRAINE = "uk-UA"  # Ukrainian (Ukraine)
    BENGALI_BANGLADESH = "bn-BD"  # Bengali (Bangladesh)
    ENGLISH_INDIA = "en-IN"  # English (India) - Pack with hi-IN
    MARATHI_INDIA = "mr-IN"  # Marathi (India)
    TAMIL_INDIA = "ta-IN"  # Tamil (India)
    TELUGU_INDIA = "te-IN"  # Telugu (India)
