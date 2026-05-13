from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.models import User

router = APIRouter()


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "username": user.username}
