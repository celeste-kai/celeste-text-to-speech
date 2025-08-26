from typing import Any

from celeste_core import AudioArtifact, Provider
from celeste_core.base.tts_client import BaseTTSClient
from celeste_core.config.settings import settings
from google import genai
from google.genai import types


class GoogleTTSClient(BaseTTSClient):
    def __init__(
        self, model: str = "gemini-2.5-flash-preview-tts", **kwargs: Any
    ) -> None:
        super().__init__(model=model, provider=Provider.GOOGLE, **kwargs)
        self.client = genai.Client(api_key=settings.google.api_key)

    async def generate_speech(
        self,
        text: str,
        voice_name: str,
        sample_rate: int = 24000,
        **kwargs: Any,
    ) -> AudioArtifact:
        """Generate speech from text using Google's TTS API.

        Args:
            text: The text to convert to speech
            voice_name: Voice to use - REQUIRED, no fallback
            sample_rate: Audio sample rate in Hz
            **kwargs: Additional generation parameters

        Returns:
            AudioArtifact with audio data
        """
        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice_name,
                        )
                    )
                ),
            ),
            **kwargs,
        )

        # Extract audio data from the response
        audio_data = response.candidates[0].content.parts[0].inline_data.data

        return AudioArtifact(
            data=audio_data,
            format="wav",
            sample_rate=sample_rate,
            channels=1,  # Mono by default
        )
