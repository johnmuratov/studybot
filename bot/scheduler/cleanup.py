import asyncio
from bot.services.task_service import TaskService


async def history_cleanup_loop():
    while True:
        deleted = await TaskService.cleanup_history(days=30)
        print(f"[CLEANUP] Удалено задач из истории: {deleted}")

        # раз в 24 часа
        await asyncio.sleep(60 * 60 * 24)