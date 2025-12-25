#!/bin/bash
set -e

echo "🔨 Сборка Tuda-Suda для Linux (Ubuntu 22.04 / GLIBC 2.35)"
echo "📍 Запуск из директории: $(pwd)"

# Переход в корень проекта
cd "$(dirname "$0")/.."
PROJECT_ROOT=$(pwd)

echo "📂 Корень проекта: $PROJECT_ROOT"

# Создание директории для артефактов
mkdir -p "$PROJECT_ROOT/distribution/dist-docker"

# Сборка Docker образа
echo "📦 Сборка Docker образа..."
docker build -t tuda-suda-builder -f "$PROJECT_ROOT/distribution/Dockerfile" "$PROJECT_ROOT"

# Запуск контейнера и копирование артефактов
echo "🚀 Сборка приложения в контейнере..."
docker run --rm -v "$PROJECT_ROOT/distribution/dist-docker:/output" tuda-suda-builder sh -c "cp -r /app/dist/* /output/"

echo "✅ Сборка завершена: $PROJECT_ROOT/distribution/dist-docker/"
echo ""
echo "Проверка версии GLIBC бинарника:"
docker run --rm -v "$PROJECT_ROOT/distribution/dist-docker:/output" ubuntu:22.04 ldd --version | head -1
echo ""
echo "📦 Для запуска:"
echo "   cd $PROJECT_ROOT/distribution/dist-docker"
echo "   ./tuda-suda"

