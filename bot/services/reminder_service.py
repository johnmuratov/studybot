from datetime import datetime, timedelta
from sqlalchemy import select
from bot.db.sessions import get_session
from bot.db.models import Task


class ReminderService:

    @staticmethod
    async def get_tasks_for_reminder():
        now = datetime.utcnow()

        async with get_session() as session:
            result = await session.execute(
                select(Task)
                .where(Task.completed == False)
                .where(Task.deleted == False)
                .where(
                    (Task.postponed_until == None) |
                    (Task.postponed_until <= now)
                )
            )
            return result.scalars().all()
