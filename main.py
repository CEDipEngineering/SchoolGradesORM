from os import name
from typing import List, Dict

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse


from my_data_classes import User, Subject

app = FastAPI()

known_users: Dict[int, User]

subject_matvar = Subject(
    idSubject=1, 
    nameSubject= "MatVar",
    professorName= "Fábio Orfali"
)

subject_CDados = Subject(
    idSubject=2, 
    nameSubject= "Ciência de Dados",
    professorName= "Fábio Ayres"
)

subject_modsim = Subject(
    idSubject=3, 
    nameSubject= "ModSim",
    professorName= "Fábio Pelicano"
)

user_1 = User(
    idUser= 1,
    nameUser= "Bruce Banner",
    classList= [subject_matvar, subject_CDados],
    notes= {subject_matvar.idSubject:["5.6", "8.7", "Rodei na PF"], subject_CDados.idSubject:["10 - PI"]}
)

user_2 = User(
    idUser= 2,
    nameUser= "Tony Stark",
    classList= [subject_modsim],
    notes= {subject_modsim.idSubject:["9.2", "Ultron**"]}
)

known_users = {user_1.idUser:user_1, user_2.idUser:user_2}

# @app.post("/")
# async def create_files(files: List[bytes] = File(...)):
#     return {"file_sizes": [len(file) for file in files]}

# @app.delete("/")
# async def create_upload_files(files: List[UploadFile] = File(...)):
#     return {"filenames": [file.filename for file in files]}

@app.get("/{idUser}")
async def get_root(idUser: int):
    fn = "index.html"
    if idUser not in known_users:
        fn = "error.html"
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    
    with open(fn, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Assemble response
    structured_response = ""
    structured_response+= f"<h2> Usuário: {known_users[idUser].nameUser} </h2>"
    structured_response+= "<p> Disciplinas </p>"
    structured_response+= "<ul>"
    for disc in known_users[idUser].classList:
        structured_response+= f"""<div id ='materias'><li> {disc.nameSubject} </li> 
                                    <form action='/delete_class/{idUser}' method='post'>
                                        <input type='submit' value='Delete'>
                                        <input type='hidden' value={disc.idSubject} name='idSubject'>
                                    </form>
                                    <form action='/update/' method='get'>
                                        <input type='submit' value='Edit'>
                                        <input type='hidden' value={disc.idSubject} name='idSubject'>
                                        <input type='hidden' value={idUser} name='idUser'>
                                    </form></div>
                                """
        structured_response+= "<ul>"
        for note in known_users[idUser].notes[disc.idSubject]:
            structured_response+= f"<li> {note} </li>"
        structured_response+= "</ul>"
    structured_response+= "</ul>"

    structured_response += f"<div id = 'add'><form action='/create/{idUser}' method='get'><input type='submit' value='Add'></form></div>"

    # Update html and send
    content = content.replace("[INSERT USER CONTENT HERE]", structured_response)    
    return HTMLResponse(content=content)

@app.get("/update/")
async def update_class(idUser: int, idSubject: int):
    fn = "update.html"
    if idUser not in known_users or idSubject not in [i.idSubject for i in known_users[idUser].classList]:
        fn = "error.html"
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    
    user = known_users[idUser]
    subject = user.classList[[i.idSubject for i in user.classList].index(idSubject)]

    with open(fn, "r", encoding="utf-8") as f:
        content = f.read()

    resp = ""
    i = 0
    for e in user.notes[idSubject]:
        resp += f'<input type="text" name="notes" value="{e}"></br>'
        i +=1

    resp += '<p>Nova anotação:</p>'
    resp += f'<input type="text" name="notes"></br>'
    
    # Update html and send
    content = content.replace("[NOME DA DISCIPLINA]", f"{subject.nameSubject}")
    content = content.replace("[NOME DO PROFESSOR]", f"{subject.professorName}")
    content = content.replace("[ANOTAÇÕES]", resp)    
    content = content.replace("[ID_USUÁRIO]", str(idUser))
    content = content.replace("[ID_SUBJECT]", str(idSubject))
    return HTMLResponse(content=content)

@app.get("/create/{idUser}")
async def create_class(idUser: int):
    fn = "create.html"
    if idUser not in known_users:
        fn = "error.html"
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)    
    with open(fn, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("[ID_USUÁRIO]", str(idUser))
    content = content.replace("[ID_NOVO]", str(len(known_users[idUser].classList)+1))
    return HTMLResponse(content=content)

@app.post("/{idUser}")
async def post_new_class(idUser: int, nameSubject: str = Form(...), professorName: str = Form(...), idSubject: int = Form(...)):
    if idUser not in known_users:
        fn = "error.html"
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)    
    new_subject = Subject(idSubject=idSubject, nameSubject=nameSubject, professorName=professorName)
    if new_subject.nameSubject in [i.nameSubject for i in known_users[idUser].classList]:
        return RedirectResponse(url=f"/create/{idUser}",status_code=302)
    known_users[idUser].classList.append(new_subject)
    known_users[idUser].notes[new_subject.idSubject] = []
    return RedirectResponse(url=f"/{idUser}",status_code=302)

# Era pra ser um PUT/PATCH, mas o form do HTML não suporta nenhum verbo exceto GET/POST
@app.post("/update_class_info/{idUser}")
async def update_class(idUser: int, idSubject: int = Form(...), subject_name: str = Form(...), professor_name: str = Form(...), notes: List[str] = Form(...)):
    if idUser not in known_users:
        fn = "error.html"
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content) 
    
    user = known_users[idUser]
    subject = user.classList[[i.idSubject for i in user.classList].index(idSubject)]
    if subject_name in [i.nameSubject for i in known_users[idUser].classList]:
        return RedirectResponse(url=f"/update/{idUser}",status_code=302)
    subject.nameSubject = subject_name
    subject.professorName = professor_name
    user.notes[idSubject] = notes.copy()
    return RedirectResponse(url=f"/{idUser}",status_code=302)
 
# DELETE, só que não
@app.post("/delete_class/{idUser}")
async def update_class(idUser: int, idSubject: int = Form(...)):
    if idUser not in known_users or idSubject not in [i.idSubject for i in known_users[idUser].classList]:
        fn = "error.html"
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content) 
    
    user = known_users[idUser]
    user.classList.remove(user.classList[[i.idSubject for i in known_users[idUser].classList].index(idSubject)])
    user.notes.pop(idSubject) # Memory leak warning, must remove here too

    return RedirectResponse(url=f"/{idUser}",status_code=302)