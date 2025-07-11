from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Alert(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    level: str  # e.g., "info", "warning", "error"
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = None  # optional link to user
