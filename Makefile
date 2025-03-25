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