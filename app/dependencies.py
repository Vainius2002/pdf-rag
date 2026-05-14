import jwt
from fastapi import Header, HTTPException
from app.services.auth import decode_token
from app.db import SessionLocal
from sqlalchemy import select
from app.models import User




def get_current_user(authorization : str = Header()):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = authorization.removeprefix("Bearer ")
    try:
        user_id = decode_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalid")

    with SessionLocal() as session:
        user = session.scalar(select(User).where(User.id == user_id))
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
