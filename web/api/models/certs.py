from sqlmodel import SQLModel, Field

class Cert(SQLModel):
    name: str
    valid_until: str
    issuer: str
