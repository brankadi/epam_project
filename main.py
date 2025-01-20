from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db import SessionLocal
from typing import List
import crud
import auth
import db
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    email: str

    class Config:
        orm_mode = True
        
class User(BaseModel):
    id: int
    username: str
    name: str
    email: str

    class Config:
        orm_mode = True
        
@app.post("/", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(db.get_db)):
    db_user = crud.create_user(db=db, username=user.username, password=user.password, name=user.name, email=user.email)
    return db_user

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = crud.get_user_by_username(auth.db, form_data.username)
    if not db_user or not crud.verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = auth.create_access_token(data={"sub": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}

class Project(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int

@app.post("/projects", response_model=Project)
def create_project(project: Project, db: Session = Depends(db.get_db)):
    db_project = crud.create_project(db, project.name, project.description, project.owner_id)
    if db_project:
        return db_project
    raise HTTPException(status_code=400, detail="Project creation failed")

@app.get("/projects", response_model=List[Project])
def get_projects(db: Session = Depends(db.get_db)):
    return crud.get_projects(db)

@app.get("/projects/{project_id}/info", response_model=Project)
def get_project_info(project_id: int, db: Session = Depends(db.get_db)):
    db_project = crud.get_project(db, project_id)
    if db_project:
        return db_project
    raise HTTPException(status_code=404, detail="Project not found")

@app.put("/projects/{project_id}/info", response_model=Project)
def update_project(project_id: int, project: Project, db: Session = Depends(db.get_db)):
    db_project = crud.update_project(db, project_id, project.name, project.description, project.owner_id)
    if db_project:
        return db_project
    raise HTTPException(status_code=404, detail="Project not found")

@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(db.get_db)):
    current_user = auth.get_current_user()
    
    if not crud.is_user_admin_in_project(db, current_user.id, project_id):
        raise HTTPException(status_code=403, detail="You are not authorized to delete this project")
    
    db_project = crud.delete_project(db, project_id)
    if db_project:
        return {"message": f"Project {project_id} deleted"}
    raise HTTPException(status_code=404, detail="Project not found")
