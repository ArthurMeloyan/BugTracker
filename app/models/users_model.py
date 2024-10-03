from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class Role(str, enum.Enum):
    MANAGER = 'Manager'
    TEAM_LEADER = 'Team Leader'
    DEVELOPER = 'Developer'
    TEST_ENGINEER = 'Test Engineer'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)

    task_created = relationship(
        "Task",
        foreign_keys="Task.creator_id",
        back_populates="creator"
    )
    task_assigned = relationship(
        "Task",
        foreign_keys="Task.assignee_id",
        back_populates="assignee"
    )

