import pytest
from unittest.mock import patch, MagicMock

from services.token_service import TokenFetchThread


class TestTokenFetchThread:
    """Тесты для TokenFetchThread."""

    def test_fetch_token_success_token_field(self):
        """Успешное получение токена (поле 'token')."""
        signals_received = []

        thread = TokenFetchThread("https://api.test", "/auth/token", "DEV")
        thread.token_received.connect(lambda t: signals_received.append(("token", t)))
        thread.error_occurred.connect(lambda e: signals_received.append(("error", e)))

        with patch("services.token_service.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"token": "abc123"}
            mock_get.return_value = mock_response

            thread.run()

        assert ("token", "abc123") in signals_received
        mock_get.assert_called_once_with("https://api.test/auth/token", timeout=10)

    def test_fetch_token_success_access_token_field(self):
        """Успешное получение токена (поле 'access_token')."""
        signals_received = []

        thread = TokenFetchThread("https://api.test", "/auth/token", "DEV")
        thread.token_received.connect(lambda t: signals_received.append(("token", t)))

        with patch("services.token_service.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"access_token": "xyz789"}
            mock_get.return_value = mock_response

            thread.run()

        assert ("token", "xyz789") in signals_received

    def test_fetch_token_empty_response(self):
        """Пустой ответ — токен не найден."""
        signals_received = []

        thread = TokenFetchThread("https://api.test", "/auth/token", "DEV")
        thread.error_occurred.connect(lambda e: signals_received.append(("error", e)))

        with patch("services.token_service.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            mock_get.return_value = mock_response

            thread.run()

        assert any("не найден" in msg for _, msg in signals_received)

    def test_fetch_token_http_error(self):
        """HTTP ошибка при получении токена."""
        signals_received = []

        thread = TokenFetchThread("https://api.test", "/auth/token", "DEV")
        thread.error_occurred.connect(lambda e: signals_received.append(("error", e)))

        with patch("services.token_service.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 401
            mock_get.return_value = mock_response

            thread.run()

        assert any("401" in msg for _, msg in signals_received)

    def test_fetch_token_connection_error(self):
        """Ошибка соединения."""
        signals_received = []

        thread = TokenFetchThread("https://api.test", "/auth/token", "DEV")
        thread.error_occurred.connect(lambda e: signals_received.append(("error", e)))

        with patch("services.token_service.requests.get") as mock_get:
            mock_get.side_effect = Exception("Connection refused")

            thread.run()

        assert any("Connection refused" in msg for _, msg in signals_received)

    def test_init_parameters(self):
        """Проверка параметров инициализации."""
        thread = TokenFetchThread("https://api.test", "/token", "PROD")

        assert thread._api_url == "https://api.test"
        assert thread._endpoint == "/token"
        assert thread._stand_name == "PROD"

