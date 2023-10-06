from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

user = config('user')
password = config('password')
server = config('server')
db = config('db')

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{server}/{db}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
