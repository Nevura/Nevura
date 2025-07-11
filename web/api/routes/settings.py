from fastapi import APIRouter
from typing import Dict
from services.settings import get_settings, update_settings

router = APIRouter()

@router.get("/")
async def read_settings():
    return await get_settings()

@router.post("/")
async def save_settings(settings: Dict):
    await update_settings(settings)
    return {"detail": "Settings updated"}
