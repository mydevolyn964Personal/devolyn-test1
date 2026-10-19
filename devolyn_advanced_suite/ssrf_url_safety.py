"""URL-validation scenarios; URLs are never fetched."""

from urllib.parse import urlparse


def unsafe_fetch_target(user_url: str) -> str:
    """Deliberately accepts any user URL, including internal targets."""
    return f"would_fetch:{user_url}"


def safe_fetch_target(user_url: str) -> str:
    parsed = urlparse(user_url)
    blocked_hosts = {"localhost", "127.0.0.1", "169.254.169.254"}
    if parsed.scheme != "https" or parsed.hostname in blocked_hosts:
        raise ValueError("URL is not an approved external HTTPS target")
    return f"would_fetch:{parsed.hostname}"
