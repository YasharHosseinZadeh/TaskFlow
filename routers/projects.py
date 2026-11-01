

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from services.project_service import create_project as create_project_service
from database import get_db
from dependencies import get_current_user
from models import Project
from schemas.project import ProjectCreate, ProjectResponse

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



