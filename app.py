import streamlit as st
import chatbot
import html
import textwrap


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CodeBuddy PRO",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# HTML RENDER HELPER
# (Defined early, before it's first used, to avoid NameError)
# ============================================================

def render_html(content):
    """
    st.markdown with unsafe_allow_html=True treats any line that starts
    with 4+ leading spaces as a Markdown code block, which breaks HTML
    rendering whenever this is called from inside an indented block
    (e.g. inside `with st.sidebar:` or `with col1:`), OR whenever nested
    tags are indented deeper than their parent (e.g. a label div nested
    inside a card div). textwrap.dedent() only removes the *common*
    leading whitespace, so deeper-nested lines can still trip the
    4-space rule. To be fully safe, strip ALL leading whitespace from
    every line instead.
    """
    stripped_lines = [line.strip() for line in content.split("\n")]
    stripped_content = "\n".join(stripped_lines)
    st.markdown(stripped_content, unsafe_allow_html=True)


# ============================================================
# CUSTOM CSS
# ============================================================

render_html("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(101,114,255,0.14), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(138,92,246,0.12), transparent 30%),
        #0b0f19;
    color: #f5f7ff;
}


/* Remove Streamlit top spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1250px;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #101522 0%,
        #0b0f19 100%
    );
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

.sidebar-title {
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 5px;
}

.sidebar-subtitle {
    font-size: 12px;
    color: #8992aa;
    margin-bottom: 25px;
}

.profile-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 15px;
    padding: 16px;
    margin-bottom: 14px;
}

.profile-label {
    color: #8992aa;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}

.profile-value {
    font-size: 16px;
    font-weight: 700;
}


/* ============================================================
   BRAND HEADER
   ============================================================ */

.brand-row {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 20px 22px;
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    margin-bottom: 25px;
    backdrop-filter: blur(15px);
}

.bot-logo {
    width: 58px;
    height: 58px;
    border-radius: 17px;
    background: linear-gradient(135deg, #6572ff, #8b5cf6);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 31px;
    box-shadow: 0 8px 30px rgba(101,114,255,0.3);
}

.brand-title {
    font-size: 26px;
    font-weight: 800;
    line-height: 1.1;
}

.brand-subtitle {
    color: #8992aa;
    font-size: 12px;
    margin-top: 5px;
}

.status {
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 7px;
    color: #b5bdd2;
    font-size: 12px;
}

.online-dot {
    width: 8px;
    height: 8px;
    background: #32d583;
    border-radius: 50%;
    box-shadow: 0 0 10px rgba(50,213,131,0.7);
}


/* ============================================================
   WELCOME
   ============================================================ */

.welcome-card {
    text-align: center;
    padding: 40px 25px;
    margin-bottom: 25px;
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 22px;
}

.welcome-icon {
    font-size: 50px;
    margin-bottom: 10px;
}

.welcome-title {
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 10px;
}

.welcome-text {
    color: #9ca5bb;
    max-width: 650px;
    margin: auto;
    line-height: 1.7;
}


/* ============================================================
   FEATURE CARDS
   ============================================================ */

.feature-card {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 20px;
    min-height: 150px;
}

.feature-icon {
    font-size: 28px;
    margin-bottom: 10px;
}

.feature-title {
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 7px;
}

.feature-text {
    color: #8f98ae;
    font-size: 12px;
    line-height: 1.6;
}


/* ============================================================
   CHAT MESSAGES
   ============================================================ */

.user-message {
    display: flex;
    justify-content: flex-end;
    margin: 12px 0;
}

.user-bubble {
    max-width: 75%;
    background: linear-gradient(135deg, #6572ff, #7657ed);
    color: white;
    padding: 13px 17px;
    border-radius: 18px 18px 5px 18px;
    line-height: 1.55;
    box-shadow: 0 8px 25px rgba(101,114,255,0.15);
}

.bot-message {
    display: flex;
    justify-content: flex-start;
    margin: 12px 0;
}

.bot-bubble {
    max-width: 78%;
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.07);
    color: #e8ebf5;
    padding: 13px 17px;
    border-radius: 18px 18px 18px 5px;
    line-height: 1.6;
}

.bot-avatar {
    margin-right: 9px;
    font-size: 22px;
    margin-top: 5px;
}


/* ============================================================
   SECTION TITLES
   ============================================================ */

.section-title {
    font-size: 14px;
    font-weight: 700;
    color: #b8c0d4;
    margin-top: 20px;
    margin-bottom: 12px;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;
    color: #687188;
    font-size: 11px;
    padding: 30px 0 10px 0;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.04);
    color: #dce1ef;
    transition: 0.2s;
}

.stButton > button:hover {
    border-color: rgba(101,114,255,0.5);
    color: white;
}


/* ============================================================
   CHAT INPUT
   ============================================================ */

.stChatInput {
    border-radius: 15px;
}

