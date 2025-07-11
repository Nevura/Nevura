from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Diagnostic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    status: str
    result: Optional[str] = None
    checked_at: datetime = Field(default_factory=datetime.utcnow)
