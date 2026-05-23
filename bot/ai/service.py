import httpx
import logging
from bot.config import OPENROUTER_API_KEY

logger = logging.getLogger(__name__)


class AIService:
    """
    OpenRouter AI service (OpenAI-compatible).
    Free tier supported.
    """

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    # Бесплатная и стабильная модель
    MODEL = "openai/gpt-3.5-turbo"

    async def ask(self, message: str) -> str:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            # эти заголовки рекомендует сам OpenRouter
            "HTTP-Referer": "https://telegram-bot.local",
            "X-Title": "study-telegram-bot",
        }

        payload = {
            "model": self.MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "Ты полезный ассистент Telegram-бота. Отвечай кратко и по делу."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            "temperature": 0.7,
        }

        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    self.BASE_URL,
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()

                data = response.json()
                return data["choices"][0]["message"]["content"].strip()

        except httpx.HTTPStatusError as e:
            logger.error(
                "OpenRouter API HTTP error %s: %s",
                e.response.status_code,
                e.response.text,
            )
            raise

        except Exception:
            logger.exception("OpenRouter AI error")
            raise
