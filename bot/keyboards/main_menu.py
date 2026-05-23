from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Добавить задачу")],

            [KeyboardButton(text="📋 Мои задачи")],
            [KeyboardButton(text="📜 История задач")],

            [KeyboardButton(text="📊 Отчёт")],
            [KeyboardButton(text="🤖 Спросить AI")],
        ],
        resize_keyboard=True,
    )
