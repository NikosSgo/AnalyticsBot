.PHONY: migrate init-db

init-db:
	@echo "Создание базы данных в контейнере..."
	docker compose run --rm analytics_bot sh -c "/app/migrations/create_db.sh"

migrate: init-db
	@echo "Прогон SQL миграций..."
	docker compose run --rm analytics_bot sh -c 'psql -h db -U $$DB_USER -d $$DB_NAME -f /app/migrations/001_init.sql'
	docker compose run --rm analytics_bot sh -c 'psql -h db -U $$DB_USER -d $$DB_NAME -f /app/migrations/002_indexes.sql'
	@echo "Загрузка JSON в БД через uv..."
	docker compose run --rm analytics_bot sh -c 'uv run /app/migrations/load_json.py /app/migrations/videos.json'
	@echo "Миграции + JSON загружены"