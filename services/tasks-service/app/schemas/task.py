from datetime import datetime
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_done: bool | None = None

class TaskResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: str | None
    is_done: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
