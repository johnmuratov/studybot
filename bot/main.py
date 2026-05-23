import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import BOT_TOKEN
from bot.db.base import Base
from bot.db.sessions import engine

from bot.handlers import (
    start,
    ai_chat,          # 🔥 FSM AI ЧАТ
    tasks,
    task_callbacks,
    cancel,
    reports,
)

from bot.scheduler.cleanup import history_cleanup_loop
from bot.scheduler.reminder_worker import reminder_worker


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # ─────────────────────────────
    # ВАЖЕН ПОРЯДОК ROUTER-ОВ
    # ─────────────────────────────

    dp.include_router(start.router)

    dp.include_router(ai_chat.router)     # 🔥 AI ЧАТ — ВЫШЕ ВСЕХ

    dp.include_router(tasks.router)
    dp.include_router(task_callbacks.router)
    dp.include_router(reports.router)
    dp.include_router(cancel.router)

    # ─────────────────────────────

    await init_db()

    # 🧹 автоочистка истории
    asyncio.create_task(history_cleanup_loop())

    # ⏰ напоминания
    asyncio.create_task(reminder_worker(bot))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
