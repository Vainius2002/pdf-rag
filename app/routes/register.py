from fastapi import APIRouter, Form, Request, HTTPException
from app.services.auth import hash_password
from fastapi.templating import Jinja2Templates
from app.db import SessionLocal
from app.models import User
from sqlalchemy import select



router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html")
    

@router.post("/register")
def register(username : str = Form(), password : str = Form()):
    with SessionLocal() as session:
        existing = session.scalar(select(User).where(User.username == username))
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")
    
        user = User(
            username = username,
            password_hash=hash_password(password)
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        
        return {"id": user.id, "username" : user.username}
    
    