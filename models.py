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

from database import Base


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