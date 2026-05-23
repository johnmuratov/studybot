from sqlalchemy import select, update, delete, or_
from datetime import datetime, timedelta

from bot.db.sessions import get_session
from bot.db.models import Task


class TaskService:

    # 📋 Активные задачи
    @staticmethod
    async def get_active_tasks(user_id: int):
        async with get_session() as session:
            result = await session.execute(
                select(Task)
                .where(Task.user_id == user_id)
                .where(Task.completed == False)
                .where(Task.deleted == False)
                .order_by(Task.deadline.asc())
            )
            return result.scalars().all()

    # ➕ Создать задачу
    @staticmethod
    async def create_task(user_id: int, title: str, deadline):
        async with get_session() as session:
            session.add(
                Task(
                    user_id=user_id,
                    title=title,
                    deadline=deadline,
                )
            )
            await session.commit()

    # ✅ Выполнить
    @staticmethod
    async def mark_completed(task_id: int):
        async with get_session() as session:
            await session.execute(
                update(Task)
                .where(Task.id == task_id)
                .values(
                    completed=True,
                    completed_at=datetime.utcnow(),
                )
            )
            await session.commit()

    # 🗑 Удалить (мягко)
    @staticmethod
    async def delete_task(task_id: int):
        async with get_session() as session:
            await session.execute(
                update(Task)
                .where(Task.id == task_id)
                .values(
                    deleted=True,
                    deleted_at=datetime.utcnow(),
                )
            )
            await session.commit()

    # 📜 ИСТОРИЯ — ЕДИНЫЙ СПИСОК
    @staticmethod
    async def get_task_history(user_id: int):
        async with get_session() as session:
            result = await session.execute(
                select(Task)
                .where(Task.user_id == user_id)
                .where(
                    (Task.completed == True) |
                    (Task.deleted == True)
                )
                .order_by(
                    (Task.completed_at.desc().nullslast()),
                    (Task.deleted_at.desc().nullslast())
                )
            )
            return result.scalars().all()

    # 🔄 Возврат задачи
    @staticmethod
    async def restore_task(task_id: int):
        async with get_session() as session:
            await session.execute(
                update(Task)
                .where(Task.id == task_id)
                .values(
                    completed=False,
                    deleted=False,
                    completed_at=None,
                    deleted_at=None,
                )
            )
            await session.commit()

    # Очистка истории старше 30 дней
    @staticmethod
    async def cleanup_history(days: int = 30) -> int:
        """
        Удаляет задачи из истории старше N дней
        Возвращает количество удалённых задач
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        async with get_session() as session:
            result = await session.execute(
                delete(Task).where(
                    or_(
                        (Task.completed == True) & (Task.completed_at < cutoff_date),
                        (Task.deleted == True) & (Task.deleted_at < cutoff_date),
                    )
                )
            )
            await session.commit()
            return result.rowcount
        
    # Напоминания
    @staticmethod
    async def snooze_task(task_id: int, minutes: int):
        async with get_session() as session:
            await session.execute(
            update(Task)
            .where(Task.id == task_id)
            .values(postponed_until=datetime.utcnow() + timedelta(minutes=minutes))
        )
        await session.commit()    