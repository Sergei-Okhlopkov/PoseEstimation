from contextlib import contextmanager
from typing import Annotated
from sqlalchemy import create_engine, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Session

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
