import os
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
INDEX_DIR = DATA_DIR / "faiss"
DB_PATH = DATA_DIR / "factoryguard.db"

for p in [DATA_DIR, UPLOAD_DIR, INDEX_DIR]:
    p.mkdir(parents=True, exist_ok=True)

GROQ_MODEL = "openai/gpt-oss-120b"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def groq_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return os.getenv("GROQ_API_KEY")

MAX_FILE_MB = 20
