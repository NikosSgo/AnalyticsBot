AnalyticsBot  
  
Telegram‑бот для аналитики видео. Пользователь задаёт вопрос текстом, бот отправляет запрос в LLM, получает `function_call`, собирает SQL, выполняет его в Postgres и возвращает результат.  
  
## Что внутри  
- Telegram‑бот на `aiogram`  
- LLM (через `openai.AsyncClient`)  
- Postgres с таблицами `videos` и `video_snapshots`  
- Миграции + загрузка демо‑данных из `migrations/videos.json`  
  
## Быстрый старт (Docker)  
1. Скопируйте и заполните переменные окружения:  
   - `cp .env.example .env.docker`  
2. Соберите и поднимите сервисы:  
   - `docker compose up -d --build`  
3. Инициализируйте БД и загрузите данные:  
   - `make migrate`  
4. Бот уже запущен в контейнере `analytics_bot`.  
  
## Локальный запуск (Python + Docker DB)  
1. Поднимите Postgres:  
   - `docker compose up -d db`  
2. Скопируйте и заполните переменные окружения:  
   - `cp .env.example .env`  
3. Установите зависимости:  
   - `uv sync`  
4. Примените миграции и загрузите данные:  
   - `make migrate`  
5. Запустите бота:  
   - `uv run python -m src.main`  
  
## Переменные окружения  
Минимально нужны:  
- `TG_BOT_TOKEN` — токен Telegram‑бота  
- `LLM_API_KEY`, `LLM_URL`, `LLM_MODEL` — настройки LLM  
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` — Postgres  
  
## Примеры вопросов  
- «Сколько просмотров у видео за вчера?»  
- «Топ‑5 видео по лайкам за неделю»  
- «Динамика просмотров по видео X»
