from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.states.ai_chat import AIChat
from bot.ai.service import AIService
from bot.keyboards.main_menu import main_menu_kb

router = Router()
ai_service = AIService()


# ─────────────────────────────
# Вход в AI-чат
# ─────────────────────────────

@router.message(F.text == "🤖 Спросить AI", ~F.state)
async def enter_ai_chat(message: Message, state: FSMContext):
    """
    Вход в режим AI-чата.
    Разрешён только если пользователь не находится в другом FSM.
    """
    await state.set_state(AIChat.waiting_message)
    await message.answer(
        "🤖 Ты в чате с AI.\n\n"
        "Пиши сообщения — я буду отвечать.\n"
        "Для выхода нажми /cancel или выбери другой раздел.",
        reply_markup=main_menu_kb(),
    )


# ─────────────────────────────
# AI-чат (основной режим)
# ─────────────────────────────

@router.message(AIChat.waiting_message, F.text)
async def ai_chat_message(message: Message, state: FSMContext):
    """
    Обработка сообщений внутри AI-чата.
    """

    text = message.text.strip()

    # Выход через кнопки меню
    if text in {
        "➕ Добавить задачу",
        "📋 Мои задачи",
        "📜 История задач",
        "📊 Отчёт",
    }:
        await state.clear()
        await message.answer(
            "Выход из AI-чата.",
            reply_markup=main_menu_kb(),
        )
        return

    # /cancel обрабатывается отдельным handler-ом
    if text.startswith("/"):
        return

    try:
        await message.answer("🤖 Думаю...")
        answer = await ai_service.ask(text)
        await message.answer(answer)
        # состояние НЕ очищаем
    except Exception:
        await message.answer("⚠️ AI временно недоступен. Попробуй позже.")
