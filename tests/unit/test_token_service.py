import pytest
from unittest.mock import patch, MagicMock

from services.token_service import TokenFetchThread


class TestTokenFetchThread:
    """Тесты для TokenFetchThread с SSO-аутентификацией."""

    def test_fetch_token_success(self):
        """Успешное получение токена через SSO."""
        signals_received = []

        thread = TokenFetchThread(
            "https://api.test", "DEV", "testuser", "testpass"
        )
        thread.token_received.connect(lambda t: signals_received.append(("token", t)))
        thread.error_occurred.connect(lambda e: signals_received.append(("error", e)))

        with patch("services.token_service.requests.get") as mock_get, patch(
            "services.token_service.requests.post"
        ) as mock_post:
            # Шаг 1: GET запрос возвращает Location header
            mock_get_response = MagicMock()
            mock_get_response.headers = {
                "Location": "https://sso.test/auth/realms/jaga/something"
            }
            mock_get.return_value = mock_get_response

            # Шаг 2: POST запрос возвращает токен
            mock_post_response = MagicMock()
            mock_post_response.status_code = 200
            mock_post_response.json.return_value = {"access_token": "abc123xyz"}
            mock_post.return_value = mock_post_response

            thread.run()

        assert ("token", "abc123xyz") in signals_received
        mock_get.assert_called_once()
        mock_post.assert_called_once()

    def test_fetch_token_no_location_header(self):
        """Ошибка: отсутствует Location header."""
        signals_received = []

        thread = TokenFetchThread(
            "https://api.test", "DEV", "testuser", "testpass"
        )
        thread.error_occurred.connect(lambda e: signals_received.append(("error", e)))

        with patch("services.token_service.requests.get") as mock_get:
            mock_get_response = MagicMock()
            mock_get_response.headers = {}
            mock_get.return_value = mock_get_response

            thread.run()

        assert any("Location header" in msg for _, msg in signals_received)

    def test_fetch_token_sso_http_error(self):
        """HTTP ошибка при запросе к SSO."""
        signals_received = []

        thread = TokenFetchThread(
            "https://api.test", "DEV", "testuser", "wrongpass"
        )
        thread.error_occurred.connect(lambda e: signals_received.append(("error", e)))

        with patch("services.token_service.requests.get") as mock_get, patch(
            "services.token_service.requests.post"
        ) as mock_post:
            mock_get_response = MagicMock()
            mock_get_response.headers = {
                "Location": "https://sso.test/auth/realms/jaga/something"
            }
            mock_get.return_value = mock_get_response

            mock_post_response = MagicMock()
            mock_post_response.status_code = 401
            mock_post_response.text = "Unauthorized"
            mock_post.return_value = mock_post_response

            thread.run()

        assert any("401" in msg for _, msg in signals_received)

    def test_fetch_token_no_access_token_in_response(self):
        """Ошибка: access_token отсутствует в ответе."""
        signals_received = []

        thread = TokenFetchThread(
            "https://api.test", "DEV", "testuser", "testpass"
        )
        thread.error_occurred.connect(lambda e: signals_received.append(("error", e)))

        with patch("services.token_service.requests.get") as mock_get, patch(
            "services.token_service.requests.post"
        ) as mock_post:
            mock_get_response = MagicMock()
            mock_get_response.headers = {
                "Location": "https://sso.test/auth/realms/jaga/something"
            }
            mock_get.return_value = mock_get_response

            mock_post_response = MagicMock()
            mock_post_response.status_code = 200
            mock_post_response.json.return_value = {}
            mock_post.return_value = mock_post_response

            thread.run()

        assert any("access_token не найден" in msg for _, msg in signals_received)

    def test_fetch_token_connection_error(self):
        """Ошибка соединения."""
        signals_received = []

        thread = TokenFetchThread(
            "https://api.test", "DEV", "testuser", "testpass"
        )
        thread.error_occurred.connect(lambda e: signals_received.append(("error", e)))

        with patch("services.token_service.requests.get") as mock_get:
            mock_get.side_effect = Exception("Connection refused")

            thread.run()

        assert any("Connection refused" in msg for _, msg in signals_received)

    def test_init_parameters(self):
        """Проверка параметров инициализации."""
        thread = TokenFetchThread(
            "https://api.test", "PROD", "myuser", "mypass"
        )

        assert thread._api_url == "https://api.test"
        assert thread._stand_name == "PROD"
        assert thread._username == "myuser"
        assert thread._password == "mypass"

