from PySide6.QtCore import QObject, Property, Signal, Slot
from PySide6.QtGui import QGuiApplication

from config import AppConfig
from services.token_service import TokenFetchThread


class TokenController(QObject):
    """Контроллер для получения токена."""

    stands_changed = Signal()
    token_changed = Signal()
    error_changed = Signal()
    loading_changed = Signal()

    def __init__(self, config: AppConfig, parent=None):
        super().__init__(parent)
        self._config = config
        self._token = ""
        self._error = ""
        self._loading = False
        self._fetch_thread = None

    @Property(list, notify=stands_changed)
    def stands(self) -> list[str]:
        return [s.name for s in self._config.stands]

    @Property(str, notify=token_changed)
    def token(self) -> str:
        return self._token

    @Property(str, notify=error_changed)
    def error(self) -> str:
        return self._error

    @Property(bool, notify=loading_changed)
    def loading(self) -> bool:
        return self._loading

    @Slot(str, str, str)
    def fetch_token(self, stand_name: str, username: str, password: str):
        if self._loading:
            return

        stand = next((s for s in self._config.stands if s.name == stand_name), None)
        if not stand:
            self._error = "Стенд не найден"
            self.error_changed.emit()
            return

        if not username or not password:
            self._error = "Введите логин и пароль"
            self.error_changed.emit()
            return

        self._token = ""
        self._error = ""
        self._loading = True
        self.token_changed.emit()
        self.error_changed.emit()
        self.loading_changed.emit()

        self._fetch_thread = TokenFetchThread(
            stand.api_url, stand_name, username, password, self
        )
        self._fetch_thread.token_received.connect(self._on_token_received)
        self._fetch_thread.error_occurred.connect(self._on_error)
        self._fetch_thread.start()

    def _on_token_received(self, token: str):
        self._token = token
        self._loading = False
        self.token_changed.emit()
        self.loading_changed.emit()
        # Копируем в буфер обмена
        QGuiApplication.clipboard().setText(token)

    def _on_error(self, error: str):
        self._error = error
        self._loading = False
        self.error_changed.emit()
        self.loading_changed.emit()

