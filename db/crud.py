from typing import List

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from db.database import get_session
from db.hash_password import get_hash
from db.models import User, MedSession
from db.schemas import Doctor, MedSessionUpdate
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


def create_med_session(session: Session, med_session: MedSession) -> MedSession:
    session.add(med_session)
    # session.flush()
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
                login="sergei",
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
