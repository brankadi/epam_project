from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import get_current_user, create_access_token
from db import get_db
import projects
import users
import documents
from models import User
from schemas import UserCreate, UserFinal, ProjectFinal, DocumentFinal

app = FastAPI()
    
    
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/auth", response_model=UserFinal)
def register_user(
    user: UserCreate, 
    db_session: Session = Depends(get_db)
    ):
    db_user = db_session.query(User).filter(
        User.username == user.username
        ).first()
    if db_user:
        raise HTTPException(
            status_code=400, 
            detail="Username already registered!"
            )
    db_user = users.create_user(
        db=db_session, 
        user=user
        )
    return db_user

@app.post("/login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db_session: Session = Depends(get_db)
    ):
    db_user = users.get_user_by_username(
        db_session, 
        form_data.username
        )
    if not db_user or not users.verify_password(
        form_data.password, db_user.hashed_password
        ):
        raise HTTPException(
            status_code=401, 
            detail="Invalid credentials"
            )
    
    access_token = create_access_token(
        data={
            "sub": db_user.id, 
            "username": db_user.username
            })
    return {
        "access_token": access_token, 
        "token_type": "bearer"
        }

@app.post("/projects", response_model=ProjectFinal)
def create_project(
    project: ProjectFinal,
    db_session: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
    ):
    db_project = projects.create_project(
        db_session, project.name, 
        project.description, 
        project.owner_id, 
        modified_by=current_user.username
        )
    if db_project:
        return ProjectFinal.model_validate(db_project)
    raise HTTPException(
        status_code=400, 
        detail="Project creation failed."
        )

@app.get("/projects", response_model=List[ProjectFinal])
def get_projects(db_session: Session = Depends(get_db)):
    return projects.get_projects(db_session)

@app.get("/projects/{project_id}/info", response_model=ProjectFinal)
def get_project_info(
    project_id: int, 
    db_session: Session = Depends(get_db)
    ):
    db_project = projects.get_project(db_session, project_id)
    if db_project:
        return db_project
    raise HTTPException(
        status_code=404, 
        detail=f"Project {project_id} not found."
        )

@app.put("/projects/{project_id}/info", response_model=ProjectFinal)
def update_project(
    project_id: int, 
    project: ProjectFinal, 
    db_session: Session = Depends(get_db)
    ):
    db_project = projects.update_project(
        db_session, project_id, 
        project.name, 
        project.description, 
        project.owner_id
        )
    if db_project:
        return db_project
    raise HTTPException(
        status_code=404, 
        detail=f"Project {project_id} not found."
        )

@app.delete("/projects/{project_id}")
def delete_project(
    project_id: int, 
    db_session: Session = Depends(get_db),
    current_user: UserFinal = Depends(get_current_user)
    ):
    
    if not projects.is_user_admin_in_project(
        db_session, 
        current_user.id, 
        project_id
        ):
        raise HTTPException(
            status_code=403, 
            detail="You are not authorized to delete this project"
            )
    
    db_project = projects.delete_project(db_session, project_id)
    if db_project:
        return f"Project {project_id} deleted"
    raise HTTPException(
        status_code=404, 
        detail="Project not found"
        )

@app.post("/documents/", response_model=DocumentFinal)
def create_document(
    document: DocumentFinal,
    db_session: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
    ):
    db_document = documents.create_document(
        db_session, 
        document.name, 
        document.type, 
        document.path, 
        modified_by=current_user.username
        )
    if db_document:
        return DocumentFinal.model_validate(db_document)
    raise HTTPException(
        status_code=400, 
        detail="Document creation failed."
        )

@app.get("/projects/{project_id}/documents", response_model=List[DocumentFinal])
def get_documents_by_project(
    project_id: int, 
    db_session: Session = Depends(get_db)
    ):
    db_documents = documents.get_project_documents(
        db_session, 
        project_id=project_id
        )
    return db_documents

@app.get("/documents/{document_id}", response_model=DocumentFinal)
def get_document(
    document_id: int, 
    db_session: Session = Depends(get_db)):
    db_document = documents.get_document(
        db_session, 
        document_id=document_id
        )
    if db_document is None:
        raise HTTPException(
            status_code=404, 
            detail="Document not found."
            )
    return db_document

@app.put("/documents/{document_id}", response_model=DocumentFinal)
def update_document(
    document_id: int, 
    document: DocumentFinal, 
    db_session: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
    ):
    db_document = documents.update_document(
        db_session, 
        document_id, 
        document.name, 
        document.type, 
        document.path,
        current_user["id"]
    )
    if db_document:
        return db_document
    raise HTTPException(
        status_code=404, 
        detail=f"Document {document_id} not found."
        )