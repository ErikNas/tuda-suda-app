# Tuda-Suda App

Десктоп-приложение для управления и мониторинга тестовых сред.

## Требования

- Python 3.11+
- Poetry

## Установка и запуск (разработка)

```bash
# Установка зависимостей
poetry install

# Запуск
poetry run python src/main.py
```

## Сборка

```bash
# Сборка исполняемого файла (Linux)
poetry run pyinstaller tuda-suda.spec

# Результат: dist/tuda-suda
```

## Конфигурация

Создайте `config.yaml` рядом с исполняемым файлом (см. пример в репозитории).
