from pathlib import Path
import fitz
from docx import Document

def load_document(path):
    p=Path(path)
    ext=p.suffix.lower()
    if ext == ".pdf":
        doc=fitz.open(path)
        return [{"page": i+1, "text": page.get_text("text")} for i,page in enumerate(doc)]
    if ext == ".docx":
        doc=Document(path)
        text="\n".join(x.text for x in doc.paragraphs if x.text.strip())
        return [{"page": 1, "text": text}]
    if ext == ".txt":
        return [{"page": 1, "text": p.read_text(encoding="utf-8",errors="ignore")}]
    raise ValueError("Unsupported knowledge-base document type.")
