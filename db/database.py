from typing import Annotated
from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///recognition_app.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


str_64 = Annotated[str, 64]


class Base(DeclarativeBase):
    type_annotation_map = {str_64: String(64)}
