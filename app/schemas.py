from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserLogin(BaseModel):
    id: int
    name: str
    access_token: str
    token_type: str = "bearer"


class User(BaseModel):
    email: EmailStr
    name: str
    id: int

    class Config:
        orm_mode = True


class PostComplain(BaseModel):
    title: str
    summary: str
    complainRating: str


class Complain(PostComplain):
    id: int
    timeLogged: datetime
    resolved: Optional[str] = None
    owner: User

    class Config:
        orm_mode = True


class UserComplain(BaseModel):
    title: str

    class Config:
        orm_mode = True


class AllComplain(BaseModel):
    title: str
    owner: User

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokData(BaseModel):
    id: Optional[str] = None


class Resolved(BaseModel):
    id: int
