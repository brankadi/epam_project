from sqlalchemy.orm import Session
from models import User, UserProject, Project
from passlib.context import CryptContext

def create_user(db, username: str, password: str, name: str, email: str):
    hashed_password = hash_password(password)  
    db_user = User(username=username, password=hashed_password, name=name, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_project(db: Session, name: str, description: str, owner_id: int):
    db_project = Project(name=name, description=description, owner_id=owner_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def add_user_to_project(db: Session, user_id: int, project_id: int, role: str):
    db_user_project = UserProject(user_id=user_id, project_id=project_id, role=role)
    db.add(db_user_project)
    db.commit()
    db.refresh(db_user_project)
    return db_user_project

def get_projects(db: Session):
    return db.query(Project).all()

def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

def update_project(db: Session, project_id: int, name: str, description: str, owner_id: int):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project:
        db_project.name = name
        db_project.description = description
        db_project.owner_id = owner_id
        db.commit()
        db.refresh(db_project)
        return db_project
    return None

def delete_project(db: Session, project_id: int):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project:
        db.delete(db_project)
        db.commit()
        return db_project
    return None

def is_user_participant_in_project(db: Session, user_id: int, project_id: int) -> bool:
    user_project = db.query(UserProject).filter(
        UserProject.user_id == user_id,
        UserProject.project_id == project_id
    ).first()

    if user_project and user_project.role in ['owner', 'participant']:
        return True
    return False

def is_user_admin_in_project(db: Session, user_id: int, project_id: int) -> bool:
    user_project = db.query(UserProject).filter(
        UserProject.user_id == user_id,
        UserProject.project_id == project_id
    ).first()
    
    if user_project and user_project.role == 'admin':
        return True
    return False