from sqlmodel import SQLModel

class SystemInfo(SQLModel):
    hostname: str
    timezone: str
    os_version: str