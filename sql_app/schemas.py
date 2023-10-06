from pydantic import BaseModel


class FileBase(BaseModel):
    id: int
    file_name: str

class FileCreate(FileBase):
    index_path: str

class File(FileBase):
    id: int
    index_path: str
    owner_id: int

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

