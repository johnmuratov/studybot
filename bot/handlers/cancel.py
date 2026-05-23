from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.keyboards.main_menu import main_menu_kb

router = Router()


@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    """
    Универсальный выход из любого режима:
    - AI-чат
    - FSM добавления задачи
    - любые другие состояния
    """
    await state.clear()

    await message.answer(
        "❌ Действие отменено.\nТы в главном меню 👇",
        reply_markup=main_menu_kb(),
    )
