from PySide6.QtCore import QObject, Property, Signal

from config import AppConfig


class ConfigController(QObject):
    """Контроллер для доступа к конфигу из QML."""

    stands_changed = Signal()

    def __init__(self, config: AppConfig, parent=None):
        super().__init__(parent)
        self._config = config

    @Property(list, notify=stands_changed)
    def stands(self) -> list[dict]:
        return [{"name": s.name, "api_url": s.api_url} for s in self._config.stands]

    @Property(list, notify=stands_changed)
    def vpn_checks(self) -> list[dict]:
        return [{"name": v.name} for v in self._config.vpn_checks]

