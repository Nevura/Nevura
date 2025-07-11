from fastapi import APIRouter
from ..models.modules import Module

router = APIRouter()

@router.get("/", response_model=list[Module])
def list_modules():
    return []
