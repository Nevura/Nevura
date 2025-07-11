from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ThemeBase(SQLModel):
    name: str
    description: Optional[str] = None
    is_default: bool = False
    approved: bool = False

class Theme(ThemeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ThemeCreate(ThemeBase):
    pass

class ThemeRead(ThemeBase):
    id: int
    created_at: datetime
