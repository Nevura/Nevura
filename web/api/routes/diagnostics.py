from fastapi import APIRouter
from ..services.diagnostics import get_diagnostics
from ..models.diagnostics import Diagnostics

router = APIRouter()

@router.get("/", response_model=Diagnostics)
def diagnostics():
    return get_diagnostics()
