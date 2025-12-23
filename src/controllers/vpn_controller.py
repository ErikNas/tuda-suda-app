from PySide6.QtCore import QObject, Property, Signal

from config import AppConfig
from services.vpn_checker import VpnCheckerThread


class VpnController(QObject):
    """Контроллер VPN-мониторинга для QML."""

    vpn_status_changed = Signal()

    def __init__(self, config: AppConfig, parent=None):
        super().__init__(parent)
        self._config = config
        self._statuses = {vpn.name: None for vpn in config.vpn_checks}
        self._checker_thread = None

    def start_monitoring(self):
        vpn_list = [{"name": v.name, "check_url": v.check_url} for v in self._config.vpn_checks]
        self._checker_thread = VpnCheckerThread(vpn_list, self)
        self._checker_thread.status_updated.connect(self._on_status_updated)
        self._checker_thread.start()

    def stop_monitoring(self):
        if self._checker_thread:
            self._checker_thread.stop()

    def _on_status_updated(self, name: str, is_available: bool):
        self._statuses[name] = is_available
        self.vpn_status_changed.emit()

    @Property(list, notify=vpn_status_changed)
    def vpn_list(self) -> list[dict]:
        return [
            {"name": name, "available": status}
            for name, status in self._statuses.items()
        ]

