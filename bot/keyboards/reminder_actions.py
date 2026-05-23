from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def reminder_actions(task_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⏳ 10 мин",
                    callback_data=f"snooze:{task_id}:10"
                ),
                InlineKeyboardButton(
                    text="⏳ 1 час",
                    callback_data=f"snooze:{task_id}:60"
                )
            ]
        ]
    )
