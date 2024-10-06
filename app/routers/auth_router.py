from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.crud import crud_users
from app.schemas.users_schema import Token, UserCreate
from app.database import get_db
from app.utils import verify_password, create_access_token, hash_password


router = APIRouter()


@router.post('/register', response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = crud_users.get_user_by_login(db, login=user.login)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this login already exists")
    user.password = hash_password(user.password)
    db_user = crud_users.create_user(db, user)
    access_token = create_access_token(data={'sub': db_user.login})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/login', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_users.get_user_by_login(db, login=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={'sub': user.login})
    return {"access_token": access_token, "token_type": "bearer"}
