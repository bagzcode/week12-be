from typing import Optional, List, Union
from pydantic import BaseModel


class TodoBase(BaseModel):
    title: str = None
    description: str = None


class TodoCreate(TodoBase):
    pass


class TodoSchema(TodoBase):
    id: int
    created: str = None
    completed: bool = False
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    todos: List[TodoSchema] = []

    class Config:
        orm_mode = True
