import asyncio
import wave
from pathlib import Path

import streamlit as st
from celeste_core import Provider, list_models
from celeste_core.enums.capability import Capability
from celeste_text_to_speech import (
    GoogleTTSClient,
    Language,
    list_voice_providers,
    list_voices,
)

st.set_page_config(page_title="Celeste TTS", page_icon="🎵", layout="wide")
st.title("🎵 Celeste Text-to-Speech")

# Get TTS models and voice providers
tts_providers = list_voice_providers()
model_providers = sorted(
    {m.provider for m in list_models(capability=Capability.TEXT_TO_SPEECH)},
    key=lambda p: p.value,
)

with st.sidebar:
    st.header("⚙️ Configuration")

    if model_providers and tts_providers:
        # Provider selection
        provider = st.selectbox(
            "Provider:", [p.value for p in model_providers], format_func=str.title
        )

        # Model selection
        models = list_models(
            provider=Provider(provider), capability=Capability.TEXT_TO_SPEECH
        )
        model_names = [m.display_name or m.id for m in models]
        selected_idx = st.selectbox(
            "Model:", range(len(models)), format_func=lambda i: model_names[i]
        )
        model = models[selected_idx].id

        # Language selection (optional filter)
        st.subheader("🌍 Language & Voice")
        language_options = ["All Languages"] + [lang.value for lang in Language]
        selected_language = st.selectbox("Filter by Language:", language_options)

        # Voice selection based on language filter
        if selected_language == "All Languages":
            available_voices = list_voices(provider=Provider(provider))
        else:
            available_voices = list_voices(
                provider=Provider(provider), language=Language(selected_language)
            )

        if available_voices:
            voice_names = [
                f"{v.display_name} ({v.description})" for v in available_voices
            ]
            selected_voice_idx = st.selectbox(
                "Voice:",
                range(len(available_voices)),
                format_func=lambda i: voice_names[i],
            )
            selected_voice = available_voices[selected_voice_idx]

            # Show voice details
            with st.expander("🎭 Voice Details"):
                st.write(f"**Voice ID:** {selected_voice.id}")
                st.write(f"**Style:** {selected_voice.description}")
                st.write(f"**Languages:** {len(selected_voice.languages)} supported")
                if len(selected_voice.languages) <= 10:
                    langs = ", ".join([lang.value for lang in selected_voice.languages])
                    st.write(f"**Supported:** {langs}")
        else:
            st.error(
                f"No voices found for {provider} with language filter: "
                f"{selected_language}"
            )
            st.stop()

        # Sample rate
        sample_rate = st.selectbox(
            "Sample Rate:", [16000, 22050, 24000, 44100], index=2
        )

    else:
        st.error("No TTS models or voices found. Make sure Google API is configured.")
        st.stop()

st.markdown(f"*Powered by {provider.title()}*")

# Text input
text = st.text_area(
    "Enter text to convert to speech:",
    "Hello! Welcome to Celeste Text-to-Speech. This is a demonstration of our "
    "speech synthesis capabilities.",
    height=150,
    placeholder="Enter any text to convert to speech...",
)

if st.button("🎵 Generate Speech", type="primary", use_container_width=True):
    if not text.strip():
        st.error("Please enter some text to convert to speech.")
    else:

        async def generate_speech() -> None:
            with st.spinner("Generating speech..."):
                try:
                    # Create TTS client
                    client = GoogleTTSClient(model=model)

                    # Generate speech
                    audio_artifact = await client.generate_speech(
                        text=text, voice_name=selected_voice.id, sample_rate=sample_rate
                    )

                    # Save to temporary file for playback
                    temp_file = Path("temp_audio.wav")
                    with wave.open(str(temp_file), "wb") as wf:
                        wf.setnchannels(audio_artifact.channels or 1)
                        wf.setsampwidth(2)  # 16-bit audio
                        wf.setframerate(audio_artifact.sample_rate or sample_rate)
                        wf.writeframes(audio_artifact.data)

                    # Display audio player
                    st.success("✅ Speech generated successfully!")
                    with open(temp_file, "rb") as audio_file:
                        st.audio(audio_file.read(), format="audio/wav")

                    # Show metadata
                    with st.expander("📊 Audio Details"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Format", audio_artifact.format or "wav")
                        with col2:
                            st.metric(
                                "Sample Rate",
                                f"{audio_artifact.sample_rate or sample_rate} Hz",
                            )
                        with col3:
                            st.metric("Channels", audio_artifact.channels or 1)

                    # Cleanup
                    temp_file.unlink(missing_ok=True)

                except Exception as e:
                    st.error(f"Error generating speech: {str(e)}")

        asyncio.run(generate_speech())

st.markdown("---")
st.caption("Built with Streamlit • Powered by Celeste TTS")
