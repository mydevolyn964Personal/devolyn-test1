import json
from urllib.error import URLError
from urllib.request import Request, urlopen


class OllamaClient:
    """Small stdlib-only client for a local Ollama server."""

    def __init__(self, base_url: str = "http://127.0.0.1:11434", model: str = "qwen3:8b") -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    def plan(self, user_message: str) -> str | None:
        payload = json.dumps({
            "model": self.model,
            "stream": False,
            "messages": [
                {"role": "system", "content": "Classify train-booking requests. Never claim a booking is confirmed without explicit user confirmation."},
                {"role": "user", "content": user_message},
            ],
        }).encode()
        request = Request(
            f"{self.base_url}/api/chat", payload,
            {"Content-Type": "application/json"}, method="POST"
        )
        try:
            with urlopen(request, timeout=10) as response:
                return json.loads(response.read())["message"]["content"]
        except (URLError, TimeoutError, KeyError, json.JSONDecodeError):
            return None
