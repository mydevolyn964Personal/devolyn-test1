"""In-memory webhook/retry scenarios for duplicate-action review."""

sent_notifications: list[str] = []


def unsafe_webhook_retry(event_id: str) -> str:
    """Deliberately sends every retry again."""
    sent_notifications.append(event_id)
    return "sent"


def safe_webhook_retry(event_id: str, processed: set[str]) -> str:
    if event_id in processed:
        return "duplicate_ignored"
    processed.add(event_id)
    sent_notifications.append(event_id)
    return "sent"
