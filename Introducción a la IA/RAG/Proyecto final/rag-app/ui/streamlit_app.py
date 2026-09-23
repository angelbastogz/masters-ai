"""Streamlit chat UI that lets the user pick Gemini or OpenAI and talk to it.

Flow: load API keys from `.env` -> sidebar lets the user choose a
provider/model and start a new chat -> each prompt is sent to the selected
provider's client (kept in `st.session_state` so it persists across Streamlit
reruns) -> the full message history is re-rendered on every rerun.
"""

import os

import streamlit as st
import requests
from dotenv import find_dotenv, load_dotenv
from google import genai
from openai import OpenAI

MODELS = {
    "Fast API": ["1.0.0"],
    "Gemini": ["gemini-3.6-flash", "gemini-3.7-flash", "gemini-3.8-flash"],
    "OpenAI": ["gpt-5.6-luna", "gpt-4o-mini"],
}
GEMINI_KEY_URL = "https://aistudio.google.com/apikey"
OPENAI_KEY_URL = "https://platform.openai.com/api-keys"
FASTAPI_URL = "http://localhost:8000"

load_dotenv(find_dotenv())
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="RAG - Proyecto final", page_icon="🤖")
st.title("Rag - Proyecto Final")


def missing_key_message(provider: str) -> str:
    """Build the error shown when the selected provider has no API key set."""
    if provider == "Gemini":
        return (
            f"Missing `GEMINI_API_KEY`. Create a key at [{GEMINI_KEY_URL}]({GEMINI_KEY_URL}) "
            "and put it in `.env`."
        )
    return (
        f"Missing `OPENAI_API_KEY`. Create a key at [{OPENAI_KEY_URL}]({OPENAI_KEY_URL}) "
        "and put it in `.env`."
    )


def api_error(provider: str, exc: Exception) -> str:
    """Turn an exception from a provider call into a user-facing chat message."""
    text = str(exc)
    if provider == "Gemini" and "leaked" in text.lower():
        return (
            "This API key was reported as leaked and Google disabled it. "
            f"Create a **new** key at [{GEMINI_KEY_URL}]({GEMINI_KEY_URL}) and put it in "
            "`.env` as `GEMINI_API_KEY`."
        )

    if provider == "Fast API" and isinstance(exc, requests.exceptions.ConnectionError):
        return "no se pudo conectar con la API."

    return f"Could not call {provider}: {exc}"


def reset_chat(provider: str, model: str) -> None:
    """Start a fresh conversation: clear history and create a new client for
    `provider`/`model`, storing everything in `st.session_state` so it survives
    Streamlit's rerun-the-whole-script-on-every-interaction model."""
    st.session_state.provider = provider
    st.session_state.model = model
    st.session_state.messages = []
    if provider == "Gemini":
        client = genai.Client(api_key=GEMINI_API_KEY)
        st.session_state.gemini_chat = client.chats.create(model=model)
        st.session_state.openai_client = None
    elif provider == "OpenAI":
        st.session_state.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        st.session_state.gemini_chat = None
    else:
        st.session_state.openai_client = None
        st.session_state.gemini_chat = None

