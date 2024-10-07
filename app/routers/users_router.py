from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud import crud_users
from app.dependencies import get_current_user
from app.models.users_model import User, Role
from app.schemas.users_schema import UserUpdate, UserDelete, UserResponse
from app.database import get_db


router = APIRouter()


def manager_only(current_user: User = Depends(get_current_user)):
    if current_user.role != Role.MANAGER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")


@router.put('{user_id}/update_login_role', dependencies=[Depends(manager_only)])
def update_user(user_id: int, updated: UserUpdate, db: Session = Depends(get_db)):
    user = crud_users.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    updated = crud_users.update_user(db, user_id=user_id, new_login=updated.login, new_role=updated.role)
    return {"message": "Login and role successfully updated"}

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


@router.delete("/{user_id}", response_model=UserDelete, dependencies=[Depends(manager_only)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    succeeded = crud_users.delete_user(db=db, user_id=user_id)
    if not succeeded:
        raise HTTPException(status_code=404, detail="User not found")
    return UserDelete(message=f'User with id {user_id} deleted successfully')



