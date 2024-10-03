from fastapi import FastAPI
#from routers import users_router, tasks_router, auth_router
from database import engine, Base
#from models import users_model, tasks_model


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bug Tracker API",
    description="API для управления задачами и пользователями",
    version="1.0.0")

#app.include_router(users_router.router, prefix="/users", tags=["Пользователи"])
#app.include_router(tasks_router.router, prefix="/tasks", tags=["Задачи"])
#app.include_router(auth_router.router, prefix="/auth", tags=["Авторизация"])

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в Bug Tracker API"}