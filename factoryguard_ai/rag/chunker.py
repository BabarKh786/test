def chunk_pages(pages, chunk_size=900, overlap=120):
    chunks=[]
    for page in pages:
        text=" ".join(page["text"].split())
        start=0
        while start < len(text):
            end=min(len(text), start+chunk_size)
            piece=text[start:end].strip()
            if piece:
                chunks.append({"text":piece,"page":page["page"]})
            if end == len(text): break
            start=end-overlap
    return chunks
