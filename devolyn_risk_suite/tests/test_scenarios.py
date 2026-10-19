import unittest

from devolyn_risk_suite.agent_tool_safety import safe_model_router
from devolyn_risk_suite.authorization_tenant import safe_ticket_lookup
from devolyn_risk_suite.high_impact_concurrency import refunds, safe_refund
from devolyn_risk_suite.input_and_audit import safe_audit, safe_query
from devolyn_risk_suite.production_dependency import safe_production_settings


class RiskSuiteTests(unittest.TestCase):
    def test_tenant_access_is_denied(self) -> None:
        with self.assertRaises(PermissionError):
            safe_ticket_lookup("T-1", "beta")

    def test_model_tool_allowlist(self) -> None:
        with self.assertRaises(PermissionError):
            safe_model_router("refund_everyone")

    def test_refund_requires_approval_and_is_idempotent(self) -> None:
        refunds.clear()
        keys: set[str] = set()
        with self.assertRaises(PermissionError):
            safe_refund("O-1", False, keys)
        self.assertEqual("refund_created", safe_refund("O-1", True, keys))
        self.assertEqual("already_processed", safe_refund("O-1", True, keys))

    def test_safe_configuration_query_and_audit(self) -> None:
        self.assertFalse(safe_production_settings()["debug"])
        self.assertIn("?", safe_query()[0])
        self.assertEqual("U-1", safe_audit("refund", "U-1", "R-1")["actor_ref"])


if __name__ == "__main__":
    unittest.main()
