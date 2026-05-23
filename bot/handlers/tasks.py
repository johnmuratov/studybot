from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.states.add_task import AddTaskStates
from bot.services.task_service import TaskService

from bot.keyboards.main_menu import main_menu_kb
from bot.keyboards.task_actions import task_actions
from bot.keyboards.task_restore import task_restore_keyboard

router = Router()


# ─────────────────────────────
# ➕ Добавление задачи
# ─────────────────────────────

@router.message(Command("add"))
@router.message(F.text == "➕ Добавить задачу")
async def add_task_start(message: Message, state: FSMContext):
    # Явно выходим из любого другого режима (например AI)
    await state.clear()

    await message.answer("Введите название задачи ✍️")
    await state.set_state(AddTaskStates.waiting_for_title)


@router.message(AddTaskStates.waiting_for_title, F.text)
async def add_task_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await message.answer("Введите дедлайн:\nDD.MM.YYYY HH:MM")
    await state.set_state(AddTaskStates.waiting_for_deadline)


@router.message(AddTaskStates.waiting_for_deadline, F.text)
async def add_task_deadline(message: Message, state: FSMContext):
    try:
        deadline = datetime.strptime(message.text.strip(), "%d.%m.%Y %H:%M")
    except ValueError:
        await message.answer("❌ Неверный формат. Попробуй ещё раз.")
        return

    data = await state.get_data()

    await TaskService.create_task(
        user_id=message.from_user.id,
        title=data["title"],
        deadline=deadline,
    )

    await state.clear()
    await message.answer(
        "✅ Задача добавлена",
        reply_markup=main_menu_kb(),
    )


# ─────────────────────────────
# 📋 Активные задачи
# ─────────────────────────────

@router.message(F.text == "📋 Мои задачи")
async def my_tasks(message: Message, state: FSMContext):
    await state.clear()

    tasks = await TaskService.get_active_tasks(message.from_user.id)

    if not tasks:
        await message.answer("Задач нет 🎉", reply_markup=main_menu_kb())
        return

    for task in tasks:
        await message.answer(
            f"{task.title}\n⏰ {task.deadline.strftime('%d.%m.%Y %H:%M')}",
            reply_markup=task_actions(task.id),
        )

    # Возвращаем меню после списка
    await message.answer("Выбери действие 👇", reply_markup=main_menu_kb())


# ─────────────────────────────
# 📜 История задач
# ─────────────────────────────

@router.message(F.text == "📜 История задач")
async def task_history(message: Message, state: FSMContext):
    await state.clear()

    tasks = await TaskService.get_task_history(message.from_user.id)

    if not tasks:
        await message.answer("История пуста 📭", reply_markup=main_menu_kb())
        return

    for task in tasks:
        if task.completed:
            icon = "✅"
        elif task.deleted:
            icon = "🗑"
        else:
            icon = "❓"

        await message.answer(
            f"{icon} {task.title}",
            reply_markup=task_restore_keyboard(task.id),
        )

    await message.answer("Выбери действие 👇", reply_markup=main_menu_kb())
