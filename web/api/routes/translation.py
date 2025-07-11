from fastapi import APIRouter, Query
from typing import Dict
from ..services.translation import load_language

router = APIRouter(prefix="/translation", tags=["translation"])

@router.get("/")
async def get_translations(lang: str = Query(default="en")) -> Dict[str, str]:
    return load_language(lang)
