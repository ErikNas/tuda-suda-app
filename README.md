# Tuda-Suda App

Десктоп-приложение для управления и мониторинга тестовых сред.

## Требования

- Python 3.11 или 3.12
- Poetry

## Быстрый старт

```bash
poetry install
poetry run python src/main.py
```

## Сборка

```bash
poetry run pyinstaller tuda-suda.spec
# Результат: dist/tuda-suda
```

## Конфигурация

Создайте `config.yaml` рядом с исполняемым файлом (см. пример в репозитории).

---

## Разработка (Dev)

### Настройка окружения на ALT Linux с нуля

#### 1. Установка Python и базовых инструментов

```bash
# Обновление пакетов
sudo apt-get update

# Установка Python 3.12 (должен быть в базовой системе)
# Проверка версии:
python3 --version

# Установка pipx для изолированной установки poetry
sudo apt-get install -y python3-module-pipx

# Добавление ~/.local/bin в PATH
pipx ensurepath

# Перезапустите терминал или выполните:
source ~/.bashrc
```

#### 2. Установка Poetry

```bash
# Установка poetry через pipx (рекомендуется)
pipx install poetry

# Проверка:
poetry --version
```

#### 3. Клонирование и настройка проекта

```bash
# Клонирование репозитория
git clone <repository-url>
cd tuda-suda-app

# Создание виртуального окружения и установка зависимостей
poetry install

# Запуск приложения
poetry run python src/main.py
```

#### 4. Установка системных зависимостей для PySide6 (при необходимости)

```bash
# Если возникают ошибки с Qt/OpenGL:
sudo apt-get install -y libgl1 libxkbcommon0 libegl1
```

### Структура проекта

```
tuda-suda-app/
├── src/
│   ├── main.py              # Точка входа
│   ├── config.py            # Pydantic-модели конфига
│   ├── controllers/         # Python-контроллеры для QML
│   ├── services/            # Бизнес-логика (VPN, стенды, токены, роли)
│   └── qml/                 # QML-файлы интерфейса
│       ├── Main.qml
│       └── views/
├── config.yaml              # Конфигурация приложения
├── pyproject.toml           # Poetry: зависимости
├── poetry.lock              # Lock-файл
└── tuda-suda.spec           # PyInstaller конфигурация
```

### Полезные команды

```bash
# Запуск приложения
poetry run python src/main.py

# Сборка исполняемого файла
poetry run pyinstaller tuda-suda.spec

# Форматирование кода
poetry run black src/

# Добавление зависимости
poetry add <package>

# Добавление dev-зависимости
poetry add --group dev <package>

# Запуск тестов
poetry run pytest

# Запуск тестов с подробным выводом
poetry run pytest -v
```

### Альтернативный запуск (без poetry)

```bash
# Активация venv напрямую
source .venv/bin/activate
python src/main.py
```
