from fastapi import FastAPI
from app.routers import users_router, tasks_router, auth_router
from app.database import Base, engine



app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users_router.router, prefix="/users", tags=["Пользователи"])
app.include_router(tasks_router.router, prefix="/tasks", tags=["Задачи"])
app.include_router(auth_router.router, prefix="/auth", tags=["Авторизация"])

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в Bug Tracker API"}