from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class NodeBase(SQLModel):
    hostname: str
    ip_address: str
    mac_address: str
    online: bool = False

class Node(NodeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    last_seen: Optional[datetime] = None

class NodeCreate(NodeBase):
    pass

class NodeRead(NodeBase):
    id: int
    last_seen: Optional[datetime]
