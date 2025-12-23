import sys
from pathlib import Path

from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QMessageBox, QApplication

from config import load_config
from controllers.config_controller import ConfigController
from controllers.vpn_controller import VpnController
from controllers.stands_controller import StandsController
from controllers.token_controller import TokenController


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Tuda-Suda App")

    # Загрузка конфига
    config_path = Path(__file__).parent.parent / "config.yaml"
    try:
        config = load_config(config_path)
    except FileNotFoundError as e:
        QMessageBox.critical(None, "Ошибка", str(e))
        sys.exit(1)
    except Exception as e:
        QMessageBox.critical(None, "Ошибка конфигурации", str(e))
        sys.exit(1)

    engine = QQmlApplicationEngine()

    # Регистрация контроллеров
    config_controller = ConfigController(config)
    vpn_controller = VpnController(config)
    stands_controller = StandsController(config)
    token_controller = TokenController(config)

    engine.rootContext().setContextProperty("configController", config_controller)
    engine.rootContext().setContextProperty("vpnController", vpn_controller)
    engine.rootContext().setContextProperty("standsController", stands_controller)
    engine.rootContext().setContextProperty("tokenController", token_controller)

    qml_file = Path(__file__).parent / "qml" / "Main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(1)

    # Запуск VPN-мониторинга
    vpn_controller.start_monitoring()

    exit_code = app.exec()
    vpn_controller.stop_monitoring()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
