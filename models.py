from sqlalchemy import Column, Integer, String, Boolean, Text, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String(255), nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String, index=True)

    projects = relationship('Project', back_populates='owner')
    user_projects = relationship('UserProject', back_populates='user')

class Project(Base):
    __tablename__ = 'projects'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='projects')
    documents = relationship('Document', back_populates='project')
    user_projects = relationship('UserProject', back_populates='project')

class UserProject(Base):
    __tablename__ = 'user_projects'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    role = Column(String)

    user = relationship('User', back_populates='user_projects')
    project = relationship('Project', back_populates='user_projects')

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    type = Column(String)
    path = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'))

    project = relationship('Project', back_populates='documents')

class Invitations(Base):
    __tablename__ = 'invitations'

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'), index=True,)
    user_token = Column(Boolean, default=False)

    project = relationship('Project', back_populates='invitations')
