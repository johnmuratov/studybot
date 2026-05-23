import pytest
from bot.scheduler.deadlines import get_tasks_with_24h_deadline


@pytest.mark.asyncio
async def test_24h_reminder(session):
    tasks = await get_tasks_with_24h_deadline(session)
    assert tasks == []
