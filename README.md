# AI Portfolio Chatbot

A personal **RAG (Retrieval-Augmented Generation) chatbot**, built from scratch, that knows everything about me — my background, skills, projects, and goals — and answers visitor questions on my portfolio site.

Not a no-code tool. Not a ChatGPT wrapper. A real RAG pipeline I built and understand end to end.

## How it works

1. My info lives as plain text in `knowledge_base/`.
2. `rag/ingest.py` splits that text into chunks, embeds them with **FastEmbed**, and stores the vectors in a local **FAISS** index.
3. When a visitor asks a question, `rag/chatbot.py` retrieves the most relevant chunks from FAISS and passes them, along with the question, to **Groq's LLaMA 3.1** to generate a grounded answer.
4. A **Flask** backend serves a custom HTML/CSS/JS chat UI and exposes a `/api/chat` endpoint that ties it all together.

## Tech stack

| Layer            | Tool                        |
|-------------------|------------------------------|
| RAG orchestration | LangChain                   |
| Vector store       | FAISS                       |
| Embeddings         | FastEmbed                   |
| LLM                | Groq (LLaMA 3.1, free tier) |
| Backend            | Flask                       |
| Frontend           | Custom HTML / CSS / JS      |

## Setup

```bash
git clone https://github.com/<your-username>/ai-portfolio-chatbot.git
cd ai-portfolio-chatbot

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

1. Copy `.env.example` to `.env` and add your free Groq API key from [console.groq.com/keys](https://console.groq.com/keys):

   ```bash
   cp .env.example .env
   ```

2. Replace the placeholder text in `knowledge_base/about_me.txt` with your real bio, skills, projects, and contact info. Add more `.txt` files to `knowledge_base/` if you want to split it up.

3. (Optional) Add your own photo as `static/avatar.jpg`.

4. Build the vector index:

   ```bash
   python -m rag.ingest
   ```

5. Run the app:

   ```bash
   python app.py
   ```

   Open `http://localhost:5000`.

## Project structure

```
ai-portfolio-chatbot/
├── app.py                  # Flask server + /api/chat endpoint
├── rag/
│   ├── ingest.py           # Builds the FAISS index from knowledge_base/
│   └── chatbot.py          # Retrieval + Groq LLM call
├── knowledge_base/         # Your personal info as .txt files
├── templates/index.html    # Chat UI
├── static/
│   ├── style.css
│   ├── script.js
│   └── avatar.jpg          # Your photo (add your own)
├── requirements.txt
└── .env.example
```

## Re-indexing

Any time you update `knowledge_base/`, rebuild the index:

```bash
python -m rag.ingest
```

## Deployment

Works well on any host that supports Python + Flask (Render, Railway, Fly.io, etc.). Just set `GROQ_API_KEY` and `OWNER_NAME` as environment variables and run `python -m rag.ingest` once during the build step before starting `app.py`.
