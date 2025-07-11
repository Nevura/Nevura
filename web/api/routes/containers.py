from sqlmodel import SQLModel, Field

class Container(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    type: str  # "lxc" ou "docker"
    status: str
