from fastapi import APIRouter
from ..models.alerts import Alert

router = APIRouter()

@router.get("/", response_model=list[Alert])
def list_alerts():
    return []
