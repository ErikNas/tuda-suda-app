import pytest
from pathlib import Path
from pydantic import ValidationError

from config import load_config, AppConfig


class TestLoadConfig:
    """Тесты загрузки конфигурации."""

    def test_load_valid_config(self, tmp_path, config_yaml_content):
        """Успешная загрузка валидного конфига."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_yaml_content)

        config = load_config(config_file)

        assert isinstance(config, AppConfig)
        assert len(config.vpn_checks) == 1
        assert config.vpn_checks[0].name == "VPN-1"
        assert len(config.stands) == 1
        assert config.stands[0].name == "DEV-1"
        assert config.stands[0].db_port == 5432
        assert config.token_api.endpoint == "/auth/token"

    def test_load_config_file_not_found(self):
        """Ошибка при отсутствии файла."""
        with pytest.raises(FileNotFoundError) as exc_info:
            load_config(Path("/nonexistent/config.yaml"))

        assert "не найден" in str(exc_info.value)

    def test_load_config_invalid_yaml(self, tmp_path, invalid_yaml_content):
        """Ошибка при невалидном YAML."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(invalid_yaml_content)

        with pytest.raises(Exception):
            load_config(config_file)

    def test_load_config_missing_required_fields(self, tmp_path, incomplete_yaml_content):
        """Ошибка при отсутствии обязательных полей."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(incomplete_yaml_content)

        with pytest.raises(ValidationError):
            load_config(config_file)

    def test_load_config_empty_file(self, tmp_path):
        """Ошибка при пустом файле."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("")

        with pytest.raises(Exception):
            load_config(config_file)


class TestAppConfigModel:
    """Тесты pydantic-модели конфига."""

    def test_stand_model_validation(self):
        """Валидация модели Stand."""
        from config import Stand

        stand = Stand(
            name="TEST",
            api_url="https://test.com/api",
            db_host="localhost",
            db_port=5432,
            db_name="db",
            db_user="user",
            db_password="pass",
        )

        assert stand.name == "TEST"
        assert stand.db_port == 5432

    def test_stand_invalid_port_type(self):
        """Ошибка при неверном типе порта."""
        from config import Stand

        # pydantic автоматически конвертирует строку в int
        stand = Stand(
            name="TEST",
            api_url="https://test.com/api",
            db_host="localhost",
            db_port="5432",  # строка, будет конвертирована
            db_name="db",
            db_user="user",
            db_password="pass",
        )
        assert stand.db_port == 5432

    def test_vpn_check_model(self):
        """Валидация модели VpnCheck."""
        from config import VpnCheck

        vpn = VpnCheck(name="VPN", check_url="https://vpn.test")

        assert vpn.name == "VPN"
        assert vpn.check_url == "https://vpn.test"

