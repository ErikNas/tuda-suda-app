import pytest
from unittest.mock import patch, MagicMock

from services.vpn_checker import VpnCheckerThread


class TestVpnCheckerThread:
    """Тесты для VpnCheckerThread."""

    def test_check_url_success(self):
        """Успешная проверка URL — статус 200."""
        checker = VpnCheckerThread([{"name": "VPN", "check_url": "https://test"}])

        with patch("services.vpn_checker.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            result = checker._check_url("https://test")

        assert result is True
        mock_get.assert_called_once_with("https://test", timeout=5)

    def test_check_url_server_error(self):
        """Ошибка сервера — статус 500."""
        checker = VpnCheckerThread([{"name": "VPN", "check_url": "https://test"}])

        with patch("services.vpn_checker.requests.get") as mock_get:
            mock_get.return_value.status_code = 500
            result = checker._check_url("https://test")

        assert result is False

    def test_check_url_not_found(self):
        """Страница не найдена — статус 404."""
        checker = VpnCheckerThread([{"name": "VPN", "check_url": "https://test"}])

        with patch("services.vpn_checker.requests.get") as mock_get:
            mock_get.return_value.status_code = 404
            result = checker._check_url("https://test")

        assert result is False

    def test_check_url_connection_error(self):
        """Ошибка соединения."""
        checker = VpnCheckerThread([{"name": "VPN", "check_url": "https://test"}])

        with patch("services.vpn_checker.requests.get") as mock_get:
            mock_get.side_effect = Exception("Connection refused")
            result = checker._check_url("https://test")

        assert result is False

    def test_check_url_timeout(self):
        """Таймаут соединения."""
        import requests

        checker = VpnCheckerThread([{"name": "VPN", "check_url": "https://test"}])

        with patch("services.vpn_checker.requests.get") as mock_get:
            mock_get.side_effect = requests.Timeout("Timeout")
            result = checker._check_url("https://test")

        assert result is False

    def test_init_with_vpn_list(self):
        """Инициализация с списком VPN."""
        vpn_list = [
            {"name": "VPN-1", "check_url": "https://vpn1.test"},
            {"name": "VPN-2", "check_url": "https://vpn2.test"},
        ]

        checker = VpnCheckerThread(vpn_list)

        assert checker._vpn_checks == vpn_list
        assert checker._running is True

    def test_stop(self):
        """Остановка потока."""
        checker = VpnCheckerThread([])
        checker._running = True

        # Мокаем wait чтобы не ждать реально
        with patch.object(checker, "wait"):
            checker.stop()

        assert checker._running is False

