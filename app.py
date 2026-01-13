import os
import uuid
import streamlit as st

from config.config import APP_TITLE, ENABLE_VOICE_INPUT
from src.indexing.indexer import build_or_load_index
from src.rag.retriever import Retriever
from src.rag.qa_chain import QAChain
from src.llm.openai_client import OpenAIClient
from src.voice.speech_to_text import listen_from_mic


# =========================
# Streamlit Page Config
# =========================

st.set_page_config(page_title=APP_TITLE, layout="wide")
st.title(APP_TITLE)


# =========================
# One-time Backend Init
# =========================

if "vector_store" not in st.session_state:
    (
    st.session_state.vector_store,
    st.session_state.embedder,
    st.session_state.unique_funds,
) = build_or_load_index()


if "llm" not in st.session_state:
    st.session_state.llm = OpenAIClient(
        api_key=os.getenv("OPENAI_API_KEY")
    )

if "retriever" not in st.session_state:
    st.session_state.retriever = Retriever(
        vector_store=st.session_state.vector_store,
        embedder=st.session_state.embedder,
        unique_funds=st.session_state.unique_funds
    )

if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = QAChain(
        retriever=st.session_state.retriever,
        llm_client=st.session_state.llm
    )


# =========================
# Chat State Initialization
# =========================

if "chats" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.chats = {
        chat_id: {
            "name": "New Chat",
            "messages": []
        }
    }
    st.session_state.active_chat_id = chat_id

if "renaming_chat_id" not in st.session_state:
    st.session_state.renaming_chat_id = None


# =========================
# Sidebar - Chat Management
# =========================

st.sidebar.header("Chats")

# New Chat
if st.sidebar.button("➕ New Chat"):
    new_chat_id = str(uuid.uuid4())
    st.session_state.chats[new_chat_id] = {
        "name": "New Chat",
        "messages": []
    }
    st.session_state.active_chat_id = new_chat_id
    st.session_state.renaming_chat_id = None

st.sidebar.divider()

# Chat List with inline rename
for chat_id, chat_data in st.session_state.chats.items():
    is_active = chat_id == st.session_state.active_chat_id

    col1, col2 = st.sidebar.columns([0.85, 0.15])

    with col1:
        if st.session_state.renaming_chat_id == chat_id:
            new_name = st.text_input(
                "",
                value=chat_data["name"],
                key=f"rename_input_{chat_id}",
                label_visibility="collapsed"
            )
            chat_data["name"] = new_name
        else:
            if st.button(chat_data["name"], key=f"chat_{chat_id}"):
                st.session_state.active_chat_id = chat_id
                st.session_state.renaming_chat_id = None

    with col2:
        if is_active:
            if st.button("✏️", key=f"edit_{chat_id}"):
                st.session_state.renaming_chat_id = chat_id

st.sidebar.divider()

# Voice Settings
st.sidebar.header("Voice Settings")
use_voice_input = False
if ENABLE_VOICE_INPUT:
    use_voice_input = st.sidebar.checkbox("🎙️ Voice Input")


# =========================
# Main Chat Window
# =========================

chat = st.session_state.chats[st.session_state.active_chat_id]

# Display Chat History
for message in chat["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================
# User Input (Text + Voice)
# =========================

user_input = None

if use_voice_input:
    if st.button("🎙️ Speak"):
        with st.spinner("Listening..."):
            spoken_text = listen_from_mic()

        if spoken_text:
            user_input = spoken_text
            st.success(f"You said: {spoken_text}")
        else:
            st.warning("Could not understand audio.")

if not user_input:
    user_input = st.chat_input("Ask about holdings or trades...")


# =========================
# RAG Answer Flow
# =========================

if user_input:
    chat["messages"].append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("thinking... 🧠"):
            answer = st.session_state.qa_chain.answer(user_input)
        st.markdown(answer)

    chat["messages"].append(
        {"role": "assistant", "content": answer}
    )
