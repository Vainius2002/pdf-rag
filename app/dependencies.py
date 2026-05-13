import jwt
from fastapi import Header, HTTPException
from sqlalchemy import select

from app.db import SessionLocal
from app.models import User
from app.services.auth import decode_token


def get_current_user(authorization: str = Header()) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = authorization.removeprefix("Bearer ")

    try:
        user_id = decode_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    with SessionLocal() as session:
        user = session.scalar(select(User).where(User.id == user_id))
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
