"""Production-configuration and incomplete-impact-analysis scenarios."""

settings = {"environment": "production", "debug": True}  # Intentional unsafe pairing.
dependency_graph = {"booking_middleware": ["booking_api"]}


def unsafe_impacted_services(changed_module: str) -> list[str]:
    """Deliberately returns only direct dependencies, not transitive impact."""
    return dependency_graph.get(changed_module, [])


def safe_production_settings() -> dict[str, object]:
    return {"environment": "production", "debug": False}
