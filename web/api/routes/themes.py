from fastapi import APIRouter
from typing import List
from web.api.models.themes import Theme, ThemeCreate, ThemeRead
from services.themes import list_themes, create_theme, apply_theme

router = APIRouter()

@router.get("/", response_model=List[ThemeRead])
async def get_themes():
    return await list_themes()

@router.post("/", response_model=ThemeRead)
async def add_theme(theme: ThemeCreate):
    return await create_theme(theme)

@router.post("/apply/{theme_id}")
async def apply_theme_route(theme_id: int):
    await apply_theme(theme_id)
    return {"detail": "Theme applied"}
