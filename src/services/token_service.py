import requests
from PySide6.QtCore import QThread, Signal

from services.app_logger import logger


class TokenFetchThread(QThread):
    """Фоновый поток для получения токена."""

    token_received = Signal(str)  # token
    error_occurred = Signal(str)  # error message

    def __init__(self, api_url: str, endpoint: str, stand_name: str, parent=None):
        super().__init__(parent)
        self._api_url = api_url
        self._endpoint = endpoint
        self._stand_name = stand_name

    def run(self):
        logger.info(f"Получение токена с {self._stand_name}...")
        try:
            url = f"{self._api_url}{self._endpoint}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                token = data.get("token", data.get("access_token", ""))
                if token:
                    logger.ok(f"Токен получен с {self._stand_name}")
                    self.token_received.emit(token)
                else:
                    logger.error("Токен не найден в ответе")
                    self.error_occurred.emit("Токен не найден в ответе")
            else:
                logger.error(f"Ошибка получения токена: HTTP {response.status_code}")
                self.error_occurred.emit(f"Ошибка: {response.status_code}")
        except Exception as e:
            logger.error(f"Ошибка получения токена: {e}")
            self.error_occurred.emit(str(e))
