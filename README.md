# Trade Bot 🤖📊  
### Text + Voice based RAG Chatbot for Holdings & Trades Data

Trade Bot is a **closed-book Retrieval-Augmented Generation (RAG) chatbot** built using Streamlit.
It answers questions **only** from the provided financial datasets (`holdings.csv` and `trades.csv`) and strictly refuses to answer when the information is not found.

The system supports:
- Text-based chat
- Voice input (speech-to-text)
- Voice output (text-to-speech) - IN_PROGRESS
- Multi-chat conversations with memory (ChatGPT-style UI)

---

## 🧠 Key Features

- **Closed-book RAG** (no internet, no hallucinations)
- **Strict refusal logic**  
  → Responds with:  
  `Sorry can not find the answer`
- **FAISS-based vector search**
- **One-time indexing per session**
- **Multi-chat support** (new chat, rename chat, switch chat)
- **Conversation memory per chat**
- **Optional voice input & read-aloud responses**
- **Deterministic LLM responses** (no temperature)

---

## 🏗️ Architecture Overview

User (Text / Voice)
↓
Speech-to-Text (optional)
↓
Query Embedding
↓
FAISS Vector Search
↓
Similarity Threshold Check
┌───────────────┐
│ score < limit │ → "Sorry can not find the answer"
└───────────────┘
↓
Context-only Prompt
↓
LLM (gpt-5-mini)
↓
Answer (Text / Voice)

---

## 📁 Project Structure

trade-bot/
│
├── app.py # Streamlit app
├── requirements.txt
├── README.md
│
├── data/
│ ├── holdings.csv
│ └── trades.csv
│
├── config/
│ └── config.py
│
├── src/
│ ├── ingestion/
│ │ ├── load_data.py
│ │ └── document_builder.py
│ │
│ ├── embeddings/
│ │ ├── embedder.py
│ │ └── vector_store.py
│ │
│ ├── indexing/
│ │ └── indexer.py
│ │
│ ├── rag/
│ │ ├── retriever.py
│ │ ├── prompt.py
│ │ └── qa_chain.py
│ │
│ ├── llm/
│ │ └── openai_client.py
│ │
│ ├── voice/
│ │ ├── speech_to_text.py
│ │ └── text_to_speech.py
│ │
│ └── utils/
│ └── logger.py

---

## ⚙️ How Indexing Works (Important)

- CSV files are loaded and converted into text documents
- Documents are embedded using `sentence-transformers`
- Embeddings are stored in a **local FAISS index**
- Indexing runs **only once per Streamlit session**
- Subsequent user queries reuse the same vector store

This avoids re-embedding and ensures fast responses.

---

## 🛡️ Hallucination Prevention

The chatbot **never answers blindly**.

Safeguards / Guardrails:
- Similarity score threshold before LLM is called
- Context-only prompting
- No external knowledge access
- Deterministic LLM configuration

If relevant context is not found:
```bash
Sorry can not find the answer
```

---

## 🎙️ Voice Support

- **Voice Input:**  
  Uses microphone + speech recognition to convert speech to text

- **Voice Output:**  
  Uses offline text-to-speech to read answers aloud

Both features can be toggled from the sidebar.

---

## 🚀 Running the App

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set OpenAI key
```bash
export OPENAI_API_KEY=your_api_key_here
```

### 3. Run Streamlit app
```bash
streamlit run app.py
```

---

## Author

Sagnik Mukherjee
GitHub: [sagnikmukherjee](https://github.com/sagnik0712mukherjee)
