import pytest
from config import AppConfig, Stand, VpnCheck, TokenApi


@pytest.fixture
def sample_config():
    """Пример конфигурации для тестов."""
    return AppConfig(
        vpn_checks=[
            VpnCheck(name="VPN-1", check_url="https://vpn1.test/health"),
            VpnCheck(name="VPN-2", check_url="https://vpn2.test/health"),
        ],
        stands=[
            Stand(
                name="DEV-1",
                api_url="https://dev1.test/api",
                db_host="db1.test",
                db_port=5432,
                db_name="testdb",
                db_user="user",
                db_password="pass",
            ),
            Stand(
                name="DEV-2",
                api_url="https://dev2.test/api",
                db_host="db2.test",
                db_port=5432,
                db_name="testdb",
                db_user="user",
                db_password="pass",
            ),
        ],
        token_api=TokenApi(endpoint="/auth/token"),
    )


@pytest.fixture
def config_yaml_content():
    """Валидный YAML-контент для тестов."""
    return """
vpn_checks:
  - name: "VPN-1"
    check_url: "https://vpn1.test/health"

stands:
  - name: "DEV-1"
    api_url: "https://dev1.test/api"
    db_host: "db.test"
    db_port: 5432
    db_name: "testdb"
    db_user: "user"
    db_password: "pass"

token_api:
  endpoint: "/auth/token"
"""


@pytest.fixture
def invalid_yaml_content():
    """Невалидный YAML для тестов ошибок."""
    return "invalid: yaml: : content"


@pytest.fixture
def incomplete_yaml_content():
    """YAML без обязательных полей."""
    return """
vpn_checks:
  - name: "VPN-1"
"""

