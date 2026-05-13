def chunker(pdf_polished, chunk_size=500):
    chunks = []
    for i in range(0, len(pdf_polished), chunk_size):
        chunk = pdf_polished[i:i + chunk_size]
        chunks.append(chunk)
    return chunks