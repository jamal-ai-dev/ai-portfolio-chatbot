import os
from dotenv import load_dotenv
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_DIR = os.path.join(BASE_DIR, "faiss_index")

GROQ_MODEL = "llama-3.1-8b-instant"
OWNER_NAME = os.getenv("OWNER_NAME", "Jamal")

# Loaded lazily so importing this module doesn't require an index/key yet.
_embeddings = None
_db = None
_llm = None


def _load():
    global _embeddings, _db, _llm

    if _db is None:
        if not os.path.isdir(INDEX_DIR):
            raise RuntimeError(
                "FAISS index not found. Run `python -m rag.ingest` first."
            )
        _embeddings = FastEmbedEmbeddings()
        _db = FAISS.load_local(
            INDEX_DIR, _embeddings, allow_dangerous_deserialization=True
        )

    if _llm is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is missing. Add it to your .env file.")
        _llm = ChatGroq(model=GROQ_MODEL, temperature=0.4, groq_api_key=api_key)


SYSTEM_PROMPT_TEMPLATE = """You are the AI assistant embedded on {name}'s personal portfolio website.
Your only job is to answer questions about {name} — their background, skills, projects, and goals —
using ONLY the context below, pulled from {name}'s own knowledge base.

Rules:
- Be friendly, confident, and concise (2-4 sentences unless asked for more detail).
- Speak about {name} in the third person, like a knowledgeable assistant, not as {name} themself.
- If the answer isn't in the context, say you don't have that info yet and suggest the visitor
  use the Contact section to ask {name} directly. Never invent facts.

Context:
{context}
"""


def get_answer(question: str) -> str:
    _load()

    docs = _db.similarity_search(question, k=4)
    context = "\n\n".join(d.page_content for d in docs) if docs else "No relevant info found."

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(name=OWNER_NAME, context=context)

    messages = [
        ("system", system_prompt),
        ("human", question),
    ]
    response = _llm.invoke(messages)
    return response.content
