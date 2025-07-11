from fastapi import APIRouter
from ..models.system import SystemInfo
from ..services.system import fetch_system_info

router = APIRouter()

@router.get("/info", response_model=SystemInfo)
def get_info():
    return fetch_system_info()

@router.get("/", response_model=list[Module])
def get_modules():
    return list_modules()

@router.post("/enable")
def enable(name: str):
    enable_module(name)
    return {"status": "enabled"}

@router.post("/disable")
def disable(name: str):
    disable_module(name)
    return {"status": "disabled"}