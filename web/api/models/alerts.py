from pydantic import BaseModel
from datetime import datetime

class Alert(BaseModel):
    id: int
    title: str
    message: str
    severity: str
    created_at: datetime
