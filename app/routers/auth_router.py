from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.crud import crud_users
from app.schemas.users_schema import Token, UserCreate
from app.database import get_db
from app.utils import verify_password, create_access_token, hash_password



router = APIRouter()


@router.post('/register', response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = crud_users.get_user_by_username(db, username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this login already exists")

    user.password = hash_password(user.password)
    db_user = crud_users.create_user(db, user)
    access_token = create_access_token(data={'sub': db_user.username})

    print(f"Registered user: {user.username}, Password: {user.password}")
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/login', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_users.get_user_by_username(db, username=form_data.username)

    if not user:
        print(f"Login failed: {form_data.username} not found.")
        raise HTTPException(status_code=400, detail="Incorrect username")

    print(f"User found: {user.username}, Hashed Password: {user.password}")

    if not verify_password(form_data.password, user.password):
        print(f"Login failed: Incorrect password for {form_data.username}. Password: {form_data.password}")
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token = create_access_token(data={'sub': user.username})

    return {"access_token": access_token, "token_type": "bearer"}
