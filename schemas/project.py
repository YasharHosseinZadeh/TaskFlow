from pydantic import BaseModel,Field,ConfigDict


class ProjectCreate(BaseModel):
    name: str = Field(max_length=100)
    description: str | None = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    name: str
    description: str | None
    owner_id : int