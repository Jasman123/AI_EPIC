import streamlit as st
import whisper
import tempfile
from gtts import gTTS
import os

st.title("🎙 Audio ↔ Text ↔ Audio")

# --- Upload Audio & Transcribe ---
audio_file = st.file_uploader("Upload audio (wav/mp3)", type=["wav", "mp3"])

if audio_file:
    # Simpan sementara audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_file.read())
        temp_audio_path = tmp_file.name

    st.info(f"File audio disimpan sementara: {temp_audio_path}")

    # Load Whisper model
    model = whisper.load_model("small")  # bisa diganti tiny, medium, large

    # Transcribe audio
    result = model.transcribe(temp_audio_path)
    text_output = result["text"]

    st.subheader("📝 Transkripsi Audio:")
    st.write(text_output)

    # --- Text to Speech (gTTS) ---
    if st.button("Convert to Audio"):
        tts = gTTS(text=text_output, lang="id")  # gunakan lang="en" untuk bahasa Inggris
        tts_file = "tts_output.mp3"
        tts.save(tts_file)

        st.audio(tts_file, format="audio/mp3")
        st.success("✅ Text berhasil diubah menjadi audio!")
