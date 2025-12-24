import pytest
from unittest.mock import patch, MagicMock

from controllers.config_controller import ConfigController
from controllers.vpn_controller import VpnController
from controllers.stands_controller import StandsController
from controllers.token_controller import TokenController
from controllers.roles_controller import RolesController
from controllers.logs_controller import LogsController


class TestConfigController:
    """Интеграционные тесты ConfigController."""

    def test_stands_property(self, sample_config):
        """Свойство stands возвращает список стендов."""
        controller = ConfigController(sample_config)

        stands = controller.stands

        assert len(stands) == 2
        assert stands[0]["name"] == "DEV-1"
        assert "api_url" in stands[0]

    def test_vpn_checks_property(self, sample_config):
        """Свойство vpn_checks возвращает список VPN."""
        controller = ConfigController(sample_config)

        vpn_checks = controller.vpn_checks

        assert len(vpn_checks) == 2
        assert vpn_checks[0]["name"] == "VPN-1"


class TestVpnController:
    """Интеграционные тесты VpnController."""

    def test_vpn_list_initial_state(self, sample_config):
        """Начальное состояние — все VPN с None статусом."""
        controller = VpnController(sample_config)

        vpn_list = controller.vpn_list

        assert len(vpn_list) == 2
        assert all(vpn["available"] is None for vpn in vpn_list)

    def test_start_stop_monitoring(self, sample_config):
        """Запуск и остановка мониторинга."""
        controller = VpnController(sample_config)

        with patch("controllers.vpn_controller.VpnCheckerThread") as mock_thread:
            mock_instance = MagicMock()
            mock_thread.return_value = mock_instance

            controller.start_monitoring()

            mock_thread.assert_called_once()
            mock_instance.start.assert_called_once()

            controller.stop_monitoring()
            mock_instance.stop.assert_called_once()


class TestStandsController:
    """Интеграционные тесты StandsController."""

    def test_stands_initial_state(self, sample_config):
        """Начальное состояние стендов."""
        controller = StandsController(sample_config)

        stands = controller.stands

        assert len(stands) == 2
        assert all(s["status"] == "unknown" for s in stands)
        assert all(s["version"] == "—" for s in stands)

    def test_loading_property(self, sample_config):
        """Свойство loading."""
        controller = StandsController(sample_config)

        assert controller.loading is False

    def test_refresh_starts_checker(self, sample_config):
        """Метод refresh запускает проверку."""
        controller = StandsController(sample_config)

        with patch("controllers.stands_controller.StandCheckerThread") as mock_thread:
            mock_instance = MagicMock()
            mock_thread.return_value = mock_instance

            controller.refresh()

            assert controller.loading is True
            mock_thread.assert_called_once()
            mock_instance.start.assert_called_once()

    def test_refresh_ignored_when_loading(self, sample_config):
        """Повторный refresh игнорируется при загрузке."""
        controller = StandsController(sample_config)
        controller._loading = True

        with patch("controllers.stands_controller.StandCheckerThread") as mock_thread:
            controller.refresh()

            mock_thread.assert_not_called()


class TestTokenController:
    """Интеграционные тесты TokenController."""

    def test_stands_property(self, sample_config):
        """Свойство stands возвращает имена стендов."""
        controller = TokenController(sample_config)

        stands = controller.stands

        assert stands == ["DEV-1", "DEV-2"]

    def test_initial_state(self, sample_config):
        """Начальное состояние."""
        controller = TokenController(sample_config)

        assert controller.token == ""
        assert controller.error == ""
        assert controller.loading is False

    def test_fetch_token_unknown_stand(self, sample_config):
        """Ошибка при неизвестном стенде."""
        controller = TokenController(sample_config)

        controller.fetch_token("UNKNOWN")

        assert controller.error == "Стенд не найден"

    def test_fetch_token_starts_thread(self, sample_config):
        """fetch_token запускает поток."""
        controller = TokenController(sample_config)

        with patch("controllers.token_controller.TokenFetchThread") as mock_thread:
            mock_instance = MagicMock()
            mock_thread.return_value = mock_instance

            controller.fetch_token("DEV-1")

            assert controller.loading is True
            mock_thread.assert_called_once()
            mock_instance.start.assert_called_once()


class TestRolesController:
    """Интеграционные тесты RolesController."""

    def test_stands_property(self, sample_config):
        """Свойство stands возвращает имена стендов."""
        controller = RolesController(sample_config)

        stands = controller.stands

        assert stands == ["DEV-1", "DEV-2"]

    def test_initial_state(self, sample_config):
        """Начальное состояние."""
        controller = RolesController(sample_config)

        assert controller.result == ""
        assert controller.is_error is False
        assert controller.loading is False

    def test_change_role_empty_email(self, sample_config):
        """Ошибка при пустом email."""
        controller = RolesController(sample_config)

        controller.change_role("DEV-1", "", "admin")

        assert controller.result == "Введите email"
        assert controller.is_error is True

    def test_change_role_unknown_stand(self, sample_config):
        """Ошибка при неизвестном стенде."""
        controller = RolesController(sample_config)

        controller.change_role("UNKNOWN", "user@test.com", "admin")

        assert controller.result == "Стенд не найден"
        assert controller.is_error is True

    def test_change_role_starts_thread(self, sample_config):
        """change_role запускает поток."""
        controller = RolesController(sample_config)

        with patch("controllers.roles_controller.RoleChangeThread") as mock_thread:
            mock_instance = MagicMock()
            mock_thread.return_value = mock_instance

            controller.change_role("DEV-1", "user@test.com", "admin")

            assert controller.loading is True
            mock_thread.assert_called_once()
            mock_instance.start.assert_called_once()


class TestLogsController:
    """Интеграционные тесты LogsController."""

    def test_initial_state(self):
        """Начальное состояние."""
        # Сбрасываем логгер
        from services.app_logger import AppLogger
        AppLogger._instance = None

        controller = LogsController()

        assert controller.logs_text == ""

        AppLogger._instance = None

    def test_clear_logs(self):
        """Очистка логов."""
        from services.app_logger import AppLogger, logger
        AppLogger._instance = None

        controller = LogsController()
        logger.info("Test message")

        assert controller.logs_text != ""

        controller.clear()

        assert controller.logs_text == ""

        AppLogger._instance = None

