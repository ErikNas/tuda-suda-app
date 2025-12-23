import requests
from PySide6.QtCore import QThread, Signal


class TokenFetchThread(QThread):
    """Фоновый поток для получения токена."""

    token_received = Signal(str)  # token
    error_occurred = Signal(str)  # error message

    def __init__(self, api_url: str, endpoint: str, parent=None):
        super().__init__(parent)
        self._api_url = api_url
        self._endpoint = endpoint

    def run(self):
        try:
            url = f"{self._api_url}{self._endpoint}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                token = data.get("token", data.get("access_token", ""))
                if token:
                    self.token_received.emit(token)
                else:
                    self.error_occurred.emit("Токен не найден в ответе")
            else:
                self.error_occurred.emit(f"Ошибка: {response.status_code}")
        except Exception as e:
            self.error_occurred.emit(str(e))

