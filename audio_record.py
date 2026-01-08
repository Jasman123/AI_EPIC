import streamlit as st
import whisper

st.title("🎙 Speech Recognition")

audio_file = st.file_uploader("Upload audio", type=["wav", "mp3"])

if audio_file:
    model = whisper.load_model("small")
    result = model.transcribe(audio_file)
    st.write(result["text"])
