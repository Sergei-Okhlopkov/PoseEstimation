from typing import List

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from db.models import User
from db.schemas import Doctor
from enums import UserType


def create_user(session: Session, user: User):
    # TODO: переделать на insert
    session.add(user)
    session.flush()
    session.commit()
    return user


def get_doctors(session: Session) -> List[Doctor]:
    stmt = select(User).where(User.user_type == UserType.Doctor.value)
    result = session.execute(stmt)

    return result.scalars().all()


def get_user_by_id(session: Session, id: int) -> User:
    stmt = select(User).where(User.id == id)
    result = session.execute(stmt)

    return result.scalars().one_or_none()


def get_user_by_login(session: Session, login: str) -> User:
    stmt = select(User).where(User.login == login)
    result = session.execute(stmt)

    return result.scalars().one_or_none()


def get_patients_by_doctor_id(session: Session, doctor_id: int):
    stmt = select(User).where(User.doctor_id == doctor_id)
    result = session.execute(stmt)

    return result.scalars().all()
