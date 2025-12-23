from PySide6.QtCore import QObject, Property, Signal, Slot

from services.app_logger import logger


class LogsController(QObject):
    """Контроллер для страницы логов."""

    logs_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._logs_text = ""
        logger.log_added.connect(self._on_log_added)

    def _on_log_added(self, entry: str):
        if self._logs_text:
            self._logs_text += "\n"
        self._logs_text += entry
        self.logs_changed.emit()

    @Property(str, notify=logs_changed)
    def logs_text(self) -> str:
        return self._logs_text

    @Slot()
    def clear(self):
        logger.clear()
        self._logs_text = ""
        self.logs_changed.emit()

