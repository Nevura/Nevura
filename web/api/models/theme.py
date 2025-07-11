from sqlmodel import SQLModel, Field

class Theme(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    is_active: bool
