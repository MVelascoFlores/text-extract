from pydantic import BaseModel
from datetime import datetime


class HistoryBase(BaseModel):
    id: int
    pregunta: str
    respuesta: str

class HistoryCreate(HistoryBase):
    pass

class History(HistoryBase):
    file_id: int
    fecha: datetime

class FileBase(BaseModel):
    id: int
    file_name: str

class FileCreate(FileBase):
    index_path: str

class File(FileBase):
    id: int
    index_path: str
    owner_id: int
    history: list[History] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    is_active: bool
    files: list[File] = []

    class Config:
        orm_mode = True

