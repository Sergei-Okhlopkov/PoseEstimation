from typing import List, Optional

from sqlalchemy import select, update, and_
from sqlalchemy.orm import Session

from db.database import get_session
from db.hash_password import get_hash
from db.models import User, MedSession, Comment
from db.schemas import Doctor, MedSessionUpdate
from enums import UserType


def create_user(session: Session, user: User):
    session.add(user)
    session.flush()
    session.commit()
    return user


def create_comment(session: Session, comment: Comment):
    session.add(comment)
    session.flush()
    session.commit()


def get_last_comment_by_exercise_for_user(
    session: Session,
    excercise_type: int,
    user_id: int,
) -> Comment | None:
    # stmt = (
    #     select(Comment)
    #     .where(
    #         and_(Comment.user_id == user_id, Comment.exercise_type == excercise_type)
    #     )
    #     .order_by(Comment.date.desc())
    # )
    comment = (
        session.query(Comment)
        .filter_by(user_id=user_id, exercise_type=excercise_type)
        .order_by(Comment.date.desc())
        .one_or_none()
    )
    return comment
    # return session.execute(stmt).one_or_none()


def get_doctors(session: Session) -> List[Doctor]:
    stmt = select(User).where(User.user_type == UserType.Doctor.value)
    result = session.execute(stmt)

    return result.scalars().all()


def create_med_session(session: Session, med_session: MedSession) -> MedSession:
    session.add(med_session)
    session.commit()
    session.refresh(med_session)
    return med_session


def update_med_session(
    session: Session, med_session_id: int, med_session: MedSessionUpdate
) -> None:
    stmt = (
        update(MedSession)
        .where(MedSession.id == med_session_id)
        .values(
            finished_at=med_session.finished_at,
            max_angle=med_session.max_angle,
            avg_speed=med_session.avg_speed,
        )
    )

    session.execute(stmt)
    session.commit()


def get_user_by_id(session: Session, user_id: int) -> User:
    stmt = select(User).where(User.id == user_id)
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


def get_user_med_sessions_by_exercise_type(
    session: Session, user_id: int, exercise_type: int, limit: int = 10
) -> List[MedSession]:
    stmt = (
        select(MedSession)
        .where(
            and_(
                MedSession.user_id == user_id,
                MedSession.exercise_type == exercise_type,
            )
        )
        .order_by(MedSession.finished_at)
        .limit(limit)
    )

    result = session.execute(stmt)
    return result.scalars().all()


def fill_db_data():
    with get_session() as session:
        users = [
            User(
                last_name="Здоровьев",
                first_name="Николай",
                patronymic="Сергеевич",
                login="vrach",
                password=get_hash("123"),
                email="vrach@mail.ru",
                user_type=2,
                doctor_id=None,
            ),
            User(
                last_name="Неболеев",
                first_name="Фёдор",
                patronymic=None,
                login="neboleev",
                password=get_hash("123"),
                email="neboleev@mail.ru",
                user_type=2,
                doctor_id=None,
            ),
            User(
                last_name="Охлопков",
                first_name="Сергей",
                patronymic="Михайлович",
                login="ser",
                password=get_hash("123"),
                email="sergei@mail.ru",
                user_type=1,
                doctor_id=1,
            ),
            User(
                last_name="Шприцов",
                first_name="Александр",
                patronymic=None,
                login="shpritsov",
                password=get_hash("123"),
                email="shpritsov@mail.ru",
                user_type=2,
                doctor_id=None,
            ),
            User(
                last_name="Солодухина",
                first_name="Анастасия",
                patronymic="Романовна",
                login="anastas",
                password=get_hash("123"),
                email="anastas@mail.ru",
                user_type=1,
                doctor_id=4,
            ),
            User(
                last_name="Дачников",
                first_name="Сергей",
                patronymic="Николаевич",
                login="dach",
                password=get_hash("123"),
                email="dach@mail.ru",
                user_type=2,
                doctor_id=None,
            ),
            User(
                last_name="Пионтко",
                first_name="Ярослав",
                patronymic="Владимирович",
                login="yar",
                password=get_hash("123"),
                email="yar@mail.ru",
                user_type=1,
                doctor_id=4,
            ),
        ]

        for user in users:
            create_user(session, user)
