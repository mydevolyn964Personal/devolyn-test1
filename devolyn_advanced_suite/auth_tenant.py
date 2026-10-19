"""Authentication and tenant-isolation scenarios using local dictionaries."""

DOCUMENTS = {"D-1": {"tenant": "alpha", "classification": "internal"}}


def unsafe_document_access(document_id: str, caller_tenant: str, authenticated: bool) -> dict[str, str]:
    """Deliberately ignores caller identity, authentication, and tenant scope."""
    return DOCUMENTS[document_id]


def safe_document_access(document_id: str, caller_tenant: str, authenticated: bool) -> dict[str, str]:
    if not authenticated:
        raise PermissionError("Authentication required")
    document = DOCUMENTS[document_id]
    if document["tenant"] != caller_tenant:
        raise PermissionError("Cross-tenant access denied")
    return document
