import json
import os
import shutil
from sqlalchemy import and_
from sqlalchemy.orm import Session

from .utilities.grammar import gbnf_from_json

from . import models, schemas
from passlib.context import CryptContext
from pathlib import Path

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 0):
    if skip and limit:
        return db.query(models.User).offset(skip).limit(limit).all()
    else:
        return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    db_user = models.User(
        username=user.username,
        email=user.email, 
        fullname=user.fullname,
        is_active=True,
        hashed_password=pwd_context.hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    res = db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return res


# projects
def get_projects(db: Session, user_id: int,  skip: int = 0, limit: int = 0):
    if skip and limit:
        return db.query(models.Project).filter(models.Project.create_uid == user_id).offset(skip).limit(limit).all()
    else:
        return db.query(models.Project).filter(models.Project.create_uid == user_id).all()
    
def get_single_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def add_project(db: Session, user_id: int, name: str):
    db_project = models.Project(
        name=name,
        create_uid=user_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    # update resources
    # the curent directory is the one of the main.py file
    documentsPath = Path(f"./database/resources/{db_project.id}/documents")
    grammarsPath = Path(f"./database/resources/{db_project.id}/grammars")
    resultsPath = Path(f"./database/resources/{db_project.id}/results")
    documentsPath.mkdir(parents=True, exist_ok=True)
    grammarsPath.mkdir(parents=True, exist_ok=True)
    resultsPath.mkdir(parents=True, exist_ok=True)
    db_project.documents_location = os.path.join(Path('.').parent.absolute(), documentsPath)
    db_project.grammars_location = os.path.join(Path('.').parent.absolute(), grammarsPath)
    db_project.extraction_results_location = os.path.join(Path('.').parent.absolute(), resultsPath)
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int):
    db_project_rec = db.query(models.Project).filter(models.Project.id == project_id).first()
    resources_path = Path(db_project_rec.documents_location).parent.absolute()
    shutil.rmtree(resources_path)
    db.query(models.Question).filter(models.Question.project_id == project_id).delete()
    res = db.query(models.Project).filter(models.Project.id == project_id).delete()
    db.commit()
    return res


def delete_single_file(file_path:str):
    if os.path.isfile(file_path):
        os.remove(file_path)


# questions
def get_project_questions(db: Session, project_id: int):
    return db.query(models.Question).filter_by(project_id=project_id,is_active=True).all()

def add_project_question(db: Session, project_id: int, label:str, answer_format:str):
    try:
        test = json.loads(answer_format)
        db_project_rec = db.query(models.Project).filter(models.Project.id == project_id).first()
        if db_project_rec:
            db_question = models.Question(
                label=label,
                answer_format=answer_format,
                project_id=project_id
            )
            db.add(db_question)
            db.commit()
            db.refresh(db_question)
            # generate grammar file
            with open(os.path.join(db_project_rec.grammars_location, f"{db_question.id}.gbnf"), "w+") as f:
                f.write(gbnf_from_json(db_question.answer_format))
                f.close()
            db_question.anwser_grammar = os.path.join(db_project_rec.grammars_location, f"{db_question.id}.gbnf")
            db.commit()
            db.refresh(db_question)
            return db_question
    except Exception as e:
        print(e)


def delete_question(db: Session, id: int):
    db_question_rec = db.query(models.Question).filter(models.Question.id == id).first()
    if db_question_rec:
        print(db_question_rec)
        print(db_question_rec.anwser_grammar)
        # shutil.rmtree(db_question_rec.anwser_grammar)
        os.chmod(db_question_rec.anwser_grammar, 0o777)
        os.remove(db_question_rec.anwser_grammar)
        res = db.query(models.Question).filter(models.Question.id == id).delete()
        db.query(models.Evaluation).filter(models.Evaluation.qid == id).delete()
        db.commit()
        return res
    return 0


def add_evaluation(db: Session, qid: int, document_location:str, evaluation:int):
    # question = db.query(models.Question).filter(models.Question.id == id).first()
    # if question:
    db_eval = models.Evaluation(
            qid=qid,
            document_location=document_location,
            evaluation=evaluation
        )
    db.add(db_eval)
    db.commit()
    db.refresh(db_eval)
    return db_eval


def get_evaluations(db: Session):
    return db.query(models.Evaluation).all()


def get_doc_evaluations(db: Session, doc_path: str):
    return db.query(models.Evaluation).filter(models.Evaluation.document_location == doc_path).all()


def delete_evaluation(db:Session, id: int):
    res = db.query(models.Evaluation).filter(models.Evaluation.id == id).delete()
    db.commit()
    return res