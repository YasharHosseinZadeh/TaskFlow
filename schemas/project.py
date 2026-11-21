from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length = 1,max_length=100)
    description: str | None = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    name: str
    description: str | None
    owner_id : int


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None