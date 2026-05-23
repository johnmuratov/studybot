from datetime import timedelta, datetime

async def get_tasks_with_24h_deadline(session):
    """
    Возвращает задачи, у которых дедлайн через 24 часа
    """
    now = datetime.utcnow()
    target = now + timedelta(hours=24)

    # здесь будет запрос к БД
    return []
