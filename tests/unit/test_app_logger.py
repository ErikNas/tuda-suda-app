import pytest
from unittest.mock import MagicMock
import re

from services.app_logger import AppLogger, logger


class TestAppLogger:
    """Тесты для AppLogger."""

    @pytest.fixture
    def fresh_logger(self):
        """Создаёт новый экземпляр логгера для теста."""
        # Сбрасываем синглтон для чистого теста
        AppLogger._instance = None
        new_logger = AppLogger()
        yield new_logger
        # Восстанавливаем
        AppLogger._instance = None

    def test_singleton_pattern(self):
        """Проверка паттерна синглтон."""
        AppLogger._instance = None
        logger1 = AppLogger()
        logger2 = AppLogger()

        assert logger1 is logger2
        AppLogger._instance = None

    def test_info_message_format(self, fresh_logger):
        """Формат INFO сообщения."""
        signals = []
        fresh_logger.log_added.connect(lambda msg: signals.append(msg))

        fresh_logger.info("Test message")

        assert len(signals) == 1
        assert "INFO" in signals[0]
        assert "Test message" in signals[0]
        # Проверка формата timestamp
        assert re.match(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]", signals[0])

    def test_ok_message_format(self, fresh_logger):
        """Формат OK сообщения."""
        signals = []
        fresh_logger.log_added.connect(lambda msg: signals.append(msg))

        fresh_logger.ok("Success message")

        assert len(signals) == 1
        assert "OK" in signals[0]
        assert "Success message" in signals[0]

    def test_error_message_format(self, fresh_logger):
        """Формат ERROR сообщения."""
        signals = []
        fresh_logger.log_added.connect(lambda msg: signals.append(msg))

        fresh_logger.error("Error message")

        assert len(signals) == 1
        assert "ERROR" in signals[0]
        assert "Error message" in signals[0]

    def test_logs_property(self, fresh_logger):
        """Свойство logs возвращает копию списка."""
        fresh_logger.info("Message 1")
        fresh_logger.ok("Message 2")
        fresh_logger.error("Message 3")

        logs = fresh_logger.logs

        assert len(logs) == 3
        # Проверяем, что это копия
        logs.append("New message")
        assert len(fresh_logger.logs) == 3

    def test_clear_logs(self, fresh_logger):
        """Очистка логов."""
        fresh_logger.info("Message 1")
        fresh_logger.info("Message 2")

        assert len(fresh_logger.logs) == 2

        fresh_logger.clear()

        assert len(fresh_logger.logs) == 0

    def test_signal_emitted_on_log(self, fresh_logger):
        """Сигнал log_added emit при добавлении записи."""
        mock_slot = MagicMock()
        fresh_logger.log_added.connect(mock_slot)

        fresh_logger.info("Test")

        mock_slot.assert_called_once()
        assert "Test" in mock_slot.call_args[0][0]

    def test_multiple_logs_order(self, fresh_logger):
        """Порядок логов сохраняется."""
        fresh_logger.info("First")
        fresh_logger.ok("Second")
        fresh_logger.error("Third")

        logs = fresh_logger.logs

        assert "First" in logs[0]
        assert "Second" in logs[1]
        assert "Third" in logs[2]

    def test_global_logger_instance(self):
        """Глобальный экземпляр logger доступен."""
        # logger импортирован из модуля
        assert logger is not None
        assert isinstance(logger, AppLogger)

