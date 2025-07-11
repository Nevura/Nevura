from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ModuleBase(SQLModel):
    name: str
    description: Optional[str] = None
    enabled: bool = False

class Module(ModuleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    version: Optional[str] = None
    installed_at: Optional[datetime] = None

class ModuleCreate(ModuleBase):
    pass

class ModuleRead(ModuleBase):
    id: int
    version: Optional[str]
    installed_at: Optional[datetime]
