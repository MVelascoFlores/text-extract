import bcrypt

from sqlalchemy.orm import Session

from sql_app import models, schemas


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
    user['hashed_password'] = hash_password(user['password'])
    del(user['password'])
    db_user = models.User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login(db: Session, email, password):
    user =  db.query(models.User).filter(
        models.User.email == email,
    ).first()
    is_correct = verify_password(password, user.hashed_password)
    if not is_correct:
        return False
    return user 

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(
        models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(
        models.User.email == email).first()

def create_file(db: Session, file: schemas.FileCreate, owner:int):
    db_file = models.File(**file, owner_id=owner)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_files(db: Session, user:int, 
              skip: int = 0, limit: int = 100):
    return db.query(models.File).filter(
        models.File.owner_id == user) \
        .offset(skip) \
        .limit(limit) \
        .all()

def is_file_from_user(db: Session, user:int, file:int):
    return db.query(models.File).filter(
        models.File.id == file,
        models.File.owner_id == user).first()
