import asyncio
from datetime import datetime, timedelta
from aiogram import Bot

from bot.services.reminder_service import ReminderService
from bot.keyboards.reminder_actions import reminder_actions


async def reminder_worker(bot: Bot):
    while True:
        tasks = await ReminderService.get_tasks_for_reminder()
        now = datetime.utcnow()

        for task in tasks:
            delta = task.deadline - now

            # ⏰ за 1 час
            if task.remind_1h and timedelta(minutes=59) < delta < timedelta(minutes=61):
                await bot.send_message(
                    task.user_id,
                    f"⏰ Через 1 час:\n{task.title}",
                    reply_markup=reminder_actions(task.id)
                )
                task.remind_1h = False

            # 📅 за 1 день
            if task.remind_1d and timedelta(hours=23) < delta < timedelta(hours=25):
                await bot.send_message(
                    task.user_id,
                    f"📅 Завтра:\n{task.title}",
                    reply_markup=reminder_actions(task.id)
                )
                task.remind_1d = False

        await asyncio.sleep(60)
