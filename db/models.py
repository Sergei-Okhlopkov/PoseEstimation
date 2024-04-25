import datetime
from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from db.database import Base, str_64
from enums import ExerciseType

int_pk = Annotated[int, mapped_column(primary_key=True)]


# TODO: переделать password на hash
class User(Base):
    __tablename__ = "users"
    id: Mapped[int_pk]
    first_name: Mapped[str_64]
    last_name: Mapped[str_64]
    patronymic: Mapped[str_64 | None]  # отчество необязательное поле
    login: Mapped[str_64]
    password: Mapped[str_64]
    email: Mapped[str_64]


class MedSession(Base):
    __tablename__ = "med_session"
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    started_at: Mapped[datetime.datetime]
    finished_at: Mapped[datetime.datetime]
    exercise_type: Mapped[ExerciseType]
    max_angle: Mapped[int]
    avg_speed: Mapped[int]
    comment: Mapped[str]
    comment_date: Mapped[datetime.datetime]
