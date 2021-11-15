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