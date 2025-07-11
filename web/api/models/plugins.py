from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class PluginBase(SQLModel):
    name: str
    description: Optional[str] = None
    version: Optional[str] = None
    enabled: bool = False

class Plugin(PluginBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    installed_at: Optional[datetime] = None

class PluginCreate(PluginBase):
    pass

class PluginRead(PluginBase):
    id: int
    installed_at: Optional[datetime]
