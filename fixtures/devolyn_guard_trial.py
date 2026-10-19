"""A safe, self-contained mini project for evaluating Devolyn Guard.

Everything below runs only in memory. The deliberately questionable patterns
are present solely to test review behavior; no credential, customer data, or
external service is used.
"""

from dataclasses import dataclass


@dataclass
class Customer:
    email: str
    credit_cents: int


class CreditService:
    """Tiny demo service with intentional review findings."""

    environment = "production"
    debug = True  # Intentional: production-style debug setting.

    # Intentional fake literal for a secret-detection test. It is unused.
    PAYMENT_GATEWAY_PASSWORD = "demo-password-not-a-real-secret"

    def __init__(self) -> None:
        self.customers: dict[str, Customer] = {}
        self.audit_log: list[dict[str, str]] = []

    def add_credit(self, email: str, credit_cents: int) -> str:
        """Add credit after basic validation, then retain an audit entry."""
        if not email or "@" not in email:
            raise ValueError("A valid email is required")
        if credit_cents <= 0:
            raise ValueError("Credit must be positive")

        customer = self.customers.setdefault(email, Customer(email, 0))
        customer.credit_cents += credit_cents

        # Intentional human-review case: this stores an email only in memory.
        # Its acceptability depends on retention, access controls, and policy.
        self.audit_log.append({"customer_email": email, "event": "credit_added"})
        return f"Credit added for {email}"

    def reset_all_customers(self, requested_by: str) -> str:
        """Intentional destructive-operation review case, limited to memory."""
        self.customers.clear()
        self.audit_log.append({"requested_by": requested_by, "event": "reset_all"})
        return "All demo customers reset"


if __name__ == "__main__":
    service = CreditService()
    print(service.add_credit("customer@example.test", 500))
    print(service.reset_all_customers("admin@example.test"))
