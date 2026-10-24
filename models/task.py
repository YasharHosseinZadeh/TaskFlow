from sqlalchemy import String,ForeignKey,Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.project import Project
    # from models.comment import Comment
from database import Base
from enum import Enum as PyEnum


class TaskStatus(PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskPriority(PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(Base):
    __tablename__ = "tasks"

    id : Mapped[int] = mapped_column(primary_key=True)

    title : Mapped[str] = mapped_column(String(100))

    description : Mapped[str] = mapped_column(String(500))

    status : Mapped[TaskStatus] = mapped_column(Enum(TaskStatus),default=TaskStatus.PENDING)

    priority : Mapped[TaskPriority] = mapped_column(Enum(TaskPriority),default=TaskPriority.MEDIUM)

    project_id : Mapped[int] = mapped_column(ForeignKey("projects.id"))

    project : Mapped["Project"] = relationship(back_populates="tasks")