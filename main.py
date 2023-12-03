from fastapi import FastAPI
from deta import Deta


deta = Deta()
usersdb = deta.Base("usersDB")
notesdb = deta.Base("notesDB")
app = FastAPI()


@app.get('/')
def home():
    return "Welcome To The TODO API"


@app.get('/users/{user_id}')
def user(user_id: str):
    if usersdb.get(user_id) != None:
        user = usersdb.get(user_id)
        return user
    else:
        return "User Not Found"


@app.post("/users/{user_id}")
def add_user(user_id: str, user_name: str):
    if usersdb.get(user_id) != None:
        return "User Already Exists"
    else:
        new_user = usersdb.put({"name": user_name}, user_id)
        return new_user, "User Added!"


@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    if usersdb.get(user_id):
        usersdb.delete(user_id)
        return "User Deleted"
    else:
        return "User Not Found"


@app.get("/users/{user_id}/notes")
def notes(user_id: str):
    if usersdb.get(user_id) != None:
        notes = notesdb.fetch({"user_Id": user_id})
        return notes
    elif notesdb.fetch({"user_Id": user_id}).count == 0:
        return "User Has No Todos Yet"
    else:
        return "User Not Found"


@app.post("/users/{user_id}/add-note/{note_id}")
def add_note(user_id: str, note_id: str, todo_data: str):
    if notesdb.get(note_id) != None:
        return "Note With That ID already exists"
    else:
        notesdb.put({"data": todo_data, "user_Id": user_id}, note_id)
        return "Note Was Added"


@app.delete("/users/{user_id}/delet-note/{note_id}")
def delete_note(user_id: str, note_id: str):
    if usersdb.get(user_id) != None and notesdb.get(note_id) != None:
        notesdb.delete(note_id)
        return "Note Was Deleted"
    else:
        return "There was an error with the entries"
