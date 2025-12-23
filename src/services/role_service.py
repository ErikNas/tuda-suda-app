import psycopg
from PySide6.QtCore import QThread, Signal

from services.app_logger import logger


class RoleChangeThread(QThread):
    """Фоновый поток для изменения роли пользователя в БД."""

    success = Signal(str)  # success message
    error = Signal(str)  # error message

    def __init__(self, db_config: dict, email: str, role: str, stand_name: str, parent=None):
        super().__init__(parent)
        self._db_config = db_config
        self._email = email
        self._role = role
        self._stand_name = stand_name

    def run(self):
        logger.info(f"Изменение роли {self._email} на {self._role} ({self._stand_name})...")
        try:
            conn_str = (
                f"host={self._db_config['host']} "
                f"port={self._db_config['port']} "
                f"dbname={self._db_config['name']} "
                f"user={self._db_config['user']} "
                f"password={self._db_config['password']}"
            )
            with psycopg.connect(conn_str) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE users SET role = %s WHERE email = %s",
                        (self._role, self._email)
                    )
                    if cur.rowcount == 0:
                        msg = f"Пользователь {self._email} не найден"
                        logger.error(msg)
                        self.error.emit(msg)
                    else:
                        conn.commit()
                        msg = f"Роль {self._email} изменена на {self._role}"
                        logger.ok(msg)
                        self.success.emit(msg)
        except Exception as e:
            logger.error(f"Ошибка изменения роли: {e}")
            self.error.emit(str(e))
