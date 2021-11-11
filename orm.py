import os 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import Column
from sqlalchemy import ForeignKey
from sqlalchemy.types import String, Integer
from sqlalchemy.orm import Session
import my_data_classes as schemas


'''
Must create a file named "secret.txt",
inside root directory, containing the password and
username, in the same order as bellow, 
separated by an "=" sign

Password=ex4mpl3_p4sswd
Username=example_user
'''

try:
    with open("./secret.txt", "r") as s:
        cont = s.read().split("\n")
        MYSQL_DB_USERNAME = cont[0].split("=")[1]
        MYSQL_DB_PASSWORD = cont[1].split("=")[1]
except FileNotFoundError as e:
    print(f"Unable to locate secrets file! {e}")
    exit(1)

if MYSQL_DB_PASSWORD is None or MYSQL_DB_USERNAME is None:
    print("Invalid credentials!")
    exit(1)

# print(f"Credentials found: {MYSQL_DB_USERNAME=},{MYSQL_DB_PASSWORD=}")

DATABASE_URL = f"mysql+mysqldb://{MYSQL_DB_USERNAME}:{MYSQL_DB_PASSWORD}@localhost/notas"

db_engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

Base = declarative_base()

# =====================================
# Schema
# =====================================

class User (Base):
    __tablename__ = "User"

    idUser =  Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    nameUser = Column(String)

class User_has_Class (Base):
    __tablename__ = "User_has_Class"

    idUser =  Column(Integer, ForeignKey("User.idUser"), nullable=False, primary_key=True)
    idClass = Column(Integer, ForeignKey("Class.idClass"),nullable=False, primary_key=True)

class Class (Base):
    __tablename__ = "Class"
    
    idClass = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    nameClass = Column(String, nullable=False)
    Professor = Column(String)

class Note (Base):
    __tablename__ = "Note"

    idNote = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    idUser = Column(Integer, ForeignKey("User.idUser"), nullable=False)
    idClass = Column(Integer, ForeignKey("Class.idClass"), nullable=False)
    nota = Column(String)

# ======================================
# C.R.U.D.
# ======================================

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.idUser == user_id).first()

def get_all_subjects(db: Session, user_id: int):
    queryRes = db.query(User,User_has_Class,Class).join(User_has_Class, User_has_Class.idUser==User.idUser).join(Class, Class.idClass==User_has_Class.idClass).filter(User.idUser == user_id).all()
    return [queryRes[i][2] for i in range(len(queryRes))]

def get_all_notes(db: Session, class_id: int, user_id: int):
    queryRes = db.query(Note).filter(Note.idUser == user_id).filter(Note.idClass == class_id).all()
    return queryRes

def delete_subject(db:Session, class_id: int):
    db.query(User_has_Class).filter(User_has_Class.idClass == class_id).delete()
    db.query(Class).filter(Class.idClass == class_id).delete()
    return 1

def delete_note(db:Session, note_id: int):
    db.query(Note).filter(Note.idNote == note_id).delete()
    return 1


'''
Get user (id) --OK
Get all subjects (user.id) --OK
Get all notes (subject.id and user.id) -- OK
Delete subject (subject.id) -- OK
Delete note (note.id) -- OK
Update note (note.id, newVal)
Update subject (subject.id, newName, newProf)
Create Subject (user.id, name, prof*)
Create note (user.id, class.id, newVal)
'''














# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()

# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()

# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()

# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
