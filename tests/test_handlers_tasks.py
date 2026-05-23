import pytest
from unittest.mock import AsyncMock, MagicMock

from bot.handlers.tasks import my_tasks


@pytest.mark.asyncio
async def test_my_tasks_empty(monkeypatch):
    # mock TaskService
    monkeypatch.setattr(
        "bot.services.task_service.TaskService.get_active_tasks",
        AsyncMock(return_value=[])
    )

    # mock Message
    message = MagicMock()
    message.from_user.id = 123
    message.answer = AsyncMock()

    # call handler
    await my_tasks(message)

    # assert
    message.answer.assert_awaited_once_with("Задач нет 🎉")
