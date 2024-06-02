from contextlib import contextmanager
from typing import Annotated
from sqlalchemy import create_engine, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Session

from db.crud import create_user
from db.hash_password import get_hash
from db.models import User

DATABASE_URL = "sqlite:///recognition_app.db"

engine = create_engine(DATABASE_URL)


str_64 = Annotated[str, 64]


class Base(DeclarativeBase):
    type_annotation_map = {str_64: String(64)}


@contextmanager
def get_session() -> Session:
    session = Session(bind=engine)
    try:
        yield session
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()


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
