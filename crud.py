import os 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import Column
from sqlalchemy import ForeignKey
from sqlalchemy.types import String, Integer
from sqlalchemy.orm import Session
import my_data_classes as schemas
from sqlalchemy import desc

from models import User, Class, User_has_Class, Note


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.idUser == user_id).first()

def get_all_classes(db: Session, user_id: int):
    queryRes = db.query(User,User_has_Class,Class).join(User_has_Class, User_has_Class.idUser==User.idUser).join(Class, Class.idClass==User_has_Class.idClass).filter(User.idUser == user_id).all()
    return [queryRes[i][2] for i in range(len(queryRes))]

def get_class(db: Session, user_id: int, class_id: int):
    queryRes = db.query(User,User_has_Class,Class).join(User_has_Class, User_has_Class.idUser==User.idUser).join(Class, Class.idClass==User_has_Class.idClass).filter(User.idUser == user_id).filter(Class.idClass == class_id).all()
    return [queryRes[i][2] for i in range(len(queryRes))]

def get_all_notes(db: Session, class_id: int, user_id: int):
    queryRes = db.query(Note).filter(Note.idUser == user_id).filter(Note.idClass == class_id).all()
    return queryRes

def delete_class(db:Session, class_id: int):
    db.query(User_has_Class).filter(User_has_Class.idClass == class_id).delete()
    db.query(Class).filter(Class.idClass == class_id).delete()
    return 1

def delete_note(db:Session, note_id: int):
    db.query(Note).filter(Note.idNote == note_id).delete()
    return 1

def update_note(db:Session, note_id: int, nota: str):
    db.query(Note).filter(Note.idNote == note_id).update({Note.nota:nota})
    return 1

def create_note(db:Session, user_id: int, class_id: int, nota: str):
    new_note =  Note(idUser = user_id, idClass = class_id, nota = nota)
    db.add(new_note)
    db.commit()
    return(new_note)

def update_class(db:Session, class_id: int, new_name: str, new_prof:str):
    db.query(Class).filter(Class.idClass == class_id).update({Class.nameClass : new_name, Class.Professor : new_prof})
    return 1


def create_class(db:Session, name_class:str, professor_name:str, user_id:int):
    new_class =  Class(nameClass = name_class, Professor = professor_name)
    db.add(new_class)
    db.commit()
    id_new_class = db.query(Class.idClass).order_by(desc(Class.idClass)).first()  #Not sure if works (works)
    new_user_has_class = User_has_Class(idUser = user_id, idClass = id_new_class)
    db.add(new_user_has_class)
    db.commit()
    return(new_class) 