from fastapi import APIRouter, Form, Depends, HTTPException
from sqlalchemy import select

from app.db import SessionLocal
from app.models import Document, User
from app.services.embeddings import embed
from app.services.storage import get_top_chunks
from app.services.llm import llm_message
from app.dependencies import get_current_user

router = APIRouter()


@router.post("/ask")
async def ask(
    document_id: int = Form(),
    question: str = Form(),
    user: User = Depends(get_current_user),
):
    with SessionLocal() as session:
        doc = session.scalar(select(Document).where(Document.id == document_id))
        if not doc or doc.user_id != user.id:
            raise HTTPException(status_code=404, detail="Document not found")

    question_embedded = embed(question)
    chunk_answer = get_top_chunks(document_id, question_embedded, k=5)

    text = ""
    for chunk in chunk_answer:
        text += chunk.chunk_text + "\n"

    llm_answer = llm_message(question=question, pdf_polished=text)
    return {"answer": llm_answer}
