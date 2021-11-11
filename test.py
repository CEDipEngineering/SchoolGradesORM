import orm, my_data_classes
from orm import SessionLocal, db_engine

orm.Base.metadata.create_all(bind=db_engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db = next(get_db())

d = orm.get_all_notes(db=db, user_id=3, class_id=3)
print([d[i].nota for i in range(len(d))])
# print(d[0].nameUser)
# print(d)

e = orm.delete_note(db, 4)

d = orm.get_all_notes(db=db, user_id=3, class_id=3)
print([d[i].nota for i in range(len(d))])

