from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.services.task_service import TaskService

router = Router()


@router.callback_query(F.data.startswith("task_done:"))
async def mark_done(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[1])
    await TaskService.mark_completed(task_id)
    await callback.answer("Выполнено ✅")
    await callback.message.delete()


@router.callback_query(F.data.startswith("task_delete:"))
async def delete_task(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[1])
    await TaskService.delete_task(task_id)
    await callback.answer("Удалено 🗑")
    await callback.message.delete()


@router.callback_query(F.data.startswith("task_restore:"))
async def restore_task(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[1])

    await TaskService.restore_task(task_id)

    await callback.answer("Задача возвращена 🔄")
    await callback.message.edit_text("🔄 Задача возвращена в активные")

@router.callback_query(F.data.startswith("snooze:"))
async def snooze(callback: CallbackQuery):
    _, task_id, minutes = callback.data.split(":")
    await TaskService.snooze_task(int(task_id), int(minutes))

    await callback.answer("⏳ Напоминание отложено")
    await callback.message.edit_text("⏳ Напоминание отложено")
