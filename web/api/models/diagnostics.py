from sqlmodel import SQLModel

class Diagnostics(SQLModel):
    cpu_load: float
    memory_used: int
    memory_total: int
    disk_used: int
    disk_total: int
