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
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    fullname = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)



class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    create_uid = Column(Integer, ForeignKey("users.id"), nullable=False)
    create_date = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    documents_location = Column(String, nullable=False, default='.')
    grammars_location = Column(String, nullable=False, default='.')
    extraction_results_location = Column(String, nullable=False, default='.')



class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)
    answer_format = Column(String, nullable=False) # this will basically be the json string of the answer format
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    create_date = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    anwser_grammar = Column(String, default=".", nullable=True)
    