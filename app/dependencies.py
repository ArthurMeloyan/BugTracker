from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.database import get_db
from app.schemas.users_schema import TokenData
from app.utils import SECRET_KEY, ALGORITHM
from app.crud import crud_users
from app.models.users_model import Role
from app.models.tasks_model import Status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Декодируем токен JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("sub")  # Извлекаем логин из токена (sub - subject)
        if login is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(login=login)  # Создаем объект TokenData с логином
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Получаем пользователя по логину из базы данных
    user = crud_users.get_user_by_username(db, username=token_data.login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def check_assignment_restrictions(task_status: Status, assignee_role: Role) -> bool:
    if assignee_role == Role.MANAGER:
        return False
    elif assignee_role == Role.TEST_ENGINEER and task_status in [Status.IN_PROGRESS, Status.CODE_REVIEW, Status.DEV_TEST]:
        return False
    elif assignee_role == Role.DEVELOPER and task_status == Status.TESTING:
        return False
    return True