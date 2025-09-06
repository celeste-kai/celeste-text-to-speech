import asyncio
import wave
from pathlib import Path
from typing import cast

import streamlit as st
from celeste_core import AudioArtifact, Provider, list_models
from celeste_core.enums.capability import Capability

from celeste_text_to_speech import (
    GoogleTTSClient,
    Language,
    Voice,
    list_voice_providers,
    list_voices,
)


def setup_sidebar_config() -> tuple[str, str, Voice, int]:
    """Setup sidebar configuration and return selected parameters."""
    tts_providers = list_voice_providers()
    model_providers = sorted(
        {m.provider for m in list_models(capability=Capability.TEXT_TO_SPEECH)},
        key=lambda p: p.value,
    )

    with st.sidebar:
        st.header("⚙️ Configuration")

        if not model_providers or not tts_providers:
            st.error("No TTS models or voices found. Make sure Google API is configured.")
            st.stop()

        provider = st.selectbox("Provider:", [p.value for p in model_providers], format_func=str.title)
        models = list_models(provider=Provider(provider), capability=Capability.TEXT_TO_SPEECH)
        model_names = [m.display_name or m.id for m in models]
        selected_idx = st.selectbox("Model:", range(len(models)), format_func=lambda i: model_names[i])
        model = models[selected_idx].id

        selected_voice = setup_voice_selection(provider)
        sample_rate = st.selectbox("Sample Rate:", [16000, 22050, 24000, 44100], index=2)

    return provider, model, selected_voice, sample_rate


def setup_voice_selection(provider: str) -> Voice:
    """Setup voice selection UI and return selected voice."""
    st.subheader("🌍 Language & Voice")
    language_options = ["All Languages"] + [lang.value for lang in Language]
    selected_language = st.selectbox("Filter by Language:", language_options)

    if selected_language == "All Languages":
        available_voices = list_voices(provider=Provider(provider))
    else:
        available_voices = list_voices(provider=Provider(provider), language=Language(selected_language))

    if not available_voices:
        st.error(f"No voices found for {provider} with language filter: {selected_language}")
        st.stop()

    voice_names = [f"{v.display_name} ({v.description})" for v in available_voices]
    selected_voice_idx = st.selectbox(
        "Voice:",
        range(len(available_voices)),
        format_func=lambda i: voice_names[i],
    )
    selected_voice: Voice = available_voices[selected_voice_idx]

    display_voice_details(selected_voice)
    return selected_voice


def display_voice_details(voice: Voice) -> None:
    """Display voice details in an expander."""
    with st.expander("🎭 Voice Details"):
        st.write(f"**Voice ID:** {voice.id}")
        st.write(f"**Style:** {voice.description}")
        st.write(f"**Languages:** {len(voice.languages)} supported")
        if len(voice.languages) <= 10:
            langs = ", ".join([lang.value for lang in voice.languages])
            st.write(f"**Supported:** {langs}")


def save_audio_artifact(audio_artifact: AudioArtifact, sample_rate: int) -> Path:
    """Save audio artifact to temporary file for playback."""
    temp_file = Path("temp_audio.wav")
    with wave.open(str(temp_file), "wb") as wf:
        wf.setnchannels(audio_artifact.channels or 1)
        wf.setsampwidth(2)
        wf.setframerate(audio_artifact.sample_rate or sample_rate)
        wf.writeframes(audio_artifact.data)
    return temp_file


def display_audio_results(
    temp_file: Path, provider: str, model: str, selected_voice: Voice, audio_artifact: AudioArtifact, sample_rate: int
) -> None:
    """Display audio player and metadata."""
    st.success("✅ Speech generated successfully!")
    with open(temp_file, "rb") as audio_file:
        st.audio(audio_file.read(), format="audio/wav")

    with st.expander("📊 Details"):
        st.write(f"**Provider:** {provider}")
        st.write(f"**Model:** {model}")
        st.write(f"**Voice:** {selected_voice.display_name}")
        st.write(f"**Sample Rate:** {audio_artifact.sample_rate or sample_rate} Hz")
        st.write(f"**Channels:** {audio_artifact.channels or 1}")
        st.write(f"**Format:** {audio_artifact.format or 'wav'}")


async def generate_and_play_speech(
    text: str, model: str, selected_voice: Voice, sample_rate: int, provider: str
) -> None:
    """Generate speech and display audio player."""
    client = GoogleTTSClient(model=model)
    audio_artifact = await client.generate_speech(text=text, voice_name=selected_voice.id, sample_rate=sample_rate)

    temp_file = save_audio_artifact(audio_artifact, sample_rate)
    display_audio_results(temp_file, provider, model, selected_voice, audio_artifact, sample_rate)
    temp_file.unlink(missing_ok=True)


def setup_main_ui() -> str:
    """Setup main UI elements and return text input."""
    st.set_page_config(page_title="Celeste TTS", page_icon="🎵", layout="wide")
    st.title("🎵 Celeste Text-to-Speech")

    return cast(
        str,
        st.text_area(
            "Enter text to convert to speech:",
            "Hello! Welcome to Celeste Text-to-Speech. This is a demonstration of our speech synthesis capabilities.",
            height=150,
            placeholder="Enter any text to convert to speech...",
        ),
    )


async def handle_speech_generation(
    text: str, model: str, selected_voice: Voice, sample_rate: int, provider: str
) -> None:
    """Handle speech generation with error handling."""
    if not text.strip():
        st.error("Please enter some text to convert to speech.")
        return

    with st.spinner("Generating speech..."):
        try:
            await generate_and_play_speech(text, model, selected_voice, sample_rate, provider)
        except Exception as e:
            st.error(f"Error generating speech: {str(e)}")


def show_footer() -> None:
    """Display footer section."""
    st.markdown("---")
    st.caption("Built with Streamlit • Powered by Celeste")


async def main() -> None:
    text = setup_main_ui()

    provider, model, selected_voice, sample_rate = setup_sidebar_config()
    st.markdown(f"*Powered by {provider.title()}*")

    if st.button("🎵 Generate Speech", type="primary", use_container_width=True):
        await handle_speech_generation(text, model, selected_voice, sample_rate, provider)

    show_footer()


if __name__ == "__main__":
    asyncio.run(main())
