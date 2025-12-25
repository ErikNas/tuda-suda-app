#!/bin/bash
set -e

echo "🔨 Нативная сборка Tuda-Suda (без Docker)"
echo "📍 Запуск из директории: $(pwd)"

# Переход в корень проекта
cd "$(dirname "$0")/.."
PROJECT_ROOT=$(pwd)

echo "📂 Корень проекта: $PROJECT_ROOT"

# Проверка наличия poetry
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry не найден. Установите Poetry:"
    echo "   curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Проверка версии Python
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
REQUIRED_VERSION="3.12"

if ! python3.12 --version &> /dev/null; then
    echo "❌ Python 3.12 не найден. Установите Python 3.12:"
    echo "   sudo apt-get install python3.12 python3.12-dev python3.12-venv"
    exit 1
fi

echo "✅ Python 3.12 найден: $(python3.12 --version)"

# Создание виртуального окружения с Python 3.12
echo "📦 Установка зависимостей..."
cd "$PROJECT_ROOT"
poetry env use python3.12
poetry install --no-interaction --no-ansi

# Сборка
echo "🔨 Сборка приложения с PyInstaller..."
poetry run pyinstaller tuda-suda.spec

# Создание директории для нативной сборки
mkdir -p "$PROJECT_ROOT/distribution/dist-native"

# Копирование артефактов
echo "📋 Копирование артефактов..."
cp -r "$PROJECT_ROOT/dist/"* "$PROJECT_ROOT/distribution/dist-native/"

echo "✅ Нативная сборка завершена: $PROJECT_ROOT/distribution/dist-native/"
echo ""
echo "📊 Информация о системе:"
echo "   Python: $(python3.12 --version)"
echo "   GLIBC: $(ldd --version | head -1)"
echo ""
echo "📦 Для запуска:"
echo "   cd $PROJECT_ROOT/distribution/dist-native"
echo "   ./tuda-suda"

