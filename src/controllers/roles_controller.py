from PySide6.QtCore import QObject, Property, Signal, Slot

from config import AppConfig
from services.role_service import RoleChangeThread


class RolesController(QObject):
    """Контроллер для управления ролями пользователей."""

    stands_changed = Signal()
    result_changed = Signal()
    loading_changed = Signal()

    def __init__(self, config: AppConfig, parent=None):
        super().__init__(parent)
        self._config = config
        self._result = ""
        self._is_error = False
        self._loading = False
        self._thread = None

    @Property(list, notify=stands_changed)
    def stands(self) -> list[str]:
        return [s.name for s in self._config.stands]

    @Property(str, notify=result_changed)
    def result(self) -> str:
        return self._result

    @Property(bool, notify=result_changed)
    def is_error(self) -> bool:
        return self._is_error

    @Property(bool, notify=loading_changed)
    def loading(self) -> bool:
        return self._loading

    @Slot(str, str, str)
    def change_role(self, stand_name: str, email: str, role: str):
        if self._loading:
            return

        if not email.strip():
            self._result = "Введите email"
            self._is_error = True
            self.result_changed.emit()
            return

        stand = next((s for s in self._config.stands if s.name == stand_name), None)
        if not stand:
            self._result = "Стенд не найден"
            self._is_error = True
            self.result_changed.emit()
            return

        self._result = ""
        self._loading = True
        self.result_changed.emit()
        self.loading_changed.emit()

        db_config = {
            "host": stand.db_host,
            "port": stand.db_port,
            "name": stand.db_name,
            "user": stand.db_user,
            "password": stand.db_password,
        }

        self._thread = RoleChangeThread(db_config, email.strip(), role, stand_name, self)
        self._thread.success.connect(self._on_success)
        self._thread.error.connect(self._on_error)
        self._thread.start()

    def _on_success(self, message: str):
        self._result = message
        self._is_error = False
        self._loading = False
        self.result_changed.emit()
        self.loading_changed.emit()

    def _on_error(self, message: str):
        self._result = message
        self._is_error = True
        self._loading = False
        self.result_changed.emit()
        self.loading_changed.emit()

