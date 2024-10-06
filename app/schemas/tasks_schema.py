from pydantic import BaseModel
from typing import Optional
from app.models.tasks_model import Type, Priority, Status


class TaskBase(BaseModel):
    type: Type
    priority: Optional[Priority] = None
    status: Status
    title: str
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    creator_id: int


class TaskCreate(BaseModel):

    type: Type
    priority: Priority
    status: Status
    title: str
    description: str
    assignee_id: int
    creator_id: int


class TaskUpdate(BaseModel):
    type: Optional[Type] = None
    priority: Optional[Priority] = None
    status: Optional[Status] = None
    title: Optional[str] = None
    description: Optional[str] = None
    assignee_id: Optional[int] = None


class TaskDelete(BaseModel):
    message: str


class TaskResponse(TaskBase):
    id: int
    created_at: str
    updated_at: str

    model_config = {
        "from_attributes": True
    }



