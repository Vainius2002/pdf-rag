from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from app.services.auth import verify_password, create_access_token
from app.db import SessionLocal
from app.models import User
from sqlalchemy import select



router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")


@router.post("/login")
def login(name : str = Form(), passw : str = Form()):
    with SessionLocal() as session:
        user = session.scalar(select(User).where(User.username == name))
        
        if not user or not verify_password(passw, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        token = create_access_token(user.id)
        return {"access_token" : token, "token_type" : "bearer"}
        