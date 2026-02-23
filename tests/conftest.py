import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


# Make tests robust regardless of how pytest is invoked.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def mock_selenium_driver():
    """Mock Selenium WebDriver for testing."""
    with patch('selenium.webdriver.Chrome') as mock_driver_class:
        mock_driver = MagicMock()
        mock_driver_class.return_value = mock_driver
        mock_driver.page_source = "<html><body>Mock HTML content</body></html>"
        yield mock_driver


@pytest.fixture
def mock_dependencies():
    """Mock dependency installation."""
    with patch('src.dependencies.install_dependencies'):
        yield


@pytest.fixture
def temp_base_dir(tmp_path):
    """Create a temporary base directory for testing."""
    base_dir = tmp_path / "test_base"
    base_dir.mkdir()
    return str(base_dir)
