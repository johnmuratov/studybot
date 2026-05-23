УДАЛЕНЫ ТОКЕНЫ БОТА И API AI из файла .env
Описание:
StudyBot — Telegram-бот для управления задачами и взаимодействия с AI.

Функции:
- Добавление задач
- Просмотр задач
- История задач
- Напоминания
- AI-чат
- FSM
- Async scheduler

Структура проекта:
bot/
├── ai/
├── db/
├── handlers/
├── keyboards/
├── scheduler/
├── services/
├── states/

Установка:

1. Создать venv:
python -m venv venv

2. Активировать:
Windows:
venv\Scripts\activate

Linux/macOS:
source venv/bin/activate

3. Установить зависимости:
pip install -r requirements.txt

4. Создать .env:
BOT_TOKEN=your_bot_token
OPENROUTER_API_KEY=your_api_key

5. Запуск:
python -m bot.main

Основные команды:
/start
/menu
/cancel
/add

Технологии:
- Python
- aiogram 3
- SQLAlchemy
- SQLite
- asyncio
- OpenRouter API
