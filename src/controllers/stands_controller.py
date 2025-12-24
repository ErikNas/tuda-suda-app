from PySide6.QtCore import QObject, Property, Signal, Slot

from config import AppConfig
from services.stand_checker import StandCheckerThread


class StandsController(QObject):
    """Контроллер для управления стендами."""

    stands_changed = Signal()
    loading_changed = Signal()

    def __init__(self, config: AppConfig, parent=None):
        super().__init__(parent)
        self._config = config
        self._stands_data = {
            s.name: {
                "name": s.name,
                "api_url": s.api_url,
                "core_swagger_url": s.core_swagger_url or "",
                "external_swagger_url": s.external_swagger_url or "",
                "status": "unknown",
                "version": "—",
            }
            for s in config.stands
        }
        self._loading = False
        self._checker_thread = None

    @Property(list, notify=stands_changed)
    def stands(self) -> list[dict]:
        return list(self._stands_data.values())

    @Property(bool, notify=loading_changed)
    def loading(self) -> bool:
        return self._loading

    @Slot()
    def refresh(self):
        if self._loading:
            return

        self._loading = True
        self.loading_changed.emit()

        stands_list = [{"name": s.name, "api_url": s.api_url} for s in self._config.stands]
        self._checker_thread = StandCheckerThread(stands_list, self)
        self._checker_thread.stand_checked.connect(self._on_stand_checked)
        self._checker_thread.all_checked.connect(self._on_all_checked)
        self._checker_thread.start()

    def _on_stand_checked(self, name: str, status: str, version: str):
        self._stands_data[name]["status"] = status
        self._stands_data[name]["version"] = version
        self.stands_changed.emit()

    def _on_all_checked(self):
        self._loading = False
        self.loading_changed.emit()

