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


class FileBase(BaseModel):
    file_path: str
    

class Project(ProjectBase):
    id: int
    is_active: bool
    is_running: bool
    create_uid: int
    create_date: datetime
    documents_location: str
    grammars_location: str
    extraction_results_location: str

    class Config:
        from_attributes = True



class QuestionBase(BaseModel):
    label: str
    answer_format: str
    project_id: int

class Question(QuestionBase):
    id: int
    is_active: bool
    create_date: datetime
    anwser_grammar: str

    class Config:
        from_attributes = True


