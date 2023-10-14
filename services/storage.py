from fastapi import Depends
from sql_app import models
from sqlalchemy.orm import Session
from sql_app import schemas
from sql_app.database import (
    session_local,
    engine,
)
from sql_app.crud import (
    get_user_by_email as crud_get_user_by_email,
    create_file as crud_create_file,
    create_user as crud_create_user,
    login as crud_login,
    get_files as crud_get_files,
    is_file_from_user as crud_is_file_from_user,
    create_history as crud_create_history,
    get_history as crud_get_history,
)

models.Base.metadata.create_all(bind=engine)

def create_user(email, password, db:Session = session_local()):
    user = {
        'email': email,
        'password': password,
    }
    return crud_create_user(db, user)

def login(email, password, db:Session = session_local()):
    return crud_login(db, email, password)

def get_user_by_email(email, db: Session = session_local()):
    return crud_get_user_by_email(db, email)

def create_file(file_name:str, file_path:str, 
                owner:int, db:Session = session_local()):
    file: schemas.FileCreate = {
        'index_path': file_path,
        'file_name': file_name
    }
    return crud_create_file(
        db, file, owner
    )

def get_files(user:int, db: Session = session_local()):
    return crud_get_files(
        db, user
    )

def is_file_from_user(user:int, file:int, db: Session = session_local()):
    from_user = crud_is_file_from_user(db, user, file)
    if from_user:
        return from_user
    return None

def create_history(pregunta:str,
                   respuesta:str,
                   file:int,
                   db: Session = session_local()):
    history: schemas.HistoryCreate = {
        'pregunta': pregunta,
        'respuesta': respuesta,
    }
    return crud_create_history(db, history, file)

def get_history(file_id:int, 
                skip: int = 0, limit: int = 100,
                order_desc=False,
                db: Session = session_local()):
    return crud_get_history(db, file_id, skip, limit, order_desc)
