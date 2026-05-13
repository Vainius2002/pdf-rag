from app.db import SessionLocal
from app.models import Document, Chunk
from sqlalchemy import select


def save_document(filename, chunks_with_embeddings, user_id):
    with SessionLocal() as session:

        doc = Document(filename=filename, user_id=user_id)
        session.add(doc)
        session.flush()
        
        for chunk_text, embedding in chunks_with_embeddings:
            chunk = Chunk(document_id=doc.id, chunk_text=chunk_text, embedding=embedding)
            session.add(chunk)
        session.commit()
        return doc.id
#Normally you'd just call session.commit() at the end. But the problem is that until we do session.commit, doc.id doesnt exist- You want chunks to have document_id=doc.id but session.flush makes it exist, jus doesnt commit yet


def get_top_chunks(document_id, question_embedding, k=5):
    with SessionLocal() as session:
        stmt = (
            select(Chunk)
            .where(Chunk.document_id == document_id)
            .order_by(Chunk.embedding.cosine_distance(question_embedding))
            .limit(k)
        )
        return list(session.scalars(stmt))
    

#cosine_distance is the pgvector method on Vector columns. It returns a number representing "how far apart" two vectors are. Small number = very similar, big = very different. 
#  So ORDER BY cosine_distance puts the most similar chunks first.
#session.scalars(stmt) returns the actual Chunk objects (not rows of columns). I can use .chunk_text on each, normal Python.