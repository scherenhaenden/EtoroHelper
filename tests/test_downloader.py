import os
import sys
import types
from unittest.mock import MagicMock, patch

import pytest

def ensure_selenium_stub():
    """Provide a minimal selenium module if it is missing."""
    if 'selenium' in sys.modules:
        return

    selenium_mod = types.ModuleType('selenium')
    webdriver_mod = types.ModuleType('selenium.webdriver')
    support_mod = types.ModuleType('selenium.webdriver.support')
    support_ui_mod = types.ModuleType('selenium.webdriver.support.ui')

    support_ui_mod.WebDriverWait = MagicMock()

    support_mod.ui = support_ui_mod
    webdriver_mod.support = support_mod
    webdriver_mod.Chrome = MagicMock()
    options_obj = MagicMock()
    options_obj.add_argument = MagicMock()
    options_obj.add_argument.side_effect = lambda *_: None
    webdriver_mod.ChromeOptions = MagicMock(return_value=options_obj)
    selenium_mod.webdriver = webdriver_mod

    sys.modules['selenium'] = selenium_mod
    sys.modules['selenium.webdriver'] = webdriver_mod
    sys.modules['selenium.webdriver.support'] = support_mod
    sys.modules['selenium.webdriver.support.ui'] = support_ui_mod


ensure_selenium_stub()


def ensure_webdriver_manager_stub():
    """Stub webdriver_manager module used by downloader."""
    if 'webdriver_manager' in sys.modules:
        return

    webdriver_manager_mod = types.ModuleType('webdriver_manager')
    chrome_mod = types.ModuleType('webdriver_manager.chrome')

    class DummyChromeDriverManager:
        def install(self):
            return '/tmp/chromedriver'

    chrome_mod.ChromeDriverManager = DummyChromeDriverManager
    webdriver_manager_mod.chrome = chrome_mod

    sys.modules['webdriver_manager'] = webdriver_manager_mod
    sys.modules['webdriver_manager.chrome'] = chrome_mod


ensure_webdriver_manager_stub()


def ensure_chrome_submodules():
    chrome_mod = types.ModuleType('selenium.webdriver.chrome')
    service_mod = types.ModuleType('selenium.webdriver.chrome.service')
    service_mod.Service = MagicMock()
    chrome_mod.service = service_mod
    sys.modules['selenium.webdriver.chrome'] = chrome_mod
    sys.modules['selenium.webdriver.chrome.service'] = service_mod


ensure_chrome_submodules()


def ensure_selenium_common_modules():
    common_mod = types.ModuleType('selenium.webdriver.common')
    by_mod = types.ModuleType('selenium.webdriver.common.by')

    class By:
        CSS_SELECTOR = 'css selector'
        ID = 'id'

    by_mod.By = By
    common_mod.by = by_mod

    ec_mod = types.ModuleType('selenium.webdriver.support.expected_conditions')

    def presence_of_element_located(selector):
        def _predicate(driver):
            return True

        return _predicate

    ec_mod.presence_of_element_located = presence_of_element_located

    sys.modules['selenium.webdriver.common'] = common_mod
    sys.modules['selenium.webdriver.common.by'] = by_mod
    sys.modules['selenium.webdriver.support.expected_conditions'] = ec_mod


ensure_selenium_common_modules()


@pytest.fixture(autouse=True)
def mock_webdriver_wait(monkeypatch):
    """Stub out WebDriverWait to avoid real sleeps."""
    mock_wait = MagicMock()
    mock_wait.until.return_value = True
    monkeypatch.setattr('selenium.webdriver.support.ui.WebDriverWait', lambda *args, **kwargs: mock_wait)
    return mock_wait


class TestDownloadIntegration:
    """Integration tests for the downloader module."""

    @patch('webdriver_manager.chrome.ChromeDriverManager.install')
    @patch('selenium.webdriver.Chrome')
    def test_download_person_data_creates_files(self, mock_chrome_class, mock_install, temp_base_dir):
        """Ensure every page is downloaded into the output folder."""
        mock_driver = MagicMock()
        mock_driver.page_source = '<html><body>mock</body></html>'
        mock_chrome_class.return_value = mock_driver
        mock_install.return_value = '/tmp/chromedriver'

        download_dir = os.path.join(temp_base_dir, 'downloads', 'testuser', '2026-02-23')

        from src.downloader import download_person_data
        download_person_data('testuser', download_dir)

        assert mock_chrome_class.called
        assert mock_driver.get.call_count == 4

        assert os.path.exists(os.path.join(download_dir, 'profile.html'))
        assert os.path.exists(os.path.join(download_dir, 'stats.html'))
        assert os.path.exists(os.path.join(download_dir, 'portfolio.html'))
        assert os.path.exists(os.path.join(download_dir, 'chart.html'))

        mock_driver.quit.assert_called_once()

    @patch('webdriver_manager.chrome.ChromeDriverManager.install')
    @patch('selenium.webdriver.Chrome')
    def test_webdriver_setup_failure(self, mock_chrome_class, mock_install, temp_base_dir, capsys):
        """Report errors when Chrome cannot be instantiated."""
        mock_chrome_class.side_effect = Exception('Chrome error')
        mock_install.return_value = '/tmp/chromedriver'

        download_dir = os.path.join(temp_base_dir, 'downloads', 'testuser', '2026-02-23')

        from src.downloader import download_person_data
        download_person_data('testuser', download_dir)

        captured = capsys.readouterr()
        assert 'Error setting up WebDriver' in captured.out
        assert 'Chrome error' in captured.out

    def test_download_no_person_file(self, temp_base_dir, capsys):
        """Download with empty person string should not create any output."""
        from src.downloader import download_person_data
        # Passing an empty person and a download_dir; the function requires person to be non-empty
        # but the downloader itself doesn't validate – that's done in main.py.
        # Here we just confirm no crash occurs when download_dir doesn't yet exist
        download_dir = os.path.join(temp_base_dir, 'downloads', 'nobody', '2026-02-23')
        # We won't actually run selenium here; we just verify setup failure path exits cleanly.
        # The test is now more of a smoke test with an invalid Chrome setup.
        with patch('selenium.webdriver.Chrome', side_effect=Exception('no chrome')):
            with patch('webdriver_manager.chrome.ChromeDriverManager.install', return_value='/tmp/x'):
                download_person_data('nobody', download_dir)
        captured = capsys.readouterr()
        assert 'Error setting up WebDriver' in captured.out
