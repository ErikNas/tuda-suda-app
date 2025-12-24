import pytest
from unittest.mock import patch, MagicMock

from services.role_service import RoleChangeThread


class TestRoleChangeThread:
    """Тесты для RoleChangeThread."""

    @pytest.fixture
    def db_config(self):
        return {
            "host": "localhost",
            "port": 5432,
            "name": "testdb",
            "user": "user",
            "password": "pass",
        }

    def test_change_role_success(self, db_config):
        """Успешное изменение роли."""
        signals_received = []

        thread = RoleChangeThread(db_config, "user@test.com", "admin", "DEV")
        thread.success.connect(lambda m: signals_received.append(("success", m)))
        thread.error.connect(lambda e: signals_received.append(("error", e)))

        with patch("services.role_service.psycopg.connect") as mock_connect:
            mock_cursor = MagicMock()
            mock_cursor.rowcount = 1
            mock_conn = MagicMock()
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_conn.__enter__.return_value = mock_conn
            mock_connect.return_value = mock_conn

            thread.run()

        assert any("success" in sig[0] for sig in signals_received)
        assert any("admin" in sig[1] for sig in signals_received if sig[0] == "success")

    def test_change_role_user_not_found(self, db_config):
        """Пользователь не найден."""
        signals_received = []

        thread = RoleChangeThread(db_config, "notfound@test.com", "admin", "DEV")
        thread.error.connect(lambda e: signals_received.append(("error", e)))

        with patch("services.role_service.psycopg.connect") as mock_connect:
            mock_cursor = MagicMock()
            mock_cursor.rowcount = 0  # Ни одна строка не обновлена
            mock_conn = MagicMock()
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_conn.__enter__.return_value = mock_conn
            mock_connect.return_value = mock_conn

            thread.run()

        assert any("не найден" in msg for _, msg in signals_received)

    def test_change_role_connection_error(self, db_config):
        """Ошибка подключения к БД."""
        signals_received = []

        thread = RoleChangeThread(db_config, "user@test.com", "admin", "DEV")
        thread.error.connect(lambda e: signals_received.append(("error", e)))

        with patch("services.role_service.psycopg.connect") as mock_connect:
            mock_connect.side_effect = Exception("Connection refused")

            thread.run()

        assert any("Connection refused" in msg for _, msg in signals_received)

    def test_change_role_sql_error(self, db_config):
        """SQL ошибка."""
        signals_received = []

        thread = RoleChangeThread(db_config, "user@test.com", "admin", "DEV")
        thread.error.connect(lambda e: signals_received.append(("error", e)))

        with patch("services.role_service.psycopg.connect") as mock_connect:
            mock_cursor = MagicMock()
            mock_cursor.execute.side_effect = Exception("SQL syntax error")
            mock_conn = MagicMock()
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_conn.__enter__.return_value = mock_conn
            mock_connect.return_value = mock_conn

            thread.run()

        assert any("SQL syntax error" in msg for _, msg in signals_received)

    def test_init_parameters(self, db_config):
        """Проверка параметров инициализации."""
        thread = RoleChangeThread(db_config, "test@mail.com", "user", "PROD")

        assert thread._db_config == db_config
        assert thread._email == "test@mail.com"
        assert thread._role == "user"
        assert thread._stand_name == "PROD"

    def test_connection_string_format(self, db_config):
        """Проверка формирования строки подключения."""
        thread = RoleChangeThread(db_config, "user@test.com", "admin", "DEV")

        with patch("services.role_service.psycopg.connect") as mock_connect:
            mock_cursor = MagicMock()
            mock_cursor.rowcount = 1
            mock_conn = MagicMock()
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_conn.__enter__.return_value = mock_conn
            mock_connect.return_value = mock_conn

            thread.run()

        # Проверяем, что connect вызван с правильной строкой
        call_args = mock_connect.call_args[0][0]
        assert "host=localhost" in call_args
        assert "port=5432" in call_args
        assert "dbname=testdb" in call_args

