from .ollama_client import OllamaClient
from .tools import TrainInventory


class TrainBookingAgent:
    """Orchestrates LLM planning, local tools, and explicit-confirmation policy."""

    def __init__(self, inventory: TrainInventory | None = None, llm: OllamaClient | None = None) -> None:
        self.inventory = inventory or TrainInventory()
        self.llm = llm or OllamaClient()

    def search_trains(self, origin: str, destination: str) -> list[dict[str, object]]:
        return [train.__dict__ for train in self.inventory.search(origin, destination)]

    def propose_booking(self, train_id: str, passenger_email: str) -> dict[str, str]:
        booking = self.inventory.create_pending_booking(train_id, passenger_email)
        return {
            "booking_id": booking.booking_id,
            "status": booking.status,
            "next_step": "Ask the customer to explicitly reply yes before confirming.",
        }

    def confirm_booking(self, booking_id: str, customer_reply: str) -> dict[str, str]:
        booking = self.inventory.confirm_booking(booking_id, customer_reply)
        return {"booking_id": booking.booking_id, "status": booking.status}

    def explain_plan(self, user_message: str) -> str:
        """Uses Qwen when available; safe deterministic fallback otherwise."""
        return self.llm.plan(user_message) or (
            "I can search local demo trains and prepare a booking. "
            "I will require explicit confirmation before confirming it."
        )
