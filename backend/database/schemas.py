from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    fullname: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True



class ProjectBase(BaseModel):
    name: str
    create_date: datetime
    create_uid: int

class Project(ProjectBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True



class QuestionBase(BaseModel):
    name: str
    project_id: int
    create_date: datetime

class Question(QuestionBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True