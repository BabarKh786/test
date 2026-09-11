# FactoryGuard AI

FactoryGuard AI is a modular food-safety and quality assistant. It uses factory-provided SOPs and documents as a RAG knowledge base, operational records for deterministic analysis, and GPT-OSS 120B through Groq for grounded reasoning and recommendations.

## Stack
- Streamlit UI
- GPT-OSS 120B via Groq
- FAISS vector search
- Sentence Transformers embeddings
- PyMuPDF / python-docx / pandas
- SQLite
- Pydantic
- Plotly
- ReportLab

## Run locally
1. Create a Groq API key.
2. Set `GROQ_API_KEY` in your environment or `.streamlit/secrets.toml`.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Run:
   `streamlit run app.py`

## Streamlit Cloud
Push this repository to GitHub, create a Streamlit Community Cloud app, choose `app.py`, and add `GROQ_API_KEY` in the app's Secrets settings.

Never commit an API key.

## RAG behavior
SOP/HACCP/specification/procedure documents are indexed into FAISS. Analysis retrieves the most relevant chunks and passes them with the operational evidence to GPT-OSS 120B. If no relevant factory-specific requirement is available, the app does not invent one; it reports that a factory-specific comparison cannot be completed.

## MVP modules
- Temperature records
- Cleaning records
- SOP review
- HACCP review
- Inspection report
- Laboratory report
- Visual observation
- Corrective action tracking
- PDF report
