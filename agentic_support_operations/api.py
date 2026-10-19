from .agent import SupportOperationsAgent


class SupportApi:
    """Transport-neutral request facade; real auth belongs before this layer."""

    def __init__(self, agent: SupportOperationsAgent | None = None) -> None:
        self.agent = agent or SupportOperationsAgent()

    def execute(self, request: dict[str, object]) -> dict[str, str]:
        ticket_id = request.get("ticket_id")
        action = request.get("action")
        payload = request.get("payload", {})
        if not isinstance(ticket_id, str) or not isinstance(action, str) or not isinstance(payload, dict):
            return {"status": "rejected", "reason": "Invalid request schema"}
        if not all(isinstance(key, str) and isinstance(value, str) for key, value in payload.items()):
            return {"status": "rejected", "reason": "Payload values must be strings"}
        return self.agent.handle(ticket_id, action, payload)
