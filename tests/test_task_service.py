import pytest
from bot.services.task_service import TaskService

@pytest.mark.asyncio
async def test_get_active_tasks_empty():
    tasks = await TaskService.get_active_tasks(user_id=999)
    assert tasks == []
