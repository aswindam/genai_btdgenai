"""Health Assistant chat page.

Rendered with Streamlit's native chat primitives (``st.chat_message`` /
``st.chat_input``) and backed by the Azure AI Foundry model exposed through
``llm.py``.
"""

import base64
import os

import streamlit as st

try:  # imported as part of the ``app`` package (streamlit_app.py entry point)
    from app import llm
except ImportError:  # run directly from inside the app/ directory
    import llm

SYSTEM_PROMPT = """You are a knowledgeable, empathetic assistant specialised in brain tumours.
Answer questions about brain tumours, scans and reports, symptoms, diagnosis,
treatment options and next steps. Use clear headings and short bullet points.
Be supportive and easy to understand for a non-medical reader.
Always remind the user to confirm anything important with a qualified clinician.
If a question is unrelated to health, politely steer the conversation back.
"""

GREETING_KEYS = ['hey', 'hello', 'hi ', 'hi!', 'hi.', 'hiya', 'good morning', 'good evening']
UNRELATED_KEYWORDS = ['movie', 'music', 'series', 'tv show', 'netflix', 'cricket', 'football']

WELCOME = ("Hello! I'm your brain tumour assistant. Ask me about symptoms, scans, "
           "reports, treatment options or next steps.")
REFUSAL = ("Sorry, I can't help with movies, music, series or sport. "
           "I'm here for brain tumour and health related questions.")

GOOD_NEWS_KEYS = ['no tumor', 'no tumour', 'positive result', 'no tumor found',
                  'no symptoms', 'no brain tumor', 'benign']

USER_AVATAR = "🧑"
BOT_AVATAR = "🧠"

SUGGESTIONS = [
    "What are the common symptoms of a brain tumour?",
    "Explain the difference between benign and malignant tumours",
    "What should I ask my doctor after an MRI?",
]


def _background_css(image_path="app/Chatbot.png"):
    """Background image plus a dark scrim so the text stays readable."""
    try:
        image_base64 = base64.b64encode(open(image_path, "rb").read()).decode()
        background = f"url('data:image/png;base64,{image_base64}')"
    except OSError:
        background = "none"

    return f"""
        <style>
            .stApp {{
                background-image: linear-gradient(rgba(6, 12, 28, 0.88), rgba(6, 12, 28, 0.94)), {background};
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            /* Chat bubbles */
            [data-testid="stChatMessage"] {{
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.10);
                border-radius: 14px;
                padding: 0.85rem 1.05rem;
                margin-bottom: 0.65rem;
                backdrop-filter: blur(6px);
            }}
            [data-testid="stChatMessage"] p,
            [data-testid="stChatMessage"] li,
            [data-testid="stChatMessage"] h1,
            [data-testid="stChatMessage"] h2,
            [data-testid="stChatMessage"] h3,
            [data-testid="stChatMessage"] strong {{
                color: #EAF2FF !important;
            }}
            /* Input bar */
            [data-testid="stChatInput"] {{
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(120, 180, 255, 0.35);
                border-radius: 12px;
            }}
            .assist-title {{
                color: #7FC4FF;
                text-shadow: 0 3px 10px rgba(0, 0, 0, 0.75);
                margin-bottom: 0.1rem;
            }}
            .assist-sub {{
                color: #B9C9E0;
                margin-top: 0;
                font-size: 0.95rem;
            }}
        </style>
    """


def _classify(query):
    """Return 'offtopic', 'greeting' or 'answer' for the given query."""
    text = query.lower().strip()

    if any(keyword in text for keyword in UNRELATED_KEYWORDS):
        return 'offtopic'

    # A bare greeting (no real question attached) just gets the welcome text.
    padded = f" {text} "
    if any(keyword in padded for keyword in GREETING_KEYS) and len(text.split()) <= 4:
        return 'greeting'

    return 'answer'


def _render_history():
    for message in st.session_state['messages']:
        avatar = USER_AVATAR if message['role'] == 'user' else BOT_AVATAR
        with st.chat_message(message['role'], avatar=avatar):
            st.markdown(message['content'])


def _answer(prompt):
    """Stream the model reply, persisting it to the conversation."""
    with st.chat_message('assistant', avatar=BOT_AVATAR):
        placeholder = st.empty()
        reply = ''
        try:
            for chunk in llm.stream_chat(st.session_state['messages'], system=SYSTEM_PROMPT):
                reply += chunk
                placeholder.markdown(reply + '▌')
            placeholder.markdown(reply or '_No response received._')
        except Exception as exc:  # noqa: BLE001 - surfaced to the user
            placeholder.error(f"Sorry, the assistant is unavailable right now.\n\n`{exc}`")
            return None

    return reply


def _handle(prompt):
    """Append the user turn, produce a reply and store it."""
    st.session_state['messages'].append({'role': 'user', 'content': prompt})
    with st.chat_message('user', avatar=USER_AVATAR):
        st.markdown(prompt)

    kind = _classify(prompt)

    if kind == 'offtopic':
        reply = REFUSAL
        with st.chat_message('assistant', avatar=BOT_AVATAR):
            st.warning(REFUSAL)
    elif kind == 'greeting':
        reply = WELCOME
        with st.chat_message('assistant', avatar=BOT_AVATAR):
            st.markdown(WELCOME)
    else:
        reply = _answer(prompt)

    if reply:
        st.session_state['messages'].append({'role': 'assistant', 'content': reply})

        if any(keyword in prompt.lower() for keyword in GOOD_NEWS_KEYS):
            st.success("That's wonderful news about your scan results! 🎉")
            st.balloons()


def code():
    st.markdown(_background_css(), unsafe_allow_html=True)

    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # ---------------- Header ----------------
    st.markdown("<h1 class='assist-title'>Health Assistant 💬</h1>", unsafe_allow_html=True)
    st.markdown("<p class='assist-sub'>Ask me anything about brain tumours, scans, symptoms or treatment.</p>",
                unsafe_allow_html=True)

    # ---------------- Sidebar ----------------
    with st.sidebar:
        st.title("Health Assistant 💬")
        st.caption(f"{len(st.session_state['messages'])} messages in this conversation")

        if st.button("🗑️ Clear chat", use_container_width=True):
            st.session_state['messages'] = []
            st.rerun()

        st.markdown("### How to use")
        st.markdown(
            "- Type your question in the box at the bottom\n"
            "- Press **Enter** to send\n"
            "- The full conversation stays on screen\n"
            "- Use **Clear chat** to start over"
        )
        st.info("Educational information only - always confirm with a qualified clinician.")

    # ---------------- Conversation ----------------
    _render_history()

    pending = None

    # Starter prompts, shown only on an empty conversation.
    if not st.session_state['messages']:
        st.markdown("###### Try one of these")
        for index, column in enumerate(st.columns(len(SUGGESTIONS))):
            with column:
                if st.button(SUGGESTIONS[index], key=f"suggestion_{index}", use_container_width=True):
                    pending = SUGGESTIONS[index]

    typed = st.chat_input("Ask about symptoms, scans, reports or treatment...")
    prompt = typed or pending

    if prompt:
        _handle(prompt)
        # Redraw so the starter buttons disappear once a chat has begun.
        if pending:
            st.rerun()


if __name__ == "__main__":
    code()
