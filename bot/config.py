import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///db.sqlite3"
)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY not set")
