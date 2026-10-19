import unittest

from ollama_train_booking_agent.agent import TrainBookingAgent
from ollama_train_booking_agent.tools import TrainInventory


class OfflineLlm:
    def plan(self, user_message: str) -> str | None:
        return None


class TrainBookingAgentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = TrainBookingAgent(TrainInventory(), OfflineLlm())

    def test_search_returns_local_route(self) -> None:
        trains = self.agent.search_trains("Delhi", "Jaipur")
        self.assertEqual(["QW101", "QW202"], [train["train_id"] for train in trains])

    def test_confirmation_is_required_before_booking(self) -> None:
        proposal = self.agent.propose_booking("QW101", "traveler@example.test")
        with self.assertRaises(PermissionError):
            self.agent.confirm_booking(proposal["booking_id"], "book it")
        self.assertEqual("confirmed", self.agent.confirm_booking(proposal["booking_id"], "yes")["status"])

    def test_fallback_does_not_claim_booking(self) -> None:
        message = self.agent.explain_plan("Book QW101")
        self.assertIn("explicit confirmation", message)


if __name__ == "__main__":
    unittest.main()
