from datetime import datetime, timezone

from sqlalchemy.orm import Session
from fastapi import Depends

from models import User, UserProject, Project, Role
from users import get_user

def create_project(
        db_session: Session, 
        name: str, 
        description: str,
        owner_id: int,
        created_at: datetime,
        modified_by: str = 'admin'
        ):
    created_at = created_at or datetime.now(timezone.utc)
    
    db_project = Project(
        name=name, 
        description=description, 
        owner_id=owner_id,
        created_at=created_at,
        modified_by=modified_by
        )
    db_session.add(db_project)
    db_session.commit()
    db_session.refresh(db_project)

    db_user_project = UserProject(
        user_id=owner_id, 
        project_id=db_project.id, 
        role=Role.owner
        )
    db_session.add(db_user_project)
    db_session.commit()

    return db_project

def add_user_to_project(
        db_session: Session, 
        user_id: int, 
        project_id: int, 
        role: str
        ):
    db_user_project = UserProject(
        user_id=user_id, 
        project_id=project_id, 
        role=role
        )
    db_session.add(db_user_project)
    db_session.commit()
    db_session.refresh(db_user_project)
    return db_user_project

def get_projects(db_session: Session):
    return db_session.query(Project).all()

def get_project(db_session: Session, project_id: int):
    return db_session.query(Project).filter(
        Project.id == project_id
        ).first()

def is_user_participant_in_project(
        db_session: Session, 
        user_id: int, 
        project_id: int) -> bool:
    user_project = db_session.query(UserProject).filter(
        UserProject.user_id == user_id,
        UserProject.project_id == project_id
    ).first()
    if user_project and user_project.role in [
        'owner', 
        'participant'
        ]:
        return True
    return False

def is_user_admin_in_project(
        db_session: Session, 
        user_id: int, 
        project_id: int) -> bool:
    user_project = db_session.query(UserProject).filter(
        UserProject.user_id == user_id,
        UserProject.project_id == project_id
    ).first()
    if user_project and user_project.role == 'admin':
        return True
    return False

def update_project(
        db_session: Session, 
        project_id: int, 
        name: str, 
        description: str, 
        owner_id: int, 
        updated_at: datetime,
        current_user: User = Depends(get_user)
        ):
    updated_at = updated_at or datetime.now(timezone.utc)
    db_project = db_session.query(Project).filter(
        Project.id == project_id
        ).first()
    
    if db_project:
        db_project.name = name
        db_project.description = description
        db_project.owner_id = owner_id
        db_project.modified_by = current_user.username
        db_project.updated_at = updated_at

        db_session.commit()
        db_session.refresh(db_project)
        return db_project
    return None

def delete_project(db_session: Session, project_id: int, user_id: int):
    db_project = db_session.query(Project).filter(
        Project.id == project_id
        ).first()
    if db_project:
        if is_user_admin_in_project(db_session, user_id, project_id):
            db_session.delete(db_project)
            db_session.commit()
            return f"Project {project_id} has been deleted."
        else:
            raise ValueError(f"User {user_id} is not admin!")
    return None

def grant_acces(
        db_session: Session, 
        project_id: int, 
        owner_id: int, 
        invited_user_id: int):
    db_project = db_session.query(Project).filter(
        Project.id == project_id
        ).first()
    if not db_project:
        raise ValueError(
            f"Project {project_id} does not exist."
            )
    if db_project.owner_id != owner_id:
        raise PermissionError(
            f"User {owner_id} is not the owner of project {project_id}."
            )
    user_project_rel = db_session.query(UserProject).filter(
        UserProject.user_id == invited_user_id,
        UserProject.project_id == project_id
    ).first()
    if user_project_rel:
        raise ValueError(
            f"User {invited_user_id} already has access to project {project_id}."
            )
    
    db_user_project = UserProject(
        user_id=invited_user_id, project_id=project_id, role='participant'
        )
    db_session.add(db_user_project)
    db_session.commit()
    db_session.refresh(db_user_project)
    return db_user_project
