from fastapi import APIRouter, Form, Depends, HTTPException
from sqlalchemy import select
from app.db import SessionLocal
from app.models import Document, User
from app.dependencies import get_current_user
from app.services.embeddings import embed
from app.services.storage import get_top_chunks
from app.services.llm import llm

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

router = APIRouter()

# My own personal prompt template for my openai
prompt = ChatPromptTemplate.from_template(
    "Answer the question based only on the context below.\n"
    "If the answer isn't in the context, say you don't know.\n\n"
    "Context:\n{context}\n\n"
    "Question:\n{question}"
)
#my lcel chain. | in here is like ->
#also, prompt is the template we create. llm is the defined ai we imported. stroutputparser auto parses strings in the return. so we can keep using this pipeline using .invoke
chain = prompt | llm | StrOutputParser()


@router.post("/ask")
async def ask(document_id: int = Form(), question: str = Form(), user: User=Depends(get_current_user)):
    with SessionLocal() as session:
        doc= session.scalar(select(Document).where(Document.id == document_id))
        if not doc or doc.user_id != user.id:
            raise HTTPException(status_code=404, detail="Document not found")
    
        question_embedded = embed(question)

        chunks = get_top_chunks(document_id, question_embedded, k=5)
        context = ""
        for chunk in chunks:
            context += chunk.chunk_text + "\n"

        answer = chain.invoke({"question": question, "context": context})
        return {"answer": answer}


