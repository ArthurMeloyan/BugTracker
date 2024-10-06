from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import crud_users
from app.schemas.users_schema import UserCreate, UserUpdate, UserDelete, UserResponse
from app.database import get_db


router = APIRouter()


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = crud_users.get_user_by_login(db, user.login)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with login already exists")
    return crud_users.create_user(db, user)


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_users.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud_users.get_users(db, skip, limit)
    return users


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud_users.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = crud_users.update_user(db=db, user_id=user_id, user=user)
    if updated_user is None:
        raise HTTPException(status_code=400, detail="Error occurred while updating user")
    return updated_user


@router.delete("/{user_id}", response_model=UserDelete)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    succeeded = crud_users.delete_user(db=db, user_id=user_id)
    if not succeeded:
        raise HTTPException(status_code=404, detail="User not found")
    return UserDelete(message=f'User with id {user_id} deleted successfully')



