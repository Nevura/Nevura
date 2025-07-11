from pydantic import BaseModel

class Theme(BaseModel):
    name: str
    primary: str
    background: str
