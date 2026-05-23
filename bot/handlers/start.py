from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.keyboards.main_menu import main_menu_kb

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    # Явно сбрасываем любое состояние (AI, добавление задач и т.д.)
    await state.clear()

    await message.answer(
        "Привет! Я учебный бот 🤖\nВыбери действие в меню 👇",
        reply_markup=main_menu_kb(),
    )


@router.message(Command("menu"))
async def menu_handler(message: Message, state: FSMContext):
    # /menu — всегда возврат в главное меню
    await state.clear()

    await message.answer(
        "Меню 👇",
        reply_markup=main_menu_kb(),
    )
