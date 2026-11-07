from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Project
from schemas.task import TaskCreate
from models.task import Task

async def create_task(
        task_info:TaskCreate,
        user_id: int,
        db : AsyncSession
):
    project = await db.execute(
        select(Project)
        .where(Project.id == task_info.project_id)
        .where(Project.owner_id == user_id)
    )

    result = project.scalar_one_or_none()
    if result is None:
        return None

    task = Task(
        title=task_info.title,
        description=task_info.description,
        status=task_info.status,
        priority=task_info.priority,
        project_id=result.id
    )


    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_project_tasks(project_id:int,user_id:int,db: AsyncSession):
    project = await db.execute(select(Project).where(Project.id == project_id)
    .where(Project.owner_id == user_id))
    result = project.scalar_one_or_none()

    if result is None:
        return None

    tasks = await db.execute(select(Task).where(Task.project_id == project_id))
    result = tasks.scalars().all()
    return result