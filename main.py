from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from typing import List

app = FastAPI()

db = []
project_id = 1

class Project(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int

@app.post("/projects", response_model=Project)
def create_projects(project: Project):
    global project_id
    new_project = Project(id=project_id, name=project.name, description=project.description, owner_id=project.owner_id)
    db.append(new_project)
    project_id += 1
    return new_project

@app.get("/projects", response_model=List[Project])
def get_projects():
    return db

@app.get("/projects/{project_id}/info", response_model=Project)
def get_project_info(project_id: int):
    for pr in db:
        if pr.id == project_id:
            return pr
    raise HTTPException(status_code=404, detail='Project not found')

@app.put("/projects/{project_id}/info", response_model=Project)
def update_project(project_id: int, project: Project):
    for pr in db:
        if pr.id == project_id:
            pr.name = project.name
            pr.description = project.description
            pr.owner_id = project.owner_id
            return pr
    raise HTTPException(status_code=404, detail='Project not found')
        
@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    global db
    project_to_delete = None

    for pr in db:
        if pr.id == project_id:
            project_to_delete = pr
            break

    if project_to_delete is None:
        return f'error: project id {project_id} not found.'
    
    db.remove(project_to_delete)
    return f'Project id {project_id} has been deleted.'