import enum
from typing import Optional

from sqlalchemy import Integer, String, Boolean, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String, index=True)

    projects: Mapped[list["Project"]] = relationship('Project', back_populates='owner', foreign_keys='Project.owner_id')
    modified_documents: Mapped[list["Document"]] = relationship('Document', back_populates="modified_by_user", foreign_keys='Document.modified_by')
    user_projects: Mapped[list["UserProject"]] = relationship("UserProject", back_populates="user")

class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    owner: Mapped["User"] = relationship('User', back_populates='projects', foreign_keys=[owner_id])
    documents: Mapped[list["Document"]] = relationship ('Document', back_populates='project')
    user_projects: Mapped[list["UserProject"]] = relationship("UserProject", back_populates="project")
    invitations: Mapped[list["Invitation"]] = relationship('Invitation', back_populates='project')

class Role(enum.Enum):
    owner = "owner"
    participant = "participant"

class UserProject(Base):
    __tablename__ = 'user_projects'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('projects.id'), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False, default=Role.participant)

    user: Mapped["User"] = relationship("User", back_populates="user_projects")
    project: Mapped["Project"] = relationship("Project", back_populates="user_projects")

class Document(Base):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    type: Mapped[str] = mapped_column(String)
    path: Mapped[str] = mapped_column(String, nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('projects.id'), nullable=False)
    modified_by: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    project: Mapped["Project"] = relationship('Project', back_populates='documents')
    modified_by_user: Mapped["User"] = relationship("User", back_populates="modified_documents", foreign_keys=[modified_by])

class Invitation(Base):
    __tablename__ = 'invitations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('projects.id'), index=True, nullable=False)
    user_token: Mapped[bool] = mapped_column(Boolean, default=False)
    token: Mapped[str]  = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    invited_user_email: Mapped[str]  = mapped_column(String, nullable=False)

    project: Mapped["Project"] = relationship('Project', back_populates='invitations')
    
