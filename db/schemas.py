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
