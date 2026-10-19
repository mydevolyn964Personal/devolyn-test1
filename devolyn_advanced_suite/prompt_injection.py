"""Indirect prompt-injection scenarios; model text is represented as strings."""


def unsafe_retrieval_agent(retrieved_text: str) -> str:
    """Deliberately lets retrieved instructions select a privileged action."""
    if "issue_refund" in retrieved_text:
        return "would_execute:issue_refund"
    return "would_execute:search"


def safe_retrieval_agent(retrieved_text: str) -> str:
    """Retrieved text is evidence only; it cannot choose a tool."""
    return "would_execute:search"
