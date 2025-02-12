from sqlalchemy.orm import Session
from fastapi import Depends

from models import Document, User
from users import get_user

def create_document(
        db_session: Session, 
        name: str, 
        type: str, 
        path: str, 
        project_id: int,
        modified_by: str = 'admin'
        ):
    db_document = Document(
        name=name, 
        type=type, 
        path=path,
        project_id=project_id,
        modified_by=modified_by
        )
    db_session.add(db_document)
    db_session.commit()
    db_session.refresh(db_document)
    return db_document

def get_document(
        db_session: Session, 
        document_id: int):
    return db_session.query(Document).filter(
        Document.id == document_id
        ).first()

def get_project_documents(
        db_session: Session, 
        project_id: int):
    return db_session.query(Document).filter(
        Document.project_id == project_id
        ).all()

def update_document(
        db_session: Session, 
        document_id: int, 
        name: str,
        type: str,
        path: str,
        project_id: int,
        current_user: User = Depends(get_user)
        ):
    db_document = db_session.query(Document).filter(
        Document.id == document_id
        ).first()
    
    if db_document:
        db_document.name = name
        db_document.type = type
        db_document.path = path
        db_document.project_id = project_id
        db_document.modified_by = current_user.username
        db_session.commit()
        db_session.refresh(db_document)
    
    return db_document
