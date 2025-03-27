build:
	./build.sh
render-start:
	gunicorn task_manager.wsgi
install:
	uv sync
migrate:
	python manage.py migrate
start:
	python manage.py runserver
ruff:
	uv run ruff check task_manager/
format:
	uv run black task_manager/