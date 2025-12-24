from pathlib import Path

import yaml
from pydantic import BaseModel


class VpnCheck(BaseModel):
    name: str
    check_url: str


class Stand(BaseModel):
    name: str
    api_url: str
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    core_swagger_url: str | None = None
    external_swagger_url: str | None = None


class TokenApi(BaseModel):
    endpoint: str


class AppConfig(BaseModel):
    vpn_checks: list[VpnCheck]
    stands: list[Stand]
    token_api: TokenApi


def load_config(config_path: Path) -> AppConfig:
    """Загружает конфиг из YAML файла."""
    if not config_path.exists():
        raise FileNotFoundError(f"Конфиг не найден: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return AppConfig(**data)

