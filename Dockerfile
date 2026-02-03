# Используем официальный Python образ
FROM python:3.14-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем uv для управления зависимостями
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Копируем файлы с зависимостями
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости с помощью uv
RUN uv sync --frozen --no-dev

# Копируем остальные файлы проекта
COPY . .

# Создаём непривилегированного пользователя
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

RUN chmod +x /app/migrations/create_db.sh

# Открываем порт (замените на ваш, если отличается)
EXPOSE 8000

# Команда запуска (используем uv run для запуска в виртуальном окружении)
CMD ["uv", "run", "src/main.py"]