
ENV_FILE=env
DJANGO_SETTINGS_MODULE=metrics_control.settings
CELERY_APP=celery:app
CELERY_WORKER=worker --loglevel=info --concurrency=4
CELERY_BEAT=beat --loglevel=info


help:
	@echo "Использование:"
	@echo "  make install     - установить зависимости"
	@echo "  make migrate     - выполнить миграции"
	@echo "  make run         - запустить Django сервер"
	@echo "  make run-celery  - запустить Celery worker"
	@echo "  make run-beat    - запустить Celery beat"
	@echo "  make run-all     - запустить всё вместе (в разных терминалах)"

install:
	@echo "Установка зависимостей..."
	poetry install

migrate:
	@echo "Применение миграций..."
	poetry run python src/manage.py migrate

run:
	@echo "Запуск Django сервера..."
	poetry run python src/manage.py runserver

run-celery:
	@echo "Запуск Celery worker..."
	poetry run celery -A src.celery_app worker --loglevel=info

run-beat:
	@echo "Запуск Celery beat..."
	poetry run celery -A src.celery_app beat --loglevel=info

run-all:
	@echo "Запуск всех компонентов (в разных терминалах):"
	@echo "1. Django: make run"
	@echo "2. Celery: make run-celery"
	@echo "3. Beat:   make run-beat"
