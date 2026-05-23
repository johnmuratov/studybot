from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.services.task_service import TaskService
from bot.keyboards.main_menu import main_menu_kb

router = Router()


@router.message(F.text == "📊 Отчёт")
async def weekly_report(message: Message, state: FSMContext):
    # ВАЖНО: выходим из любого режима (AI, FSM задач и т.д.)
    await state.clear()

    tasks = await TaskService.get_task_history(message.from_user.id)

    if not tasks:
        await message.answer(
            "Нет данных для отчёта 📭",
            reply_markup=main_menu_kb(),
        )
        return

    completed = sum(1 for t in tasks if t.completed)
    deleted = sum(1 for t in tasks if t.deleted)

    await message.answer(
        "📊 *Отчёт*\n\n"
        f"✅ Выполнено: {completed}\n"
        f"🗑 Удалено: {deleted}",
        parse_mode="Markdown",
        reply_markup=main_menu_kb(),
    )
