from fastapi import APIRouter
from sqlalchemy import text
from app.db import SessionLocal

router = APIRouter()

@router.get("/db-check")
def db_check():
    with SessionLocal() as session:
        result = session.execute(text("SELECT 1")).scalar()
    return {"db_says" : result}