from fastapi import APIRouter, Form
from app.services.embeddings import embed
from app.services.storage import get_top_chunks
from app.services.llm import llm_message

router = APIRouter()


@router.post("/ask")
async def ask(document_id: int = Form(), question: str = Form()):
    question_embedded = embed(question)

    chunk_answer = get_top_chunks(document_id, question_embedded, k=5)

    text = ""
    for chunk in chunk_answer:
        text += chunk.chunk_text + "\n"

    llm_answer = llm_message(question=question, pdf_polished=text)
    return {"answer": llm_answer}