/* Fix: typed text becoming invisible on the dark background */
div[data-testid="stChatInput"] textarea,
div[data-testid="stChatInput"] div[data-baseweb="textarea"],
div[data-baseweb="textarea"] textarea,
[data-testid="stChatInputTextArea"] {
    color: #f5f7ff !important;
    -webkit-text-fill-color: #f5f7ff !important;
    background-color: #141a2b !important;
    caret-color: #f5f7ff !important;
}

div[data-testid="stChatInput"] textarea::placeholder,
[data-testid="stChatInputTextArea"]::placeholder {
    color: #8992aa !important;
    -webkit-text-fill-color: #8992aa !important;
    opacity: 1 !important;
}

div[data-testid="stChatInput"] {
    background-color: #141a2b !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 15px !important;
}

/* Fix: text typed in sidebar / other text_input, number_input, textarea widgets too */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
input, textarea {
    color: #f5f7ff !important;
    -webkit-text-fill-color: #f5f7ff !important;
    background-color: #141a2b !important;
}

</style>
""")


# ============================================================
# SAFE HELPERS FOR chatbot.py
# (In case chatbot.py is missing something, app should not crash)
# ============================================================

def safe_load_profile():
    try:
        profile = chatbot.load_profile()
        if not isinstance(profile, dict):
            return {}
        return profile
    except Exception:
        return {}


def safe_save_profile(data):
    try:
        chatbot.save_profile(data)
    except Exception:
        # Saving profile should never crash the UI
        # (e.g. read-only filesystem on some hosts)
        pass


def safe_log_conversation(user_text, bot_text):
    try:
        chatbot.log_conversation(user_text, bot_text)
    except Exception:
        pass


def safe_detect_language(text):
    try:
        return chatbot.detect_language(text)
    except Exception:
        return "unknown"


def safe_detect_intent(text, context):
    try:
        return chatbot.detect_intent(text, context)
    except Exception:
        return "unknown"


def safe_get_response(intent, context):
    try:
        return chatbot.get_response(intent, context)
    except Exception:
        return "Sorry, mujhe abhi is sawal ka jawab dene mein masla ho raha hai. Dobara try karein."


TECHNICAL_TOPICS = getattr(chatbot, "TECHNICAL_TOPICS", set())
HISTORY_LIMIT = getattr(chatbot, "HISTORY_LIMIT", 20)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "context" not in st.session_state:

    # chatbot.load_profile() is expected to return a DICTIONARY
    profile = safe_load_profile()

    st.session_state.context = {
        "name": profile.get("name"),
        "last_topic": None,
        "last_message": "",
        "mood_score": 0,
        "history": []
    }


# ============================================================
# HELPER
# ============================================================

def safe_html(text):
    return html.escape(str(text)).replace("\n", "<br>")


# ============================================================
# PROCESS MESSAGE
# ============================================================
def process_message(user_input):

    try:
        cleaned = chatbot.clean_input(user_input)
    except Exception:
        cleaned = user_input.strip() if user_input else ""

    if not cleaned:
        return

    language = safe_detect_language(cleaned)

    st.session_state.context["last_message"] = cleaned

    intent = safe_detect_intent(
        cleaned,
        st.session_state.context
    )

    response = safe_get_response(
        intent,
        st.session_state.context
    )

    # USER MESSAGE
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # MOOD
    if intent == "positive":
        st.session_state.context["mood_score"] += 1

    elif intent == "negative":
        st.session_state.context["mood_score"] -= 1

    # LAST TOPIC
    if intent in TECHNICAL_TOPICS:
        st.session_state.context["last_topic"] = intent

    # HISTORY
    st.session_state.context["history"].append({
        "user": user_input,
        "bot": response,
        "intent": intent,
        "language": language
    })

    if len(st.session_state.context["history"]) > HISTORY_LIMIT:
        st.session_state.context["history"].pop(0)

    # LOG
    safe_log_conversation(
        user_input,
        response
    )

    # SAVE NAME
    if intent == "name" and st.session_state.context.get("name"):
        safe_save_profile({
            "name": st.session_state.context["name"]
        })

    # BOT MESSAGE
    st.session_state.messages.append({
        "role": "bot",
        "content": response
    })


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html("""
    <div class="sidebar-title">
        🤖 CodeBuddy PRO
    </div>

    <div class="sidebar-subtitle">
        Your personal rule-based coding companion
    </div>
    """)


    # --------------------------------------------------------
    # PROFILE
    # --------------------------------------------------------

    current_name = st.session_state.context.get("name")

    display_name = (
        current_name.title()
        if current_name
        else "Guest"
    )

    render_html(f"""
    <div class="profile-card">

        <div class="profile-label">
            Profile
        </div>

        <div class="profile-value">
            👤 {safe_html(display_name)}
        </div>

    </div>
    """)


    # --------------------------------------------------------
    # MOOD
    # --------------------------------------------------------

    mood_score = st.session_state.context.get(
        "mood_score",
        0
    )

    if mood_score > 0:
        mood_text = "Positive 😊"

    elif mood_score < 0:
        mood_text = "Negative 😔"

    else:
        mood_text = "Neutral 😌"


    render_html(f"""
    <div class="profile-card">

        <div class="profile-label">
            Current Mood
        </div>

        <div class="profile-value">
            {mood_text}
        </div>

    </div>
    """)


    # --------------------------------------------------------
    # LAST TOPIC
    # --------------------------------------------------------

    last_topic = st.session_state.context.get(
        "last_topic"
    )

    if last_topic:
        topic_display = last_topic.replace(
            "_",
            " "
        ).title()
    else:
        topic_display = "No topic yet"


    render_html(f"""
    <div class="profile-card">

        <div class="profile-label">
            Last Topic
        </div>

        <div class="profile-value">
            💻 {safe_html(topic_display)}
        </div>

    </div>
    """)


    # --------------------------------------------------------
    # QUICK TOPICS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">⚡ Quick Topics</div>',
        unsafe_allow_html=True
    )


    quick_topics = [
        "Explain Python",
        "What is AI?",
        "What is machine learning?",
        "Explain SQL",
        "Explain OOP",
        "Explain data structures",
        "What is Git?"
    ]


    for idx, topic in enumerate(quick_topics):

        if st.button(
            topic,
            key=f"quick_{idx}",
            use_container_width=True
        ):
            process_message(topic)
            st.rerun()


    st.markdown("---")


    # --------------------------------------------------------
    # CLEAR CONVERSATION
    # --------------------------------------------------------

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True,
        key="clear_conversation_btn"
    ):

        st.session_state.messages = []

        st.session_state.context = {
            "name": current_name,
            "last_topic": None,
            "last_message": "",
            "mood_score": 0,
            "history": []
        }

        st.rerun()


    # --------------------------------------------------------
    # ENGINE INFO
    # --------------------------------------------------------

    render_html("""
    <div style="
        margin-top:25px;
        text-align:center;
        color:#687188;
        font-size:11px;
        line-height:1.7;
    ">
        <b style="color:#aeb6cb;">
            CodeBuddy Pro
        </b>
        <br>
        100% Rule-Based Engine
        <br>
        No LLM • No API
    </div>
    """)


# ============================================================
# MAIN HEADER
# ============================================================

render_html("""
<div class="brand-row">

    <div class="bot-logo">
        🤖
    </div>

    <div>

        <div class="brand-title">
            CodeBuddy
            <span style="color:#6572ff;">
                PRO
            </span>
        </div>

        <div class="brand-subtitle">
            Smart conversations • Coding help •
            English + Roman Urdu
        </div>

    </div>

    <div class="status">
        <span class="online-dot"></span>
        Online
    </div>

