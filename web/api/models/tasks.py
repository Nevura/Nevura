from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class TaskBase(SQLModel):
    name: str
    schedule: str  # cron format
    command: str
    enabled: bool = True

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    last_run: Optional[datetime]
    next_run: Optional[datetime]
    created_at: datetime
