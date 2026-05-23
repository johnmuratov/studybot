from datetime import datetime, timedelta
from sqlalchemy import select
from bot.db.sessions import get_session
from bot.db.models import Task


class StatsService:

    #Недельный отчёт
    @staticmethod
    async def weekly_report(user_id: int):
        week_ago = datetime.utcnow() - timedelta(days=7)

        async with get_session() as session:
            result = await session.execute(
                select(Task)
                .where(Task.user_id == user_id)
                .where(Task.deadline >= week_ago)
            )
            tasks = result.scalars().all()

        completed = sum(1 for t in tasks if t.completed)
        deleted = sum(1 for t in tasks if t.deleted)
        active = sum(1 for t in tasks if not t.completed and not t.deleted)

        return completed, deleted, active
