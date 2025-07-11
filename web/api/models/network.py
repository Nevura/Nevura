from sqlmodel import SQLModel

class NetworkInterface(SQLModel):
    name: str
    ip: str
    gateway: str
    dns: list[str]
