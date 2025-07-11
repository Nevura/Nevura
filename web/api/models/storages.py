from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class StorageBase(SQLModel):
    name: str
    type: str  # e.g., "raid", "disk", "volume"
    size_gb: int
    used_gb: int = 0
    mount_point: Optional[str] = None

class StorageVolume(StorageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class StorageCreate(StorageBase):
    pass

class StorageRead(StorageBase):
    id: int
    created_at: datetime
