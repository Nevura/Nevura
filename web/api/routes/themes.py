from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

# Thèmes du store (simulé)
STORE_THEMES = [
    {"id": "theme1", "name": "Blue Classic", "approved": True, "source": "store"},
    {"id": "theme2", "name": "Solarized Dark", "approved": True, "source": "store"},
    {"id": "theme3", "name": "Experimental Red", "approved": False, "source": "store"},
]

@router.get("/store")
async def get_store_themes():
    return JSONResponse(content=STORE_THEMES)

@router.get("/", response_model=list[Theme])
def get_themes():
    return list_themes()

@router.post("/activate")
def activate(name: str):
    activate_theme(name)
    return {"status": "activated"}