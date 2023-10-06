from fastapi.security import OAuth2PasswordBearer
from fastapi import (
    Depends, 
    HTTPException,
    status,
)

from jose import jwt, JWTError

from decouple import config

from services.storage import get_user_by_email

from datetime import datetime, timedelta


SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES', cast=int)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token/")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email:str = payload.get("email")
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user

def create_access_token(data: dict, 
    expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES):
    """
        create the access token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, 
        algorithm=ALGORITHM)
    return encoded_jwt