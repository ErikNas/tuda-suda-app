import requests
from PySide6.QtCore import QThread, Signal


class VpnCheckerThread(QThread):
    """Фоновый поток для проверки доступности VPN."""

    status_updated = Signal(str, bool)  # (vpn_name, is_available)
    check_completed = Signal()

    def __init__(self, vpn_checks: list[dict], parent=None):
        super().__init__(parent)
        self._vpn_checks = vpn_checks
        self._running = True

    def run(self):
        while self._running:
            for vpn in self._vpn_checks:
                if not self._running:
                    break
                is_available = self._check_url(vpn["check_url"])
                self.status_updated.emit(vpn["name"], is_available)

            self.check_completed.emit()

            # Ждём 30 секунд перед следующей проверкой
            for _ in range(30):
                if not self._running:
                    break
                self.msleep(1000)

    def _check_url(self, url: str) -> bool:
        try:
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def stop(self):
        self._running = False
        self.wait()

