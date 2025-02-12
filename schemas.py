from typing import Optional

from pydantic import BaseModel
from datetime import datetime

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
    name: str
    description: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class DocumentFinal(BaseModel):
    name: str
    type: str
    path: str
    project_id: int

    model_config = {"from_attributes": True}