from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.ai.service import AIService

router = Router()
ai_service = AIService()


class AIStates(StatesGroup):
    waiting_for_question = State()


@router.message(F.text == "🤖 Спросить AI")
async def ask_ai_start(message: Message, state: FSMContext):
    await state.set_state(AIStates.waiting_for_question)
    await message.answer("🤖 Напиши свой вопрос")


@router.message(AIStates.waiting_for_question)
async def ask_ai(message: Message, state: FSMContext):
    question = message.text.strip()

    if not question:
        await message.answer("❗ Вопрос не может быть пустым")
        return

    await message.answer("⌛ Думаю...")

    try:
        answer = await ai_service.ask(question)
        await message.answer(answer)
    except Exception:
        await message.answer("⚠️ Ошибка AI. Попробуй позже.")

    # ⬅️ ВАЖНО: выходим из AI-режима
    await state.clear()
