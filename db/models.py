import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped
from db.database import Base, str_64
from enums import ExerciseType, UserType

int_pk = Annotated[int, mapped_column(primary_key=True)]


# TODO: переделать password на hash
class User(Base):
    __tablename__ = "users"
    id: Mapped[int_pk]
    med_session_id: Mapped[int | None] = mapped_column(
        ForeignKey("med_sessions.id"), nullable=True
    )
    comment_id: Mapped[int | None] = mapped_column(
        ForeignKey("comments.id"), nullable=True
    )
    first_name: Mapped[str_64]
    last_name: Mapped[str_64]
    patronymic: Mapped[str_64 | None] = mapped_column(
        nullable=True
    )  # отчество необязательное поле
    login: Mapped[str_64]
    password: Mapped[str_64]
    email: Mapped[str_64]
    user_type: Mapped[int]


class MedSession(Base):
    __tablename__ = "med_sessions"
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    started_at: Mapped[datetime.datetime]
    finished_at: Mapped[datetime.datetime]
    exercise_type: Mapped[ExerciseType]
    max_angle: Mapped[int]
    avg_speed: Mapped[int]


class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int_pk]
    text: Mapped[str]
    date: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), onupdate=datetime.datetime.utcnow()
    )
    exercise_type: Mapped[ExerciseType]
