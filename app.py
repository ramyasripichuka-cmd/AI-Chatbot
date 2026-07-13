import streamlit as st
import google.generativeai as genai
import sqlite3
import json
import os
from dotenv import load_dotenv
from datetime import datetime

# ==========================
# Page Configuration
# ==========================
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ==========================
# Load API Key
# ==========================
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

# ==========================
# SQLite Database
# ==========================
conn = sqlite3.connect("chatbot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS conversations(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    messages TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# ==========================
# Session State
# ==========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None


# ==========================
# Database Functions
# ==========================
def save_conversation():

    data = json.dumps(st.session_state.messages)

    if len(st.session_state.messages) > 0:
        title = st.session_state.messages[0]["content"][:30]

    else:
        title = "New Chat"

    if st.session_state.conversation_id is None:

        cursor.execute(
            """
            INSERT INTO conversations(title,messages)
            VALUES(?,?)
            """,
            (title, data)
        )

        conn.commit()

        st.session_state.conversation_id = cursor.lastrowid

    else:

        cursor.execute(
            """
            UPDATE conversations
            SET title=?,
                messages=?
            WHERE id=?
            """,
            (
                title,
                data,
                st.session_state.conversation_id
            )
        )

        conn.commit()


def load_conversation(chat_id):

    cursor.execute(
        "SELECT messages FROM conversations WHERE id=?",
        (chat_id,)
    )

    row = cursor.fetchone()

    if row:
        st.session_state.messages = json.loads(row[0])
        st.session_state.conversation_id = chat_id


def delete_conversation(chat_id):

    cursor.execute(
        "DELETE FROM conversations WHERE id=?",
        (chat_id,)
    )

    conn.commit()

    if st.session_state.conversation_id == chat_id:
        st.session_state.messages = []
        st.session_state.conversation_id = None


def get_all_conversations():

    cursor.execute("""
    SELECT id,title,created_at
    FROM conversations
    ORDER BY created_at DESC
    """)

    return cursor.fetchall()


def new_chat():

    st.session_state.messages = []
    st.session_state.conversation_id = None

    # ======================================
# Main UI
# ======================================

st.title("🤖 AI Chatbot")

st.write("Chat with Gemini AI")

# ======================================
# Sidebar
# ======================================

with st.sidebar:

    st.header("Conversations")

    if st.button("➕ New Conversation"):
        new_chat()
        st.rerun()

    st.divider()

    chats = get_all_conversations()

    if len(chats) == 0:
        st.info("No conversations yet.")

    for chat in chats:

        chat_id = chat[0]
        title = chat[1]

        col1, col2 = st.columns([4,1])

        with col1:
            if st.button(
                title,
                key=f"load_{chat_id}",
                use_container_width=True
            ):
                load_conversation(chat_id)
                st.rerun()

        with col2:
            if st.button(
                "🗑️",
                key=f"delete_{chat_id}"
            ):
                delete_conversation(chat_id)
                st.rerun()


# ======================================
# Display Previous Messages
# ======================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ======================================
# User Input
# ======================================

prompt = st.chat_input("Type your message...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

# ======================================
# Generate AI Response
# ======================================

    try:

        # Build conversation history
        history = ""

        for msg in st.session_state.messages:
            role = "User" if msg["role"] == "user" else "Assistant"
            history += f"{role}: {msg['content']}\n"

        # Send to Gemini
        response = model.generate_content(history)

        ai_reply = response.text

    except Exception as e:

        ai_reply = f"Error: {e}"

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(ai_reply)

    # Save response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )

    # Save conversation in SQLite
    save_conversation()