</div>
""")


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.messages:

    render_html("""
    <div class="welcome-card">

        <div class="welcome-icon">
            👋
        </div>

        <div class="welcome-title">
            Welcome to CodeBuddy
        </div>

        <div class="welcome-text">
            Your personal rule-based coding companion.
            Ask questions naturally in English, Roman Urdu,
            or a mixture of both.
        </div>

    </div>
    """)


    col1, col2, col3 = st.columns(3)


    with col1:

        render_html("""
        <div class="feature-card">

            <div class="feature-icon">
                💬
            </div>

            <div class="feature-title">
                Natural Conversation
            </div>

            <div class="feature-text">
                Greetings, mood, name,
                casual conversation and
                follow-up questions.
            </div>

        </div>
        """)


    with col2:

        render_html("""
        <div class="feature-card">

            <div class="feature-icon">
                💻
            </div>

            <div class="feature-title">
                Coding Assistant
            </div>

            <div class="feature-text">
                Python, SQL, OOP, DSA,
                Git, HTML, CSS and
                programming concepts.
            </div>

        </div>
        """)


    with col3:

        render_html("""
        <div class="feature-card">

            <div class="feature-icon">
                🌍
            </div>

            <div class="feature-title">
                Bilingual
            </div>

            <div class="feature-text">
                Understands English,
                Roman Urdu, and
                mixed conversations.
            </div>

        </div>
        """)


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        render_html(
            f"""
            <div class="user-message">
                <div class="user-bubble">
                    {safe_html(message["content"])}
                </div>
            </div>
            """
        )

    elif message["role"] == "bot":

        render_html(
            f"""
            <div class="bot-message">
                <div class="bot-avatar">
                    🤖
                </div>
                <div class="bot-bubble">
                    {safe_html(message["content"])}
                </div>
            </div>
            """
        )


# ============================================================
# CHAT INPUT (only ONE instance — duplicate removed)
# ============================================================

user_input = st.chat_input("Message CodeBuddy...")

if user_input:
    process_message(user_input)
    st.rerun()


# ============================================================
# FOOTER
# ============================================================

render_html("""
<div class="footer">
    CodeBuddy PRO • 100% Rule-Based Python Chatbot
    <br>
    No LLM • No API • English + Roman Urdu
</div>
""")