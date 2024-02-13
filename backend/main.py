from datetime import timedelta, timezone, datetime
import os
from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from database.schemas import User
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.middleware.cors import CORSMiddleware
from database import crud, models, schemas
from database.database import SessionLocal, engine
from sqlalchemy.orm import Session


# models.Base.metadata.create_all(bind=engine)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserInDB(User):
    hashed_password: str


class TokenData(BaseModel):
    username: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str):
    user = crud.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def validate_user(user: User):
    if user.username and user.email and user.password:
        return True
    else:
        return False


# users

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    if validate_user(user):
        return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/details/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@app.get("/users/delete/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    response = crud.delete_user(db, user_id=user_id)
    if response is None:
        raise HTTPException(status_code=404, detail="User not found")
    return response


# projects
@app.get("/projects/", response_model=list[schemas.Project])
def get_user_projects(
    user:Annotated[User, Depends(get_current_active_user)], 
    db: Session = Depends(get_db)):
    if user:
        return crud.get_projects(db, user_id=user.id)
    else:
        raise HTTPException(status_code=400, detail="User not found")

@app.post("/projects/", response_model=schemas.Project)
def create_project(
    project: schemas.ProjectBase,
    user:Annotated[User, Depends(get_current_active_user)], 
    db: Session = Depends(get_db)):
    if project.name and user:
        return crud.add_project(db, name=project.name, user_id=user.id)
    else:
        raise HTTPException(status_code=400, detail="Missing required information: name, create_uid")
    
@app.get("/projects/delete/{project_id}")
def delete_project(
    project_id: int, 
    user:Annotated[User, Depends(get_current_active_user)], 
    db: Session = Depends(get_db)
    ):
    if user:
        response = crud.delete_project(db, project_id=project_id)
        if response is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return response
    else:
       raise HTTPException(status_code=403, detail="Unauthorized action") 

@app.post("/project/{project_id}/upload")
def upload_project_documents(
    project_id: int, 
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)):
    project = crud.get_single_project(project_id=project_id, db=db)
    if project:
        for file in files:
            try:
                contents = file.file.read()
                with open(os.path.join(project.documents_location, file.filename), 'wb') as f:
                    f.write(contents)
            except Exception:
                return {"message": "There was an error uploading the file(s)"}
            finally:
                file.file.close()
        return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}   
    else:
         raise HTTPException(status_code=404, detail="Project not found")


# questions
@app.get("/questions/{project_id}", response_model=list[schemas.Question])
def get_project_questions(project_id: int, db: Session = Depends(get_db)):
    return crud.get_project_questions(db, project_id=project_id)


@app.post("/questions/", response_model=schemas.Question)
def create_project_question(
    question: schemas.QuestionBase, 
    user:Annotated[User, Depends(get_current_active_user)], 
    db: Session = Depends(get_db)
    ):
    if user:
        if question.label and question.project_id and question.answer_format:
            return crud.add_project_question(
                db, 
                label=question.label, 
                answer_format=question.answer_format, 
                project_id=question.project_id
                )
        else:
            raise HTTPException(status_code=400, detail="Missing required fields")
    else:
       raise HTTPException(status_code=403, detail="Unauthorized action")

    
@app.get("/questions/delete/{question_id}")
def delete_project_question(question_id: int, db: Session = Depends(get_db)):
    response = crud.delete_question(db, id=question_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return response