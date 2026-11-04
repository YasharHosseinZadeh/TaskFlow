

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database import get_db
from models import Project
from schemas.project import ProjectCreate, ProjectUpdate
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


async def get_projects(
        user_id : int,
        db : AsyncSession
):
    projects = await db.execute(select(Project).where(Project.owner_id == user_id))
    return projects.scalars().all()


async def get_project(
        project_id : int,
        db : AsyncSession,
        user_id : int
):
    project = await db.execute(select(Project).where(Project.id == project_id).where(Project.owner_id == user_id))
    result = project.scalar_one_or_none()
    return result


async def update_project(
        project_info : ProjectUpdate,
        db : AsyncSession,
        user_id : int,
        project_id : int
):
    user = await db.execute(select(Project).where(Project.id == project_id).where(Project.owner_id == user_id))
    project = user.scalar_one_or_none()
    if project is  None:
        return None

    x = project_info.model_dump(exclude_unset=True)

    for key, value in x.items():
        setattr(project, key, value)

    await db.commit()
    await db.refresh(project)
    return project


async def delete_project(
        project_id : int,
        user_id : int,
        db : AsyncSession
):
    project = await db.execute(select(Project).where(Project.id == project_id).where(Project.owner_id == user_id))
    result = project.scalar_one_or_none()

    if result is None:
        return None

    await db.delete(result)
    await db.commit()
    return {
        "message" : "deleted project"
    }