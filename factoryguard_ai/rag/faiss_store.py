import json
from pathlib import Path
import faiss
import numpy as np
from config import INDEX_DIR
from rag.embeddings import embed

def index_factory(factory_id, chunks):
    folder=Path(INDEX_DIR)/str(factory_id)
    folder.mkdir(parents=True,exist_ok=True)
    vectors=np.asarray(embed([x["text"] for x in chunks]),dtype="float32")
    index=faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    faiss.write_index(index,str(folder/"index.faiss"))
    (folder/"metadata.json").write_text(json.dumps(chunks,ensure_ascii=False),encoding="utf-8")

def search_factory(factory_id, query, k=5):
    folder=Path(INDEX_DIR)/str(factory_id)
    index_path=folder/"index.faiss"; meta_path=folder/"metadata.json"
    if not index_path.exists(): return []
    index=faiss.read_index(str(index_path))
    chunks=json.loads(meta_path.read_text(encoding="utf-8"))
    q=np.asarray(embed([query]),dtype="float32")
    scores, ids=index.search(q,min(k,index.ntotal))
    return [{**chunks[i],"score":float(scores[0][j])} for j,i in enumerate(ids[0]) if i >= 0]
