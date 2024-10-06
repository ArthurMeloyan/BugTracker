from sqlalchemy.orm import Session
from app.models.tasks_model import Task
from app.schemas.tasks_schema import TaskCreate, TaskUpdate, Status

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: TaskCreate):
    db_task = Task(
        type = task.type,
        priority = task.priority,
        status = task.status,
        title = task.title,
        description = task.description,
        assignee_id=task.assignee_id,
        creator_id=task.creator_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task: TaskUpdate):
    db_task = db.query(Task).filter(Task.id == task.id).first()
    if not db_task:
        return False
    if task.type:
        db_task.type = task.type
    if task.priority:
        db_task.priority = task.priority
    if task.status:
        db_task.status = task.status
    if task.title:
        db_task.title = task.title
    if task.description:
        db_task.description = task.description
    if task.assignee_id:
        db_task.assignee_id = task.assignee_id
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True


def update_task_status(db: Session, task_id: int, status: Status):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return None
    if status in [Status.TO_DO, Status.WONTFIX]:
        task.status = status
    elif task.status == Status.TO_DO and status == Status.IN_PROGRESS:
        task.status = status
    elif task.status == Status.IN_PROGRESS and status == Status.CODE_REVIEW:
        task.status = status
    elif task.status == Status.CODE_REVIEW and status == Status.DEV_TEST:
        task.status = status
    elif task.status == Status.DEV_TEST and status == Status.TESTING:
        task.status = status
    elif task.status == Status.TESTING and status == Status.DONE:
        task.status = status
    else:
        return None

    db.commit()
    db.refresh(task)
    return task
