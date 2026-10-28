from pydantic import BaseModel, Field,ConfigDict
from models.task import TaskPriority, TaskStatus


class TaskCreate(BaseModel):
    title : str = Field(min_length= 1, max_length=200)
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    project_id : int


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    project_id: int
