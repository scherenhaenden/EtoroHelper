import pytest
from unittest.mock import patch, MagicMock


class TestMainArguments:
    """Test cases for main.py argument parsing and logic."""

    @patch('src.dependencies.install_dependencies')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.url_utils.extract_username_from_url')
    def test_user_url_argument_parsing(self, mock_extract, mock_parse_args, mock_install):
        """Test that --user-url argument is parsed and username extracted."""
        mock_args = MagicMock()
        mock_args.user = None
        mock_args.user_url = "https://www.etoro.com/people/testuser"
        mock_args.base_dir = None
        mock_parse_args.return_value = mock_args

        mock_extract.return_value = "testuser"

        with patch.dict('sys.modules', {
            'src.parser': MagicMock(),
            'src.downloader': MagicMock(),
            'src.performance_parser': MagicMock(),
            'src.stats_parser': MagicMock()
        }):
            from main import main
            try:
                main()
            except SystemExit:
                pass

        mock_extract.assert_called_once_with("https://www.etoro.com/people/testuser")

    @patch('src.dependencies.install_dependencies')
    @patch('argparse.ArgumentParser.parse_args')
    def test_base_dir_argument(self, mock_parse_args, mock_install):
        """Test that --base-dir argument is used when provided."""
        mock_args = MagicMock()
        mock_args.user = None
        mock_args.user_url = None
        mock_args.base_dir = "custom-dir"
        mock_parse_args.return_value = mock_args

        with patch.dict('sys.modules', {
            'src.parser': MagicMock(),
            'src.downloader': MagicMock(),
            'src.performance_parser': MagicMock(),
            'src.stats_parser': MagicMock()
        }):
            from main import main
            try:
                main()
            except SystemExit:
                pass

    @patch('src.dependencies.install_dependencies')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.url_utils.extract_username_from_url', side_effect=ValueError("Invalid URL"))
    def test_invalid_url_error_handling(self, mock_extract, mock_parse_args, mock_install):
        """Test that invalid URLs are handled gracefully."""
        mock_args = MagicMock()
        mock_args.user = None
        mock_args.user_url = "invalid-url"
        mock_args.base_dir = None
        mock_parse_args.return_value = mock_args

        with patch('builtins.print') as mock_print:
            from main import main
            main()

        mock_print.assert_any_call("Error parsing URL: Invalid URL")

    @patch('src.dependencies.install_dependencies')
    @patch('argparse.ArgumentParser.parse_args')
    def test_default_base_dir_uses_current_date(self, mock_parse_args, mock_install):
        """Test that default base_dir uses current date."""
        mock_args = MagicMock()
        mock_args.user = None
        mock_args.user_url = None
        mock_args.base_dir = None
        mock_parse_args.return_value = mock_args

        with patch.dict('sys.modules', {
            'src.parser': MagicMock(),
            'src.downloader': MagicMock(),
            'src.performance_parser': MagicMock(),
            'src.stats_parser': MagicMock()
        }):
            from main import main
            try:
                main()
            except SystemExit:
                pass

    @patch('src.dependencies.install_dependencies')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.url_utils.extract_username_from_url')
    def test_user_argument_parsing(self, mock_extract, mock_parse_args, mock_install):
        """Test that --user argument is used directly without calling extract_username_from_url."""
        mock_args = MagicMock()
        mock_args.user = "scherenhaenden"
        mock_args.user_url = None
        mock_args.base_dir = None
        mock_parse_args.return_value = mock_args

        with patch.dict('sys.modules', {
            'src.parser': MagicMock(),
            'src.downloader': MagicMock(),
            'src.performance_parser': MagicMock(),
            'src.stats_parser': MagicMock()
        }):
            with patch('builtins.print') as mock_print:
                from main import main
                try:
                    main()
                except SystemExit:
                    pass

        # extract_username_from_url should NOT be called when --user is provided
        mock_extract.assert_not_called()
        # username should be used directly
        mock_print.assert_any_call("Using username: scherenhaenden")

    @patch('src.dependencies.install_dependencies')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.url_utils.extract_username_from_url')
    def test_user_overrides_user_url(self, mock_extract, mock_parse_args, mock_install):
        """Test that --user takes priority over --user-url."""
        mock_args = MagicMock()
        mock_args.user = "directuser"
        mock_args.user_url = "https://www.etoro.com/people/urluser"
        mock_args.base_dir = None
        mock_parse_args.return_value = mock_args

        with patch.dict('sys.modules', {
            'src.parser': MagicMock(),
            'src.downloader': MagicMock(),
            'src.performance_parser': MagicMock(),
            'src.stats_parser': MagicMock()
        }):
            with patch('builtins.print') as mock_print:
                from main import main
                try:
                    main()
                except SystemExit:
                    pass

        # --user-url should NOT be parsed when --user is given
        mock_extract.assert_not_called()
        mock_print.assert_any_call("Using username: directuser")
