"""Intentional sensitive-header logging scenario; the log is in memory only."""

audit_log: list[dict[str, str]] = []


def unsafe_log_request(email: str, authorization: str) -> None:
    audit_log.append({"email": email, "authorization": authorization})


def safe_log_request(customer_ref: str) -> None:
    audit_log.append({"customer_ref": customer_ref, "event": "request"})
