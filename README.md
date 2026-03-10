<div align="center">

# 🤖 AI Document Chatbot
### with Wav2Lip Talking Avatar Integration

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)

*Upload documents. Ask questions. Get answers — with a talking AI avatar.*

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 Document Upload | PDF & image ingestion with OCR support |
| 🔍 RAG-based Q&A | Hybrid retrieval via ChromaDB + BM25 |
| 🧠 Chat Memory | Persistent conversation history per session |
| ✍️ Custom Prompts | Per-chat custom AI instructions |
| 🎙️ Voice Input | Whisper-powered audio transcription |
| 🎭 Talking Avatar | Lip-synced video responses via Wav2Lip + gTTS |
| 🔐 Authentication | Secure user login & registration |
| 💬 Multi-Chat | Create and manage multiple document chats |

---

## 🛠️ Tech Stack
```text
Backend          →  Flask · SQLAlchemy · Flask-Login
Database         →  MySQL
Vector Store     →  ChromaDB
OCR              →  Tesseract (pytesseract)

AI / ML
├── LLM & RAG    →  LangChain · Ollama (Llama3)
├── Embeddings   →  Ollama
├── Speech-STT   →  OpenAI Whisper
├── Text-TTS     →  gTTS
└── Avatar       →  Wav2Lip
```

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python** 3.8+
- **MySQL** Server
- **Ollama** with the `llama3` model
- **FFmpeg**
- **Tesseract OCR**
- **Wav2Lip** *(optional — required for avatar feature only)*

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd CHATBOT
```

### 2. Install Python Dependencies
```bash
pip install flask flask-login flask-sqlalchemy pymysql
pip install langchain langchain-chroma langchain-ollama langchain-community
pip install whisper gtts pillow pytesseract unstructured markdown
```

### 3. Configure MySQL
```sql
CREATE DATABASE chat;
```

Then update your credentials in `app/__init__.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/chat'
app.config['SECRET_KEY'] = 'your-secret-key'
```

### 4. Install Ollama & Pull Llama3
```bash
ollama pull llama3
```

### 5. Setup Wav2Lip *(Optional)*

Follow the [Wav2Lip installation guide](https://github.com/Rudrabha/Wav2Lip), then update the paths in `chat_routes.py`:
```python
python_executable     = r"path\to\wav2lip\env\python.exe"
inference_script_path = r"path\to\wav2lip\inference.py"
checkpoint_path       = r"path\to\wav2lip\wav2lip.pth"
```

### 6. Run the App
```bash
python run.py
```

> 🌐 Open your browser at **http://localhost:5000**

---

## 📂 Project Structure
```
CHATBOT/
├── app/
│   ├── chat/
│   │   └── chat_routes.py          # Chat endpoints
│   ├── user/
│   │   └── user_routes.py          # Auth endpoints
│   ├── Models/
│   │   ├── User.py                 # User model
│   │   ├── Chat.py                 # Chat model
│   │   └── ChatHistory.py          # Chat history model
│   ├── document_utils/
│   │   ├── upload_documents.py     # Document processing
│   │   └── qa_chat.py              # RAG chain setup
│   ├── DOCUMENTS/                  # Uploaded PDFs
│   ├── Vector Storage/             # ChromaDB collections
│   ├── static/                     # CSS, JS, videos
│   ├── templates/                  # HTML templates
│   └── __init__.py                 # App factory
└── run.py                          # Entry point
```

---

## 💡 Usage
```
1. Register / Login      →  Create an account or sign in
2. Create New Chat       →  Upload a PDF and name your session
3. Set Custom Prompt     →  (Optional) Add specific AI instructions
4. Start Chatting        →  Ask anything about your document
5. Voice Input           →  Use your microphone for hands-free queries
6. Generate Avatar       →  Convert AI responses to a talking avatar video
```

---

## 🔌 API Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET/POST | `/register` | User registration |
| GET/POST | `/login` | User login |
| GET | `/dashboard` | Main dashboard |
| POST | `/new_chat` | Create chat with document upload |
| GET | `/start_chat/<chat_id>` | Chat interface |
| POST | `/start_chat/<chat_id>/stream` | Streaming chat responses |
| POST | `/transcribe` | Audio → text transcription |
| POST | `/wav2lip` | Generate talking avatar video |

---

## ⚙️ Features in Detail

<details>
<summary><strong>🔍 RAG Pipeline</strong></summary>

- Hybrid retrieval combining **BM25** keyword search and **vector similarity**
- Context-aware responses using full conversation history
- Customizable system prompts per chat session

</details>

<details>
<summary><strong>📄 Document Processing</strong></summary>

- PDF text extraction with layout awareness
- OCR support for images (PNG, JPG, JPEG)
- Text chunking: **800 characters** with **150 character overlap**

</details>

<details>
<summary><strong>⚡ Streaming Responses</strong></summary>

- Real-time token-by-token streaming
- Automatic Markdown → HTML conversion
- Auto-saved to persistent chat history

</details>

---

## 🛠️ Troubleshooting

| Issue | Fix |
|---|---|
| ❌ Database Connection Error | Verify MySQL is running and credentials are correct |
| ❌ Ollama Model Not Found | Run `ollama pull llama3` |
| ❌ Wav2Lip Timeout | Increase timeout in `subprocess.run` or check GPU availability |
| ❌ OCR Errors | Install Tesseract and ensure it's added to your system PATH |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please **open an issue first** to discuss what you'd like to change.

---

## 🙏 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) — RAG framework
- [Ollama](https://ollama.ai/) — Local LLM inference
- [Wav2Lip](https://github.com/Rudrabha/Wav2Lip) — Lip sync generation
- [Whisper](https://github.com/openai/whisper) — Speech recognition

---

## 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">

⭐ **Star this repo if you found it useful!**

</div>
