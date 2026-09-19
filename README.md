# 🤖 CodeBuddy PRO

**A rule-based, bilingual (English + Roman Urdu) coding companion chatbot built with Streamlit.**

CodeBuddy PRO is a sleek, dark-themed conversational assistant designed to help users learn programming concepts, get quick explanations, and chat naturally — all without relying on any external LLM or API. It runs on a 100% rule-based engine, making it lightweight, fast, and fully offline-capable.

---

## ✨ Features

- 💬 **Natural Conversation** — Handles greetings, mood detection, name recognition, and casual follow-up questions.
- 💻 **Coding Assistant** — Explains core concepts in Python, SQL, OOP, Data Structures & Algorithms (DSA), Git, HTML, and CSS.
- 🌍 **Bilingual Support** — Understands and responds in English, Roman Urdu, or a natural mix of both.
- ⚡ **Quick Topics** — One-click sidebar shortcuts for the most common programming questions.
- 😊 **Mood Tracking** — Tracks conversation sentiment (Positive / Neutral / Negative) in real time.
- 🧠 **Context Memory** — Remembers the last discussed topic and recent conversation history within a session.
- 👤 **Persistent Profile** — Saves and recalls the user's name across sessions.
- 🎨 **Modern UI** — Custom dark-themed interface with smooth gradients, chat bubbles, and responsive layout.
- 🔒 **100% Rule-Based** — No LLM, no external API calls, no internet dependency for responses — fully private and self-contained.

---

## 🖥️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | [Streamlit](https://streamlit.io/) |
| Language | Python 3.9+ |
| Styling | Custom CSS (injected via `st.markdown`) |
| Logic Engine | Rule-based intent detection (`chatbot.py`) |

---

## 📂 Project Structure

```
codebuddy-pro/
│
├── app.py              # Main Streamlit application (UI, layout, session state)
├── chatbot.py           # Core rule-based engine (intent detection, responses, profile storage)
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/codebuddy-pro.git
   cd codebuddy-pro
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. Open your browser at `http://localhost:8501` 🎉

---

## 🌐 Deployment (Streamlit Community Cloud)

This app is ready to deploy for free on [Streamlit Community Cloud](https://share.streamlit.io):

1. Push this repository to GitHub (including `app.py`, `chatbot.py`, and `requirements.txt`).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select this repository and branch, and set the main file path to `app.py`.
4. Click **Deploy** — your app will be live at a public `*.streamlit.app` URL within a few minutes.

The app works out of the box on both desktop and mobile browsers.

---

## 🧩 How It Works

1. The user types a message (in English, Roman Urdu, or mixed) via the chat input.
2. `chatbot.clean_input()` normalizes the text.
3. `chatbot.detect_language()` identifies the language used.
4. `chatbot.detect_intent()` classifies the message into an intent (e.g. greeting, coding topic, mood, name).
5. `chatbot.get_response()` generates a rule-based reply based on the detected intent and conversation context.
6. The UI updates the chat history, mood score, last topic, and logs the conversation.

---

## 🛠️ Customization

- **Add new topics:** Extend `chatbot.TECHNICAL_TOPICS` and add matching rules/responses in `chatbot.py`.
- **Change theme colors:** Edit the CSS variables inside the `st.markdown("""<style>...</style>""")` block in `app.py`.
- **Adjust conversation memory length:** Modify `chatbot.HISTORY_LIMIT`.

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork this repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Sarmad**
Built as a rule-based coding companion project — no LLM, no API, just clean logic and a friendly interface.

---

⭐ If you find this project useful, consider giving it a star on GitHub!
