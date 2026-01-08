import streamlit as st
import speech_recognition as sr
import tempfile
import os

st.set_page_config(page_title="Audio to Text", page_icon="🎤")
st.title("🎤 Audio to Text (Google SpeechRecognition)")

r = sr.Recognizer()

audio_file = st.file_uploader(
    "Upload or record audio",
    type=["wav"]
)

if audio_file:
    st.audio(audio_file)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        audio_path = tmp.name

    with st.spinner("Transcribing..."):
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)

        try:
            text = r.recognize_google(audio, language="id-ID")
            st.success("Transcription completed")
            st.text_area("Result", text, height=200)

        except sr.UnknownValueError:
            st.error("Could not understand audio")

        except sr.RequestError as e:
            st.error(f"Google API error: {e}")

    os.remove(audio_path)
