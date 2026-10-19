"""Intentional model-to-tool authorization scenario with no real tools."""


def unsafe_model_router(model_action: str) -> str:
    """Deliberately treats free-form model output as an authorized action."""
    return f"would_execute:{model_action}"


def safe_model_router(model_action: str) -> str:
    allowed = {"search_ticket", "draft_reply"}
    if model_action not in allowed:
        raise PermissionError("Model action is not allowlisted")
    return f"would_execute:{model_action}"
