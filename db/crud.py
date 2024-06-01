from typing import List

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from db.models import User
from db.schemas import Doctor
from enums import UserType


def create_user(session: Session, user: User):
    session.add(user)
    session.flush()
    session.commit()
    return user


def get_doctors(session: Session) -> List[Doctor]:
    stmt = select(User).where(User.user_type == UserType.Doctor.value)

    result = session.execute(stmt)

    return result.scalars().all()
