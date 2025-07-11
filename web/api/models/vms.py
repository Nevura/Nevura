from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class VMBase(SQLModel):
    name: str
    vm_type: str  # e.g., "qemu", "lxc", "docker", "jail"
    status: str   # e.g., "running", "stopped"
    cpu_cores: int
    ram_mb: int
    storage_gb: int
    ip_address: Optional[str] = None
    os_name: Optional[str] = None
    hostname: Optional[str] = None

class VM(VMBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class VMCreate(VMBase):
    pass

class VMRead(VMBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
