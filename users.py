from passlib.context import CryptContext

from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import User, UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_user(db_session: Session, user: UserCreate):
    hashed_password = hash_password(user.password)  
    db_user = User(
        username=user.username, 
        hashed_password=hashed_password, 
        name=user.name, 
        surname=user.surname, 
        email=user.email
        )
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user

def verify_password(
        password: str, 
        hashed_password: str
        ) -> bool:
    return pwd_context.verify(
        password, 
        hashed_password
        )

def get_user(
        db_session: Session, 
        username: str, 
        password: str
        ):
    user = db_session.query(User).filter(
        User.username == username
        ).first()
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="User not found"
            )
    if not verify_password(
        password, 
        user.hashed_password
        ):
        return False
    return user

def get_user_by_id(
        db_session: Session, 
        user_id: int
        ):
    user = db_session.query(User).filter(
        User.id == user_id
        ).first()
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="User not found."
            )
    return user

def get_user_by_username(
        db_session: Session, username: str
        ):
    user = db_session.query(User).filter(
        User.username == username
        ).first()
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="User not found."
            )
    return user