from sqlalchemy import String,ForeignKey,Enum
from sqlalchemy.orm import Mapped,mapped_column,relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.project import Project
#     from models.comment import Comment
from database import Base


class User(Base):

    __tablename__ = 'users'

    id : Mapped[int] = mapped_column(primary_key=True)

    name : Mapped[str] = mapped_column(String(100))

    email : Mapped[str] = mapped_column(String(255),unique=True)

    password_hash : Mapped[str] = mapped_column(String(255))

    projects : Mapped[list["Project"]] = relationship( back_populates="owner")