@st.cache_data(ttl=30)
def check_api_health() -> dict | None:
    """Regresa el JSON de /health, o None si la API no responde."""
    try:
        response = requests.get(f"{FASTAPI_URL}/health", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None


@st.cache_data(ttl=30)
def fetch_sources() -> list[str]:
    """Regresa los `source` distintos indexados en Chroma, o [] si la API no responde."""
    try:
        response = requests.get(f"{FASTAPI_URL}/sources", timeout=5)
        response.raise_for_status()
        return response.json()["sources"]
    except requests.exceptions.RequestException:
        return []

# Sidebar controls. `provider`/`model` are recomputed on every rerun from
# whatever is currently selected in the dropdowns (Streamlit widgets return
# their current value directly, no callbacks needed). "Nuevo chat" forces a
# reset even if provider/model didn't change, then st.rerun() re-executes the
# script immediately so the cleared chat shows up right away.
with st.sidebar:
    provider = st.selectbox("Proveedor", list(MODELS))
    model = st.selectbox("Modelo", MODELS[provider])
    if st.button("Nuevo chat"):
        reset_chat(provider, model)
        st.rerun()

    selected_source = None
    if provider == "Fast API":
        st.divider()

        st.subheader("Buscar en un documento")
        sources = fetch_sources()
        selected_source = st.selectbox(
            "Restringir búsqueda a",
            ["Todos los documentos"] + sources,
        )
        if selected_source == "Todos los documentos":
            selected_source = None

        st.divider()

        st.subheader("Agregar documentos")

        if "uploader_key" not in st.session_state:
            st.session_state.uploader_key = 0

        uploaded_files = st.file_uploader(
            "Sube archivos para indexar",
            type=["md", "txt", "pdf"],
            accept_multiple_files=True,
            key=f"file_uploader_{st.session_state.uploader_key}",
        )

        if uploaded_files and st.button("Subir e indexar"):
            files = [
                ("files", (f.name, f.getvalue(), f.type))
                for f in uploaded_files
            ]
            with st.spinner("Procesando..."):
                try:
                    response = requests.post(f"{FASTAPI_URL}/ingest", files=files, timeout=120)
                    response.raise_for_status()
                    data = response.json()
                    st.success(f"Indexado: {data['documents']} documentos, {data['chunks']} chunks")
                    st.session_state.uploader_key += 1
                    st.rerun()
                except requests.exceptions.RequestException as exc:
                    st.error(f"Error al indexar: {exc}")

        st.divider()

        health = check_api_health()
        if health is None:
            st.error("🔴 API no disponible. ¿Está corriendo `uvicorn app.main:app`?")
        elif health["chroma_status"] == "ok":
            st.success(f"🟢 API conectada — {health['documents']} chunks indexados")
        else:
            st.warning("🟡 API conectada, pero Chroma tiene un problema")

# Block the page instead of calling the API without credentials.
api_key = GEMINI_API_KEY if provider == "Gemini" else OPENAI_API_KEY
if not api_key and provider in ('Gemini', 'OpenAI'):
    reset_chat(provider, model)
    st.error(missing_key_message(provider))
    st.stop()

# Auto-reset when the user switches provider/model via the sidebar (not just
# via the "Nuevo chat" button), and on the very first run of the session.
if (
    st.session_state.get("provider") != provider
    or st.session_state.get("model") != model
    or "messages" not in st.session_state
):
    reset_chat(provider, model)


def reply_from_model(prompt: str) -> tuple[str, list | None]:
    """Send `prompt` to the currently active provider and return its reply text.

    Gemini keeps its own conversation object (`gemini_chat`), so it only needs
    the new prompt. OpenAI's Responses API is stateless per call, so the full
    `st.session_state.messages` history is sent each time to keep context.
    """
    if provider == "Gemini":
        response = st.session_state.gemini_chat.send_message(prompt)
        return response.text or "", None

    if provider == "OpenAI":
        response = st.session_state.openai_client.responses.create(
            model=model,
            input=st.session_state.messages,
        )
        return response.output_text or "", None

    response = requests.post(
        f"{FASTAPI_URL}/query",
        json={"query": prompt, "source": selected_source},
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    return data["answer"], data["citations"]

def render_message(message: dict) -> None:
    """Dibuja el contenido de un mensaje y, si trae citas, su expander."""
    st.markdown(message["content"])
    if message.get("citations"):
        with st.expander(f"📄 Fuentes ({len(message['citations'])})"):
            for c in message["citations"]:
                st.markdown(f"**{c['source']}** — distancia: `{c['score']:.3f}`")
                preview = c["text"][:300] + ("…" if len(c["text"]) > 300 else "")
                st.text(preview)
                st.divider()

# Only render from history so each message appears once (no duplicate on rerun).
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        render_message(message)

# Chat input box pinned to the bottom of the page by Streamlit. Returns None
# until the user submits a message, then returns that message once.
prompt = st.chat_input("Escribe un mensaje")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                reply, citations = reply_from_model(prompt)
            except Exception as exc:
                # Catch-all so a provider/network error becomes a chat message
                # instead of crashing the app.
                reply, citations = api_error(provider, exc), None
            render_message({"content": reply, "citations": citations})

    message = {"role": "assistant", "content": reply}
    if citations:
        message["citations"] = citations
    st.session_state.messages.append(message)
