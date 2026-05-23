from sqlalchemy import (
    Integer, String, DateTime, Boolean, Column
)
from datetime import datetime
from bot.db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)

    title = Column(String, nullable=False)
    deadline = Column(DateTime, nullable=False)

    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)

    deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)

    # 🔔 напоминания
    remind_1h = Column(Boolean, default=True)
    remind_1d = Column(Boolean, default=True)

    postponed_until = Column(DateTime, nullable=True)