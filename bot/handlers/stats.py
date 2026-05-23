from aiogram import Router, F
from aiogram.types import Message
from bot.services.stats_service import StatsService

router = Router()

@router.message(F.text == "📊 Недельный отчёт")
async def weekly_stats(message: Message):
    completed, deleted, active = await StatsService.weekly_report(
        message.from_user.id
    )

    await message.answer(
        "📊 *Недельный отчёт*\n\n"
        f"✅ Выполнено: {completed}\n"
        f"🗑 Удалено: {deleted}\n"
        f"📌 Активно: {active}",
        parse_mode="Markdown"
    )
