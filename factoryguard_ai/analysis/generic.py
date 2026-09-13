from pathlib import Path
import pandas as pd
from rag.document_loader import load_document

def extract_input(path):
    ext=Path(path).suffix.lower()
    if ext in [".pdf",".docx",".txt"]:
        pages=load_document(path)
        return "\n".join(f"[Page {p['page']}] {p['text']}" for p in pages)
    if ext in [".csv",".xlsx",".xls"]:
        df=pd.read_csv(path) if ext==".csv" else pd.read_excel(path)
        return df.head(100).fillna("").to_csv(index=False)
    return "Binary/image input. Use the visual analysis pathway."
