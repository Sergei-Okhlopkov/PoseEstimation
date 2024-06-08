from datetime import datetime
from typing import List

from pydantic import BaseModel


class SelectPatient(BaseModel):
    id: int
    first_name: str
    second_name: str
    patronymic: str


class Doctor(BaseModel):
    id: int
    first_name: str
    second_name: str
    patronymic: str


class MedSessionUpdate(BaseModel):
    finished_at: datetime
    max_angle: int
    avg_speed: int


class GraphData(BaseModel):
    angle: List[int]
    speed: List[int]
    date: List[datetime]
