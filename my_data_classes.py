from typing import List, Dict
from pydantic import BaseModel

class Subject(BaseModel):
    """
    Subject that is beign undertaken by a student,
    contains notes and possibly professor name.
    nameSubject must be unique.
    """
    idSubject: int
    nameSubject: str
    professorName: str

class User(BaseModel):
    """
    User of application.
    """
    idUser: int
    nameUser: str
    classList: List[Subject]
    notes: Dict[int, List[str]]


