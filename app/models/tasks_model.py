from sqlalchemy import Column, String, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime


class Type(str, enum.Enum):
    BUG = "bug"
    TASK = "task"


class Status(str, enum.Enum):
    TO_DO = 'To Do'
    IN_PROGRESS = 'In progress'
    CODE_REVIEW = 'Code review'
    DEV_TEST = 'Dev Test'
    TESTING = 'Testing'
    DONE = 'Done'
    WONTFIX = 'Wontfix'


class Priority(str, enum.Enum):
    CRITICAL = 'Critical'
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'



class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(Type),default=Type.BUG, nullable=False)
    priority = Column(Enum(Priority), default=Priority.MEDIUM, nullable=False)
    status = Column(Enum(Status), default=Status.TO_DO, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assignee_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    creator_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    creator = relationship('User', foreign_keys=[creator_id], back_populates='task_created')
    assignee = relationship('User', foreign_keys=[assignee_id], back_populates='task_assigned')