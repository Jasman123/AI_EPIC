import streamlit as st
import av
import numpy as np
import wave
import tempfile
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
from faster_whisper import WhisperModel

st.set_page_config(page_title="Live Voice → Text")
st.title("🎙 Live Voice → Text (No Torch, No SciPy)")

@st.cache_resource
def load_model():
    return WhisperModel("base", device="cpu", compute_type="int8")

model = load_model()

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.frames = []

    def recv_audio(self, frame: av.AudioFrame):
        self.frames.append(frame.to_ndarray())
        return frame

ctx = webrtc_streamer(
    key="voice",
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
)

if ctx.audio_processor and st.button("📝 Transcribe"):
    audio = np.concatenate(ctx.audio_processor.frames, axis=1)

    # Convert to mono float32
    audio = audio.mean(axis=0).astype(np.float32)

    # Save WAV (16kHz PCM)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        with wave.open(f.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes((audio * 32767).astype(np.int16).tobytes())

        segments, _ = model.transcribe(f.name)

    text = "".join(seg.text for seg in segments)
    st.success("Done")
    st.write(text)
