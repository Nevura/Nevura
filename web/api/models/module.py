from sqlmodel import SQLModel, Field

class Module(SQLModel, table=True):
    name: str = Field(primary_key=True)
    installed: bool
