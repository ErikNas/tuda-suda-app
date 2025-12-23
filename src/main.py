import sys
from pathlib import Path

from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QMessageBox, QApplication

from config import load_config
from controllers.config_controller import ConfigController


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

    # Регистрация контроллера
    config_controller = ConfigController(config)
    engine.rootContext().setContextProperty("configController", config_controller)

    qml_file = Path(__file__).parent / "qml" / "Main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(1)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
