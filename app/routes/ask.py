from fastapi import APIRouter, Form, Depends, HTTPException
from sqlalchemy import select
from app.db import SessionLocal
from app.models import Document, User
from app.dependencies import get_current_user

from app.services.agent import agent

router = APIRouter()


@router.post("/ask")
async def ask(document_id: int = Form(), question: str = Form(), user: User=Depends(get_current_user)):
    with SessionLocal() as session:
        doc= session.scalar(select(Document).where(Document.id == document_id))
        if not doc or doc.user_id != user.id:
            raise HTTPException(status_code=404, detail="Document not found")
    
        initial_state = {
            "question" : question,
            "document_id" : document_id,
            "chunks" : "",
            "grade" : "",
            "answer" : "",
            "attempts" : 0,
        }
        
        final_state = agent.invoke(initial_state)

        return {"answer": final_state["answer"],
                "attempts": final_state["attempts"],
                }


