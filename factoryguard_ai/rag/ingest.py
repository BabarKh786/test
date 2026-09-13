from pathlib import Path
from rag.document_loader import load_document
from rag.chunker import chunk_pages
from rag.faiss_store import index_factory
from database.repository import add_document

KB_TYPES={"SOP","HACCP Plan","Product Specification","Procedure","Other"}

def ingest_uploaded_documents(factory_id, uploaded_files, doc_type):
    saved=[]
    all_chunks=[]
    base=Path("data/uploads")/str(factory_id)
    base.mkdir(parents=True,exist_ok=True)
    for uf in uploaded_files:
        path=base/uf.name
        path.write_bytes(uf.getbuffer())
        pages=load_document(str(path))
        chunks=chunk_pages(pages)
        for c in chunks:
            c["document_name"]=uf.name
            c["document_type"]=doc_type
        all_chunks.extend(chunks)
        add_document(factory_id,uf.name,doc_type,str(path),1)
        saved.append(uf.name)
    if all_chunks:
        index_factory(factory_id,all_chunks)
    return saved, len(all_chunks)
