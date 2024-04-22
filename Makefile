dev:
	poetry run python manage.py runserver

install:
	poetry install

start:
	poetry run gunicorn task_manager.wsgi

build:
	./build.sh