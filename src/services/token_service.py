import requests
from PySide6.QtCore import QThread, Signal

from services.app_logger import logger


class TokenFetchThread(QThread):
    """Фоновый поток для получения токена через SSO."""

    token_received = Signal(str)
    error_occurred = Signal(str)

    def __init__(
        self,
        api_url: str,
        stand_name: str,
        username: str,
        password: str,
        parent=None,
    ):
        super().__init__(parent)
        self._api_url = api_url
        self._stand_name = stand_name
        self._username = username
        self._password = password

    def run(self):
        logger.info(f"🌐 Получение токена с {self._stand_name}...")
        try:
            # Шаг 1: Получить SSO location
            redirect_url = f"{self._api_url}/backend/auth?redirectUrl=/"
            response = requests.get(
                f"{self._api_url}/backend/auth",
                params={"redirectUrl": redirect_url},
                timeout=10,
                verify=False,
                allow_redirects=False,
            )

            location = response.headers.get("Location", "")
            if not location:
                raise ValueError("Location header не найден")

            sso_uri = location.split("/auth")[0]
            logger.info(f"✅ SSO URI: {sso_uri}")

            # Шаг 2: Получить токен через SSO
            form_params = {
                "username": self._username,
                "password": self._password,
                "grant_type": "password",
                "scope": "openid",
                "client_id": "jaga",
            }

            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            token_url = f"{sso_uri}/auth/realms/jaga/protocol/openid-connect/token"

            token_response = requests.post(
                token_url, data=form_params, timeout=10, verify=False, headers=headers
            )

            if token_response.status_code != 200:
                raise ValueError(
                    f"HTTP {token_response.status_code}: {token_response.text}"
                )

            token = token_response.json().get("access_token")
            if not token:
                raise ValueError("access_token не найден в ответе")

            logger.ok(f"✅ Токен получен с {self._stand_name}")
            self.token_received.emit(token)

        except Exception as e:
            logger.error(f"❌ Ошибка получения токена: {e}")
            self.error_occurred.emit(str(e))
