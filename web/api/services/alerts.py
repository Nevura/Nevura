from typing import List
from web.api.models.alerts import Alert, AlertRead

async def list_alerts() -> List[AlertRead]:
    # Liste alertes système
    pass

async def create_alert(alert: Alert) -> AlertRead:
    # Crée nouvelle alerte
    pass
