from os import name
from typing import List, Dict

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Depends, FastAPI, HTTPException

import crud
import models
import my_data_classes
from database import SessionLocal, db_engine



models.Base.metadata.create_all(bind=db_engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# css
app.mount("/static", StaticFiles(directory="static"), name="static")

# known_users: Dict[int, User]

# subject_matvar = Subject(
#     idSubject=1, 
#     nameSubject= "MatVar",
#     professorName= "Fábio Orfali"
# )

# subject_CDados = Subject(
#     idSubject=2, 
#     nameSubject= "Ciência de Dados",
#     professorName= "Fábio Ayres"
# )

# subject_modsim = Subject(
#     idSubject=3, 
#     nameSubject= "ModSim",
#     professorName= "Fábio Pelicano"
# )

# user_1 = User(
#     idUser= 1,
#     nameUser= "Bruce Banner",
#     classList= [subject_matvar, subject_CDados],
#     notes= {subject_matvar.idSubject:["5.6", "8.7", "Rodei na PF"], subject_CDados.idSubject:["10 - PI"]}
# )

# user_2 = User(
#     idUser= 2,
#     nameUser= "Tony Stark",
#     classList= [subject_modsim],
#     notes= {subject_modsim.idSubject:["9.2", "Ultron**"]}
# )

# known_users = {user_1.idUser:user_1, user_2.idUser:user_2}

@app.get("/{idUser}")
async def get_root(idUser: int, db: SessionLocal = Depends(get_db)):
    #Get info from DB
    
    try:
        user_info = crud.get_user(db, idUser) 
        if user_info is None:
            raise KeyNotFoundError
        fn = "index.html"
    except Exception as e:
        print(e)
        fn = "error.html"
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    
    classes_info = crud.get_all_classes(db, idUser)

    with open(fn, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Assemble response
    structured_response = ""
    structured_response+= f"<h2> Usuário: {user_info.nameUser} </h2>"
    structured_response+= "<p> Disciplinas </p>"
    structured_response+= "<ul>"
    for disc in classes_info:
        structured_response+= f"""<div id ='materias'><li> {disc.nameClass} </li> 
                                    <form action='/delete_class/{idUser}' method='post'>
                                        <input type='submit' value='Delete'>
                                        <input type='hidden' value={disc.idClass} name='idClass'>
                                    </form>
                                    <form action='/update/' method='get'>
                                        <input type='submit' value='Edit'>
                                        <input type='hidden' value={disc.idClass} name='idClass'>
                                        <input type='hidden' value={idUser} name='idUser'>
                                    </form></div>
                                """
        structured_response+= "<ul>"
        notes_info = crud.get_all_notes(db, disc.idClass, idUser)
        for note in notes_info:
            structured_response+= f"<li> {note.nota} </li>"
        structured_response+= "</ul>"
    structured_response+= "</ul>"

    structured_response += f"<div id = 'add'><form action='/create/{idUser}' method='get'><input type='submit' value='Add'></form></div>"

    # Update html and send
    content = content.replace("[INSERT USER CONTENT HERE]", structured_response)    
    return HTMLResponse(content=content)

@app.get("/update/")
async def update_class(idUser: int, idClass: int, db: SessionLocal = Depends(get_db)):

    fn = "update.html"
    try:
        user_info = crud.get_user(db, idUser) 
        if user_info is None:
            raise KeyNotFoundError
    except Exception as e:
        print(e)
        fn = "error.html"
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)

    try:
        class_info = crud.get_class(db, idUser, idClass) 
        if class_info is None:
            raise KeyNotFoundError
    except Exception as e:
        print(e)
        fn = "error.html"
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)

    
    all_notes = crud.get_all_notes(db, idClass, idUser)



    with open(fn, "r", encoding="utf-8") as f:
        content = f.read()

    resp = ""
    i = 0
    for e in all_notes:
        resp += f'<input type="text" name="notes" value="{e.nota}"></br>'
        i +=1

    resp += '<p>Nova anotação:</p>'
    resp += f'<input type="text" name="notes"></br>'
    
    # Update html and send
    content = content.replace("[NOME DA DISCIPLINA]", f"{class_info[0].nameClass}")
    content = content.replace("[NOME DO PROFESSOR]", f"{class_info[0].Professor}")
    content = content.replace("[ANOTAÇÕES]", resp)    
    content = content.replace("[ID_USUÁRIO]", str(idUser))
    content = content.replace("[ID_CLASS]", str(idClass))
    return HTMLResponse(content=content)

