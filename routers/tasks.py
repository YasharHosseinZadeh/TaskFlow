from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_current_user
from database import get_db
from schemas.task import TaskCreate,TaskResponse
from services.task_service import create_task as create_task_service, get_project_tasks as get_project_tasks_service
router = APIRouter()

@router.post("/tasks", response_model=TaskResponse)
async def create_task(
        task_info: TaskCreate,
        user = Depends(get_current_user),
        db : AsyncSession = Depends(get_db)
):
    result = await create_task_service(task_info, user.id,db)

    if result is None:
        raise HTTPException(status_code=404,detail="Project not found")
    return result


@router.get("/projects/{project_id}/tasks", response_model=list[TaskResponse])
async def get_tasks(
        project_id: int,
        user = Depends(get_current_user),
        db : AsyncSession = Depends(get_db)
):
    result = await get_project_tasks_service(project_id,user.id,db)
    if result is None:
        raise HTTPException(status_code=404,detail="Project not found")
    return result