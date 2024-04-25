from sqlalchemy import insert
from sqlalchemy.orm import Session

from db.models import User


def create_user(session: Session, user: User):
    session.add(user)
    session.flush()
    session.commit()
    return user
