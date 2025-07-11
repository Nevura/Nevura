from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    is_admin: bool = False
    oauth_access_token: Optional[str] = None  # token chiffré
    oauth_refresh_token: Optional[str] = None  # token chiffré
