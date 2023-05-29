from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from server import crud, models, schemas
from server.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    if users is None:
        raise HTTPException(status_code=404, detail="User not found from the list")
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/users/{user_id}/todos/", response_model=schemas.TodoSchema)
def post_todo_for_user(user_id: int, todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    get_user = crud.get_user_by_id(db, user_id)
    if get_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_todo(db=db, todo=todo, user_id=user_id)


@router.get("/todos/", response_model=List[schemas.TodoSchema])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos


@router.get("/todos/{user_id}", response_model=List[schemas.TodoSchema])
def read_todos_by_user_id(user_id: int, db: Session = Depends(get_db)):
    todos = crud.get_todos_by_userid(db, user_id)
    return todos


@router.get("/todos/{todos_id}", response_model=schemas.TodoSchema)
def read_todos_by_id(todos_id: int, db: Session = Depends(get_db)):
    todos = crud.get_todos_by_id(db, todos_id)
    if todos is None:
        raise HTTPException(status_code=404, detail="Todo is not found")
    return todos
