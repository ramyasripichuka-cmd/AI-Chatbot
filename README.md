# 🤖 AI Chatbot using Streamlit & Gemini API

## 📌 Project Overview

This project is a simple AI Chatbot Web Application built using **Streamlit**, **Google Gemini API**, and **SQLite**. It allows users to have conversations with an AI assistant while maintaining conversation history during the session. Previous conversations can be viewed, continued, or deleted.

---

## 🚀 Features

* AI-powered chatbot using Google Gemini API
* Simple and responsive Streamlit interface
* Real-time chat responses
* Conversation history
* Start a New Conversation
* View previous conversations
* Delete saved conversations
* SQLite database for storing chat history
* Session-based context retention

---

## 🛠️ Technologies Used

* Python
* Streamlit
* Google Gemini API
* SQLite
* python-dotenv

---

## 📁 Project Structure

```text
AI_Chatbot/
│── app.py
│── chatbot.db
│── requirements.txt
│── .env
│── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/AI_Chatbot.git
cd AI_Chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

## 💾 Database

This project uses **SQLite** (`chatbot.db`) to store conversation history.

The database stores:

* Conversation ID
* Conversation Title
* Messages
* Created Time

---

## 📌 How to Use

1. Open the application.
2. Type a message in the chat box.
3. Click **Send**.
4. Continue chatting with the AI.
5. Click **New Conversation** to start a fresh chat.
6. View previous conversations from the sidebar.
7. Delete conversations whenever required.

---

## 📷 Output

The chatbot provides:

* Real-time AI responses
* Saved conversation history
* New chat functionality
* Delete conversation option

---

## 📖 Technical Decision

This project uses **Streamlit** because it provides both the user interface and backend logic within a single Python application. This keeps the project lightweight, easy to understand, and quick to develop while satisfying the required chatbot functionality. Streamlit's built-in chat components also simplify building conversational applications.

---

## 📄 Requirements

* Python 3.10+
* Gemini API Key
* Internet Connection

---

## 👨‍💻 Author

Developed as an AI Chatbot Web Application using Streamlit, Google Gemini API, and SQLite.
