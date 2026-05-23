from unittest.mock import MagicMock
from bot.ai import client as ai_client


async def test_ai_explain(monkeypatch):
    fake_client = MagicMock()
    fake_client.responses.create.return_value.output_text = "Ответ"

    monkeypatch.setattr(ai_client, "get_client", lambda: fake_client)

    result = await ai_client.explain("test")
    assert result == "Ответ"
