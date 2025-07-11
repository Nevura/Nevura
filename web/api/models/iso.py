from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class ISO(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    size_bytes: int
    os_family: Optional[str] = None  # e.g., "windows", "linux", "macos"
    version: Optional[str] = None
    added_at: datetime = Field(default_factory=datetime.utcnow)
