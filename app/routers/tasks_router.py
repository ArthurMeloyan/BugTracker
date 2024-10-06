from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import crud_tasks
from app.dependencies import get_current_user
from app.models.users_model import User
from app.schemas.tasks_schema import TaskCreate, TaskUpdate, TaskDelete, TaskResponse, Status
from app.schemas.users_schema import Role
from app.database import get_db


router = APIRouter()


@router.post('/', response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return crud_tasks.create_task(db=db, task=task)


@router.get('/{task_id}', response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud_tasks.get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.get('/', response_model=List[TaskResponse])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = crud_tasks.get_tasks(db, skip, limit)
    return tasks


@router.put('/{task_id}', response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud_tasks.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    updated_task = crud_tasks.update_task(db, task)
    if updated_task is None:
        raise HTTPException(status_code=400, detail="Error occurred while updating task")
    return updated_task


@router.delete('/{task_id}', response_model=TaskDelete)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    succeeded = crud_tasks.delete_task(db=db, task_id=task_id)
    if not succeeded:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskDelete(message=f'Task with {task_id} successfully deleted')


@router.put('/{task_id}/status', response_model=TaskResponse)
def update_task_status(task_id: int, status_update: Status, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = crud_tasks.get_task(db, task_id)
    if current_user.role not in [Role.MANAGER, task.assignee_id]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    updated_task = crud_tasks.update_task_status(db, task, status_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task