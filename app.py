import streamlit as st
from dotenv import load_dotenv
from graph_model import build_graph
from uuid import uuid4

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="PDF Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("📄 RAG EPIC Project by Jasman")

# Initialize graph once
@st.cache_resource
def init_graph():
    return build_graph()

graph = init_graph()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask something about the PDF...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        result = graph.invoke({
            "messages": st.session_state.messages
        }, config={"configurable": {"thread_id": st.session_state.thread_id}})

        assistant_reply = result["messages"][-1].content
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
