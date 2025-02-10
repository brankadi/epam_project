from typing import Optional

from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    surname: Optional[str] = None
    email: str

    model_config = {"from_attributes": True}

class UserFinal(BaseModel):
    id: int
    username: str
    name: str
    surname: Optional[str] = None
    email: str

    model_config = {"from_attributes": True}

class ProjectFinal(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int

    model_config = {"from_attributes": True}

class DocumentFinal(BaseModel):
    id: int
    name: str
    type: str
    path: str
    project_id: int
    modified_by: int

    model_config = {"from_attributes": True}