@app.get("/create/{idUser}")
async def create_class(idUser: int, db: SessionLocal = Depends(get_db)):
    fn = "create.html"
    try:
        user_info = crud.get_user(db, idUser) 
        if user_info is None:
            raise KeyNotFoundError
    except Exception as e:
        print(e)
        fn = "error.html"
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)

    classes_info = crud.get_all_classes(db, idUser)

    
    with open(fn, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("[ID_USUÁRIO]", str(idUser))
    return HTMLResponse(content=content)

@app.post("/{idUser}")
async def post_new_class(idUser: int, nameClass: str = Form(...), professorName: str = Form(...), db: SessionLocal = Depends(get_db)):
    try:
        user_info = crud.get_user(db, idUser) 
        if user_info is None:
            raise KeyNotFoundError
    except Exception as e:
        print(e)
        fn = "error.html"
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)


    all_classes = crud.get_all_classes(db, idUser)
    if nameClass.lower().strip() in [e.nameClass.lower().strip() for e in all_classes]:
        RedirectResponse(url = f"/create/{idUser}", status_code = 302)

    crud.create_class(db, nameClass, professorName, idUser)

    return RedirectResponse(url=f"/{idUser}",status_code=302)

# Era pra ser um PUT/PATCH, mas o form do HTML não suporta nenhum verbo exceto GET/POST
@app.post("/update_class_info/{idUser}")
async def update_class(idUser: int, idClass: int = Form(...), nameClass: str = Form(...), professor_name: str = Form(...), notes: List[str] = Form(...), db: SessionLocal = Depends(get_db)):
    try:
        user_info = crud.get_user(db, idUser) 
        if user_info is None:
            raise KeyNotFoundError
    except Exception as e:
        print(e)
        fn = "error.html"
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content) 
    
    try:
        class_info = crud.get_class(db, idUser, idClass) 
        if class_info is None:
            raise KeyNotFoundError
    except Exception as e:
        print(e)
        fn = "error.html"
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    
    if nameClass.lower().strip() in [e.nameClass.lower().strip() for e in class_info]:
        RedirectResponse(url = f"/update/?idUser={idUser}&idClass={idClass}", status_code = 302)

    #def update_class(db:Session, class_id: int, new_name: str, new_prof:str):

    all_notes = crud.get_all_notes(db, idClass, idUser)
    new_notes = [n for n in notes if (n is not None and n.strip() != "")] # Copia só os não nulos
    if len(new_notes) != all_notes:
        crud.create_note(db, idUser, idClass, new_notes[-1])
    for i in range(len(all_notes)):
        crud.update_note(db, all_notes[i].idNote, new_notes[i])


    return RedirectResponse(url=f"/{idUser}",status_code=302)
 
# DELETE, só que não
@app.post("/delete_class/{idUser}")
async def update_class(idUser: int, idSubject: int = Form(...), db: SessionLocal = Depends(get_db)):
    if idUser not in known_users or idSubject not in [i.idSubject for i in user_info.classList]:
        fn = "error.html"
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content) 
    
    user = user_info
    user.classList.remove(user.classList[[i.idSubject for i in user_info.classList].index(idSubject)])
    user.notes.pop(idSubject) # Memory leak warning, must remove here too

    return RedirectResponse(url=f"/{idUser}",status_code=302)