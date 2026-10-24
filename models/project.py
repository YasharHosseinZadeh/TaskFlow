from sqlalchemy import String,ForeignKey,Enum
from sqlalchemy.orm import Mapped,mapped_column,relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.user import User
    from models.task import Task
from database import Base


class Project(Base):
    __tablename__ = 'projects'

    id : Mapped[int] = mapped_column(primary_key=True)

    name : Mapped[str] = mapped_column(String(100))

    description : Mapped[str] = mapped_column(String(500))

    owner_id : Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner : Mapped["User"] = relationship(back_populates="projects")

    tasks : Mapped[list["Task"]] = relationship(back_populates="project")