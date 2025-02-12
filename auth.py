from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

load_dotenv() 

SECRET_KEY = os.getenv(
    "SECRET_KEY", 
    "default_secret_key"
    ) 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update(
        {
            "exp": expire,
            "sub": str(data["sub"]),
            "token_type": "bearer"}
            )
    encoded_jwt = jwt.encode(
        to_encode, 
        SECRET_KEY, 
        algorithm=ALGORITHM
        )
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    
def get_current_user(
        token: str = Depends(oauth2_scheme), 
        db_session: Session = Depends(get_db)):
    from users import get_user_by_id
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials."
            )
    
    user_id: int = payload.get("sub") 
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token data."
            )

    user = get_user_by_id(db_session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found."
            )
    print(user)
    return user

    



