"""
Builds the FAISS vector index from everything inside knowledge_base/.

Run this once whenever you add or update your personal info:
    python -m rag.ingest
"""
import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB_DIR = os.path.join(BASE_DIR, "knowledge_base")
INDEX_DIR = os.path.join(BASE_DIR, "faiss_index")


def build_index():
    if not os.path.isdir(KB_DIR) or not os.listdir(KB_DIR):
        raise SystemExit(
            f"No files found in {KB_DIR}. Add .txt files with your info first."
        )

    loader = DirectoryLoader(KB_DIR, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    chunks = splitter.split_documents(documents)

    print(f"Loaded {len(documents)} file(s), split into {len(chunks)} chunk(s). Embedding...")

    embeddings = FastEmbedEmbeddings()
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(INDEX_DIR)

    print(f"Index saved to {INDEX_DIR}/")


if __name__ == "__main__":
    build_index()
