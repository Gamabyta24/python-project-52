build:
	./build.sh
render-start:
	gunicorn task_manager.wsgi
install:
	uv sync
collectstatic:
	python manage.py collectstatic --no-input
migrate:
	python manage.py migrate