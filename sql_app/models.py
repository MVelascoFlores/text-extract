from sqlalchemy import (
    Boolean, 
    Column,
    ForeignKey,
    Integer,
    String,
    UUID,
    DateTime,
)

import datetime

from sqlalchemy.orm import relationship

from sql_app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    files = relationship("File", back_populates='owner')


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    index_path = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="files")
    history = relationship('FilesHistory', back_populates='file')


class FilesHistory(Base):
    __tablename__ = "files_history"

    id = Column(UUID, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.datetime.now())
    pregunta = Column(String)
    respuesta = Column(String)
    file_id = Column(Integer, ForeignKey('files.id'))
    file = relationship("File", back_populates="history")
