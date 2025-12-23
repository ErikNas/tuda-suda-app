import psycopg
from PySide6.QtCore import QThread, Signal


class RoleChangeThread(QThread):
    """Фоновый поток для изменения роли пользователя в БД."""

    success = Signal(str)  # success message
    error = Signal(str)  # error message

    def __init__(self, db_config: dict, email: str, role: str, parent=None):
        super().__init__(parent)
        self._db_config = db_config
        self._email = email
        self._role = role

    def run(self):
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
                        self.error.emit(f"Пользователь {self._email} не найден")
                    else:
                        conn.commit()
                        self.success.emit(f"Роль {self._email} изменена на {self._role}")
        except Exception as e:
            self.error.emit(str(e))

