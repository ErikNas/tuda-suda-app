from datetime import datetime
from PySide6.QtCore import QObject, Signal


class AppLogger(QObject):
    """Централизованный логгер приложения."""

    log_added = Signal(str)  # новая запись лога

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        super().__init__()
        self._logs = []
        self._initialized = True

    def _format_message(self, level: str, message: str) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] {level}: {message}"

    def info(self, message: str):
        entry = self._format_message("INFO", message)
        self._logs.append(entry)
        self.log_added.emit(entry)

    def ok(self, message: str):
        entry = self._format_message("OK", message)
        self._logs.append(entry)
        self.log_added.emit(entry)

    def error(self, message: str):
        entry = self._format_message("ERROR", message)
        self._logs.append(entry)
        self.log_added.emit(entry)

    @property
    def logs(self) -> list[str]:
        return self._logs.copy()

    def clear(self):
        self._logs.clear()


# Глобальный экземпляр
logger = AppLogger()

