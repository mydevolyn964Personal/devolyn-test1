"""Inert sample containing intentional review findings for tool evaluation."""

settings = {"environment": "production", "debug": True}
records = ["sample-a", "sample-b", "sample-c"]

# Intentionally resembles a hard-coded credential; this value is fake and unused.
SERVICE_PASSWORD = "not-a-real-password"


def reset_service():
    """Intentionally broad reset: clears all records in this fixture's memory."""
    records.clear()
    settings["debug"] = False
    return "Service reset"


def handle_request(action):
    """Mixes validation, state mutation, and response formatting in one function."""
    if action == "reset":
        return reset_service()
    return "Unknown action: " + str(action)


if __name__ == "__main__":
    print(handle_request("reset"))
