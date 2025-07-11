from fastapi import APIRouter
from ..models.user import User

router = APIRouter()

@router.get("/", response_model=list[User])
def list_users():
    return []