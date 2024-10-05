from pydantic import BaseModel, Field
from typing import Optional
from app.models.users_model import Role


class UserCreate(BaseModel):
    username: str
    login: str
    password: str
    role: Role


class UserUpdate(BaseModel):
    username: Optional[str] = None
    login: Optional[str] = None
    password: Optional[str] = None
    role: Optional[Role] = None


class UserDelete(BaseModel):
    message: str


class UserResponse(BaseModel):
    id: int


    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokeData(BaseModel):
    login: Optional[str] = None

