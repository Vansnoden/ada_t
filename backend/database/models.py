from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from .database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    fullname = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)



class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    create_uid = Column(Integer, ForeignKey("users.id"), nullable=False)
    create_date = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    create_date = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    