FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Установка Python 3.12 и зависимостей
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.12 \
    python3.12-dev \
    python3.12-venv \
    curl \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libxcb-xfixes0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Установка pip для Python 3.12
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12

# Установка pipx и poetry
RUN python3.12 -m pip install --user pipx \
    && python3.12 -m pipx ensurepath \
    && /root/.local/bin/pipx install poetry

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Копирование файлов проекта из родительской директории
COPY ../pyproject.toml ../poetry.lock ./
COPY ../src/ src/
COPY ../config.yaml ../tuda-suda.spec ./

# Установка зависимостей и сборка
RUN poetry install --no-interaction --no-ansi \
    && poetry run pyinstaller tuda-suda.spec

# Артефакты будут в /app/dist/

