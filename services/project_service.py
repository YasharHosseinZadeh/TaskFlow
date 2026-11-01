from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database import get_db
from models import Project
from schemas.project import ProjectCreate
from models.user import User

async def create_project(
        project_info : ProjectCreate,
        user_id : int,
        db : AsyncSession = Depends(get_db)
):


    project = Project(
        name = project_info.name,
        description = project_info.description,
        owner_id = user_id
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)

    result = await db.execute(
        select(Project)
        .options(selectinload(Project.owner))
        .where(Project.id == project.id)
    )

    project = result.scalar_one()
    return project

