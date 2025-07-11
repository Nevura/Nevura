from pydantic import BaseModel

class VMInfo(BaseModel):
    id: str
    name: str
    status: str
    cpu: int
    ram: int
    disk: int
    os: str
