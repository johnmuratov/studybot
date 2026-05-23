from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def task_restore_keyboard(task_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Вернуть",
                    callback_data=f"task_restore:{task_id}"
                )
            ]
        ]
    )