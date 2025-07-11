from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ShareBase(SQLModel):
    name: str
    path: str
    protocol: str  # e.g., "smb", "ftp", "nfs"
    read_only: bool = False
    allowed_hosts: Optional[str] = None  # IP ranges or hostnames

class Share(ShareBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ShareCreate(ShareBase):
    pass

class ShareRead(ShareBase):
    id: int
    created_at: datetime
