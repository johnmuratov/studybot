from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def task_actions(task_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Выполнено",
                    callback_data=f"task_done:{task_id}",
                ),
                InlineKeyboardButton(
                    text="🗑 Удалить",
                    callback_data=f"task_delete:{task_id}",
                ),
                
            ]
        ]
    )
