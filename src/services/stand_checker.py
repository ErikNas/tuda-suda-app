import requests
from PySide6.QtCore import QThread, Signal


class StandCheckerThread(QThread):
    """Фоновый поток для проверки статуса стендов."""

    stand_checked = Signal(str, str, str)  # (name, status, version)
    all_checked = Signal()

    def __init__(self, stands: list[dict], parent=None):
        super().__init__(parent)
        self._stands = stands

    def run(self):
        for stand in self._stands:
            status, version = self._check_stand(stand["api_url"])
            self.stand_checked.emit(stand["name"], status, version)
        self.all_checked.emit()

    def _check_stand(self, api_url: str) -> tuple[str, str]:
        try:
            response = requests.get(f"{api_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                version = data.get("version", "—")
                return "online", version
            return "offline", "—"
        except Exception:
            return "offline", "—"

