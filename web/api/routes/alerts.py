from fastapi import APIRouter
from typing import List
from web.api.models.alerts import Alert, AlertRead
from services.alerts import list_alerts, create_alert

router = APIRouter()

@router.get("/", response_model=List[AlertRead])
async def get_alerts():
    return await list_alerts()

@router.post("/", response_model=AlertRead)
async def add_alert(alert: Alert):
    return await create_alert(alert)

@router.get("/", response_model=List[Alert])
async def list_alerts(current_user: User = Depends(get_current_user)):
    # Ici tu peux filtrer alertes selon user, ou globales
    return AlertService.list_alerts()

@router.post("/read-all", status_code=204)
async def mark_all_read(current_user: User = Depends(get_current_user)):
    AlertService.mark_all_read()