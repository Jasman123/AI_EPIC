import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from graph_model import build_graph
from uuid import uuid4
from gtts import gTTS

load_dotenv()
st.set_page_config(page_title="PDF Chatbot", page_icon="🤖", layout="centered")
st.title("📄 RAG EPIC Project by Jasman")

@st.cache_resource
def init_graph():
    return build_graph()

graph = init_graph()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "language" not in st.session_state:
    st.session_state.language = "en"

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask something about the PDF...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        result = graph.invoke(
            {"messages": st.session_state.messages},
            config={"configurable": {"thread_id": st.session_state.thread_id}}
        )

        assistant_reply = result["messages"][-1].content

    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
    if st.session_state.language == "en":
        assistant_reply = st.session_state.messages[-1]["content"]
        tts = gTTS(text=assistant_reply, lang="en")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tts.save(tmp_file.name)
            audio_path = tmp_file.name
        with open(audio_path, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")
        os.remove(audio_path)


        