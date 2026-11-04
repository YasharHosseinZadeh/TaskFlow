from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from services.project_service import (create_project as create_project_service,
get_projects as get_projects_service,
get_project as get_project_service,
update_project as update_project_service,
delete_project as delete_project_service,)
from database import get_db
from dependencies import get_current_user
from models import Project
from schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter()

@router.post("/projects",response_model=ProjectResponse)
async def create_project(
        project_info: ProjectCreate,
        db : AsyncSession = Depends(get_db),
        user = Depends(get_current_user)
):

    result = await create_project_service(project_info,user.id,db)

    if result is None:
        raise HTTPException(status_code=400, detail="User id is wrong")

    return result


@router.get("/projects",response_model=List[ProjectResponse])
async def get_projects(
        user = Depends(get_current_user),
        db : AsyncSession = Depends(get_db)
):
    result = await get_projects_service(user.id,db)
    return result


@router.get("/projects/{project_id}",response_model=ProjectResponse)
async def get_project(
        project_id: int,
        db : AsyncSession = Depends(get_db),
        user = Depends(get_current_user)
):
    result = await get_project_service(project_id,db,user.id)
    if result is None:
        raise HTTPException(status_code=404, detail="Project id is wrong")
    return result


@router.patch("/projects/{project_id}",response_model=ProjectResponse)
async def update_project(
        project_info: ProjectUpdate,
        project_id: int,
        db : AsyncSession = Depends(get_db),
        user = Depends(get_current_user),
):
    project =  await update_project_service(project_info,db,user.id,project_id)


    if project is None:
        raise HTTPException(status_code=404, detail="Project id is wrong")
    return project


@router.delete("/projects/{project_id}")
async def delete_project(
        project_id: int,
        db : AsyncSession = Depends(get_db),
        user = Depends(get_current_user)
):
    result = await delete_project_service(project_id,user.id,db)
    if result is None:
        raise HTTPException(status_code=404, detail="Project id is wrong")
    return result