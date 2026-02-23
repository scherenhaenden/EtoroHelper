import re
from urllib.parse import urlparse

def extract_username_from_url(url: str) -> str:
    """
    Extract username from eToro profile URL.

    Args:
        url: eToro URL like https://www.etoro.com/people/username

    Returns:
        Username string

    Raises:
        ValueError: If URL is invalid or not an eToro people URL
    """
    if not url:
        raise ValueError("URL cannot be empty")

    # Parse the URL
    parsed = urlparse(url)

    # Check if it's a valid eToro URL
    if parsed.scheme not in ['http', 'https'] or 'etoro.com' not in parsed.netloc:
        raise ValueError("Invalid eToro URL")

    # Extract path and check format
    path = parsed.path.strip('/')

    # Should be 'people/username' or 'people/username/stats' etc.
    if not path.startswith('people/'):
        raise ValueError("URL must be an eToro people profile URL")

    # Extract username from path
    parts = path.split('/')
    if len(parts) < 2 or parts[0] != 'people':
        raise ValueError("Invalid people URL format")

    username = parts[1]

    # Basic validation for username (alphanumeric, underscore, dash)
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        raise ValueError("Invalid username format")

    return username


def validate_username(username: str) -> str:
    """
    Validate an eToro username directly (without URL).

    Args:
        username: eToro username string (e.g., 'scherenhaenden')

    Returns:
        The validated username string

    Raises:
        ValueError: If the username is empty or has an invalid format
    """
    if not username:
        raise ValueError("Username cannot be empty")

    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        raise ValueError("Invalid username format (only alphanumeric, underscore, dash allowed)")

    return username

