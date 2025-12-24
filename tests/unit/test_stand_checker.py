import pytest
from unittest.mock import patch, MagicMock

from services.stand_checker import StandCheckerThread


class TestStandCheckerThread:
    """Тесты для StandCheckerThread."""

    def test_check_stand_online_with_version(self):
        """Стенд онлайн с версией."""
        checker = StandCheckerThread([{"name": "DEV", "api_url": "https://dev.test"}])

        with patch("services.stand_checker.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"version": "1.2.3"}
            mock_get.return_value = mock_response

            status, version = checker._check_stand("DEV", "https://dev.test")

        assert status == "online"
        assert version == "1.2.3"
        mock_get.assert_called_once_with("https://dev.test/health", timeout=5)

    def test_check_stand_online_without_version(self):
        """Стенд онлайн без версии в ответе."""
        checker = StandCheckerThread([])

        with patch("services.stand_checker.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            mock_get.return_value = mock_response

            status, version = checker._check_stand("DEV", "https://dev.test")

        assert status == "online"
        assert version == "—"

    def test_check_stand_offline_http_error(self):
        """Стенд оффлайн — HTTP ошибка."""
        checker = StandCheckerThread([])

        with patch("services.stand_checker.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 503
            mock_get.return_value = mock_response

            status, version = checker._check_stand("DEV", "https://dev.test")

        assert status == "offline"
        assert version == "—"

    def test_check_stand_offline_connection_error(self):
        """Стенд оффлайн — ошибка соединения."""
        checker = StandCheckerThread([])

        with patch("services.stand_checker.requests.get") as mock_get:
            mock_get.side_effect = Exception("Connection refused")

            status, version = checker._check_stand("DEV", "https://dev.test")

        assert status == "offline"
        assert version == "—"

    def test_check_stand_offline_timeout(self):
        """Стенд оффлайн — таймаут."""
        import requests

        checker = StandCheckerThread([])

        with patch("services.stand_checker.requests.get") as mock_get:
            mock_get.side_effect = requests.Timeout()

            status, version = checker._check_stand("DEV", "https://dev.test")

        assert status == "offline"
        assert version == "—"

    def test_check_stand_json_decode_error(self):
        """Ошибка декодирования JSON."""
        checker = StandCheckerThread([])

        with patch("services.stand_checker.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.side_effect = ValueError("Invalid JSON")
            mock_get.return_value = mock_response

            status, version = checker._check_stand("DEV", "https://dev.test")

        assert status == "offline"
        assert version == "—"

    def test_init_with_stands_list(self):
        """Инициализация со списком стендов."""
        stands = [
            {"name": "DEV-1", "api_url": "https://dev1.test"},
            {"name": "DEV-2", "api_url": "https://dev2.test"},
        ]

        checker = StandCheckerThread(stands)

        assert checker._stands == stands

