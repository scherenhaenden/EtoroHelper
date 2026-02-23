import pytest
from src.url_utils import extract_username_from_url


class TestExtractUsernameFromUrl:
    """Test cases for URL parsing functionality."""

    def test_valid_etoro_url(self):
        """Test extracting username from valid eToro URL."""
        url = "https://www.etoro.com/people/scherenhaenden"
        result = extract_username_from_url(url)
        assert result == "scherenhaenden"

    def test_valid_etoro_url_with_path(self):
        """Test extracting username from URL with additional path."""
        url = "https://www.etoro.com/people/scherenhaenden/stats"
        result = extract_username_from_url(url)
        assert result == "scherenhaenden"

    def test_valid_etoro_url_http(self):
        """Test extracting username from HTTP URL."""
        url = "http://www.etoro.com/people/testuser"
        result = extract_username_from_url(url)
        assert result == "testuser"

    def test_valid_etoro_url_subdomain(self):
        """Test extracting username from URL with subdomain."""
        url = "https://www.etoro.com/people/user123"
        result = extract_username_from_url(url)
        assert result == "user123"

    def test_invalid_url_not_etoro(self):
        """Test that non-eToro URLs raise ValueError."""
        with pytest.raises(ValueError, match="Invalid eToro URL"):
            extract_username_from_url("https://www.google.com/people/user")

    def test_invalid_url_no_people_path(self):
        """Test that URLs without /people/ raise ValueError."""
        with pytest.raises(ValueError, match="URL must be an eToro people profile URL"):
            extract_username_from_url("https://www.etoro.com/invest")

    def test_invalid_username_format(self):
        """Test that invalid username characters raise ValueError."""
        with pytest.raises(ValueError, match="Invalid username format"):
            extract_username_from_url("https://www.etoro.com/people/user@name")

    def test_empty_url(self):
        """Test that empty URL raises ValueError."""
        with pytest.raises(ValueError, match="URL cannot be empty"):
            extract_username_from_url("")

    def test_none_url(self):
        """Test that None URL raises ValueError."""
        with pytest.raises(ValueError, match="URL cannot be empty"):
            extract_username_from_url(None)

    def test_username_with_underscore(self):
        """Test username with underscore."""
        url = "https://www.etoro.com/people/user_name"
        result = extract_username_from_url(url)
        assert result == "user_name"

    def test_username_with_dash(self):
        """Test username with dash."""
        url = "https://www.etoro.com/people/user-name"
        result = extract_username_from_url(url)
        assert result == "user-name"

    def test_username_numeric(self):
        """Test numeric username."""
        url = "https://www.etoro.com/people/12345"
        result = extract_username_from_url(url)
        assert result == "12345"
