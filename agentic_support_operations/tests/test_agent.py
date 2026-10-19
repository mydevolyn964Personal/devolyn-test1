import unittest

from agentic_support_operations.agent import SupportOperationsAgent


class SupportOperationsAgentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = SupportOperationsAgent()

    def test_order_status_is_read_only_and_completes(self) -> None:
        result = self.agent.handle("T-100", "order_status", {})
        self.assertEqual("completed", result["status"])
        self.assertIn("O-77", result["message"])

    def test_refund_requires_authorized_human_approval(self) -> None:
        proposal = self.agent.handle("T-100", "refund", {"amount_cents": "500"})
        self.assertEqual("proposed", proposal["status"])
        rejected = self.agent.approve_refund(proposal["action_id"], "U-1", "support_agent", "key-1")
        self.assertEqual("rejected", rejected["status"])
        approved = self.agent.approve_refund(proposal["action_id"], "U-2", "support_manager", "key-1")
        self.assertEqual("completed", approved["status"])

    def test_unknown_action_is_not_allowlisted(self) -> None:
        result = self.agent.handle("T-100", "delete_customer", {})
        self.assertEqual("rejected", result["status"])

    def test_audit_excludes_email_and_ticket_body(self) -> None:
        self.agent.handle("T-100", "order_status", {})
        serialized = str(self.agent.audit_events)
        self.assertNotIn("customer@example.test", serialized)
        self.assertNotIn("Where is my order?", serialized)


if __name__ == "__main__":
    unittest.main()
