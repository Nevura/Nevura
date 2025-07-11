from pydantic import BaseModel
from typing import Optional

class VMDetail(BaseModel):
    uuid: str
    name: str
    os: Optional[str]
    ip: Optional[str]
    hostname: Optional[str]
    cpu_used_percent: float
    cpu_alloc: int
    ram_used_mb: int
    ram_alloc_mb: int
    disk_used_gb: float
    disk_alloc_gb: float
    latency_percent: float
    virtio_installed: bool
