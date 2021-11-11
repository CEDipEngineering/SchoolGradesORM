from pydantic import BaseModel

class User (BaseModel):
    idUser: int
    nameUser: str

class User_has_Class (BaseModel):
    idUser: int
    idClass: int

class Class (BaseModel):
    idSubject: int
    nameSubject: str
    professorName: str

class Note (BaseModel):
    idNote: int
    idUser: int
    idClass: int
    nota: str